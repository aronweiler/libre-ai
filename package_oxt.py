

import os
import shutil
import zipfile
import subprocess
import sys
import logging



# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

EXT_DIR = os.path.join(os.path.dirname(__file__), 'extension')
OXT_NAME = 'libreai.oxt'
OXT_PATH = os.path.join(os.path.dirname(__file__), OXT_NAME)




# List your pure-Python dependencies here (do not include tiktoken for now)
PYTHON_DEPS = [
    'langchain',
    # Add other pure-Python dependencies as needed
]

# Files and folders to include in the .oxt (at root)
INCLUDE = [
    'extension/',
    'pythonpath/',  # Bundled dependencies
    'Addons.xcu',
    'META-INF/',
    'description.xml',
    'manifest.xml',
]




def ensure_libreoffice_python():
    """
    Ensure that the script is being run with LibreOffice's Python 3.10.18 interpreter for binary compatibility.
    """
    import platform
    expected_version = (3, 10, 18)
    expected_exes = [
        os.path.normpath(r'C:\Program Files\LibreOffice\program\python.exe').lower(),
        os.path.normpath(r'C:\Program Files\LibreOffice\program\python-core-3.10.18\bin\python.exe').lower()
    ]
    actual_version = sys.version_info[:3]
    actual_exe = os.path.normpath(sys.executable).lower()
    valid_suffixes = [
        r'libreoffice\program\python.exe',
        r'libreoffice\program\python-core-3.10.18\bin\python.exe'
    ]
    if actual_version != expected_version or not any(actual_exe.endswith(suffix) for suffix in valid_suffixes):
        raise RuntimeError(
            f"\n[ERROR] You must run this script with LibreOffice's Python 3.10.18 for binary compatibility.\n"
            f"Current Python: {sys.executable} (version {sys.version})\n"
            f"Expected: {expected_exes[0]} or {expected_exes[1]} (version 3.10.18)\n"
            f"Run: \"C:\\Program Files\\LibreOffice\\program\\python.exe\" package_oxt.py\n"
        )

def ensure_pip_available():
    """
    Ensure that pip is available for the current Python interpreter.
    If not, print a clear error and exit.
    """
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        logging.error('pip is not installed for this Python interpreter. Please install pip before running this script.\n'
                      'You can usually install pip with: python -m ensurepip --upgrade')
        sys.exit(1)

def prepare_pythonpath():
    """
    Prepare the pythonpath/ directory by downloading and extracting all pure-Python dependencies.
    Cleans up any previous contents, downloads wheels, extracts them, and validates the result.
    Raises RuntimeError on any failure.
    """
    base_dir = os.path.dirname(__file__)
    pythonpath_dir = os.path.join(base_dir, 'pythonpath')
    # Clean up previous pythonpath directory
    if os.path.exists(pythonpath_dir):
        try:
            shutil.rmtree(pythonpath_dir)
            logging.info(f"Removed existing directory: {pythonpath_dir}")
        except Exception as e:
            raise RuntimeError(f"Failed to remove old pythonpath/: {e}")
    try:
        os.makedirs(pythonpath_dir, exist_ok=True)
        logging.info(f"Created directory: {pythonpath_dir}")
    except Exception as e:
        raise RuntimeError(f"Failed to create pythonpath/: {e}")

    # Download wheels for dependencies for the correct Python version and platform
    # On native builds (Windows), do NOT use --platform/--python-version/--implementation
    # On cross-platform builds (Linux Docker), use those flags
    import platform
    system = platform.system().lower()
    logging.info('Downloading dependencies (allowing binary wheels)...')
    try:
        if system == 'windows':
            # Native build: just download for current interpreter
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'download',
                '--dest', pythonpath_dir,
                '--only-binary', ':all:',
                *PYTHON_DEPS
            ])
        elif system == 'linux':
            # Cross-platform build: specify platform and python version
            pip_platform = 'manylinux2014_x86_64'
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'download',
                '--dest', pythonpath_dir,
                '--platform', pip_platform,
                '--python-version', '310',
                '--implementation', 'cp',
                '--only-binary', ':all:',
                *PYTHON_DEPS
            ])
        else:
            raise RuntimeError(f'Unsupported platform for packaging: {system}')
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to download dependencies: {e}")

    # Extract wheels/zip files
    extracted = set()
    for fname in os.listdir(pythonpath_dir):
        if fname.endswith('.whl') or fname.endswith('.zip'):
            logging.info(f'Extracting {fname}...')
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--no-deps', '--target', pythonpath_dir, os.path.join(pythonpath_dir, fname)
                ])
                extracted.add(fname)
                os.remove(os.path.join(pythonpath_dir, fname))
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Failed to extract {fname}: {e}")
            except Exception as e:
                raise RuntimeError(f"Failed to clean up {fname}: {e}")

    # Validate that dependencies are present
    missing = []
    for dep in PYTHON_DEPS:
        dep_dir = os.path.join(pythonpath_dir, dep.replace('-', '_'))
        if not os.path.exists(dep_dir):
            # Some packages may be single .py files or have different names; check for .dist-info as fallback
            found = False
            for entry in os.listdir(pythonpath_dir):
                if entry.lower().startswith(dep.replace('-', '_').lower()) and (entry.endswith('.dist-info') or entry.endswith('.egg-info')):
                    found = True
                    break
            if not found:
                missing.append(dep)
    if missing:
        raise RuntimeError(f"Missing dependencies after extraction: {missing}")
    logging.info('All dependencies extracted and validated.')


def package_oxt():
    """
    Package the LibreOffice AI extension as a .oxt file, including all code, resources, and bundled dependencies.
    Ensures the package is complete and production-ready.
    """
    base_dir = os.path.dirname(__file__)
    prepare_pythonpath()
    if os.path.exists(OXT_PATH):
        try:
            os.remove(OXT_PATH)
            logging.info(f"Removed existing package: {OXT_PATH}")
        except Exception as e:
            raise RuntimeError(f"Failed to remove old .oxt: {e}")
    try:
        with zipfile.ZipFile(OXT_PATH, 'w', zipfile.ZIP_DEFLATED) as oxt:
            for item in INCLUDE:
                abs_path = os.path.join(base_dir, item)
                if os.path.isdir(abs_path):
                    for root, _, files in os.walk(abs_path):
                        for f in files:
                            if f.endswith('.pyc'):
                                continue  # Skip .pyc files
                            rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                            oxt.write(os.path.join(root, f), rel_path)
                elif os.path.isfile(abs_path):
                    if not abs_path.endswith('.pyc'):
                        oxt.write(abs_path, os.path.basename(item))
        if not os.path.exists(OXT_PATH):
            raise RuntimeError(f"Packaging failed: {OXT_PATH} not created.")
        logging.info(f'Packaged extension as {OXT_PATH}')
    except Exception as e:
        raise RuntimeError(f"Failed to create .oxt: {e}")


if __name__ == '__main__':
    """
    Main entry point for packaging the LibreOffice AI extension.
    """
    ensure_libreoffice_python()
    ensure_pip_available()
    try:
        package_oxt()
        logging.info('Packaging completed successfully.')
    except Exception as exc:
        logging.error(f'Packaging failed: {exc}')
        sys.exit(1)
