import os
import shutil
import zipfile


EXT_DIR = os.path.join(os.path.dirname(__file__), 'extension')
OXT_NAME = 'libreai.oxt'
OXT_PATH = os.path.join(os.path.dirname(__file__), OXT_NAME)

# Files and folders to include in the .oxt (at root)
INCLUDE = [
    'extension/',
    'Addons.xcu',
    'META-INF/',
    'description.xml',
    'manifest.xml',
]


def package_oxt():
    base_dir = os.path.dirname(__file__)
    if os.path.exists(OXT_PATH):
        os.remove(OXT_PATH)
    with zipfile.ZipFile(OXT_PATH, 'w', zipfile.ZIP_DEFLATED) as oxt:
        for item in INCLUDE:
            abs_path = os.path.join(base_dir, item)
            if os.path.isdir(abs_path):
                for root, _, files in os.walk(abs_path):
                    for f in files:
                        rel_path = os.path.relpath(os.path.join(root, f), base_dir)
                        oxt.write(os.path.join(root, f), rel_path)
            elif os.path.isfile(abs_path):
                oxt.write(abs_path, os.path.basename(item))
    if not os.path.exists(OXT_PATH):
        raise RuntimeError(f"Packaging failed: {OXT_PATH} not created.")
    print(f'Packaged extension as {OXT_PATH}')

if __name__ == '__main__':
    package_oxt()
