"""
Automate building libreai_win.oxt and libreai_linux.oxt using Docker containers.
This script builds the .oxt for both Windows and Linux platforms and outputs them to the project root.
"""
import os
import subprocess
import sys
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
LINUX_DOCKERFILE = os.path.join(ROOT, 'Dockerfile.linux')
WIN_DOCKERFILE = os.path.join(ROOT, 'Dockerfile.windows')
LINUX_OXT = os.path.join(ROOT, 'libreai_linux.oxt')
WIN_OXT = os.path.join(ROOT, 'libreai_win.oxt')


def build_linux_oxt():
    print('[INFO] Building Linux .oxt using Docker...')
    # Clean pythonpath/ to avoid cross-platform wheel conflicts
    pythonpath_dir = os.path.join(ROOT, 'pythonpath')
    if os.path.exists(pythonpath_dir):
        shutil.rmtree(pythonpath_dir)
        print('[INFO] Removed existing pythonpath/ directory before Linux build.')
    # Build Docker image
    subprocess.check_call([
        'docker', 'build', '-f', LINUX_DOCKERFILE, '-t', 'libreai-linux-build', '.'
    ])
    # Run container and copy out the .oxt
    subprocess.check_call([
        'docker', 'run', '--rm', '-v', f'{ROOT}:/workspace', 'libreai-linux-build'
    ])
    # Move the output file
    built_oxt = os.path.join(ROOT, 'libreai.oxt')
    if os.path.exists(built_oxt):
        shutil.move(built_oxt, LINUX_OXT)
        print(f'[INFO] Linux .oxt created: {LINUX_OXT}')
    else:
        raise RuntimeError('Linux .oxt not found after build!')

def build_windows_oxt():
    print('[INFO] Building Windows .oxt natively...')
    # Clean pythonpath/ to avoid cross-platform wheel conflicts
    pythonpath_dir = os.path.join(ROOT, 'pythonpath')
    if os.path.exists(pythonpath_dir):
        shutil.rmtree(pythonpath_dir)
        print('[INFO] Removed existing pythonpath/ directory before Windows build.')
    # Run the packaging script natively with the current Python
    subprocess.check_call([
        sys.executable, os.path.join(ROOT, 'package_oxt.py')
    ])
    # Move the output file
    built_oxt = os.path.join(ROOT, 'libreai.oxt')
    if os.path.exists(built_oxt):
        shutil.move(built_oxt, WIN_OXT)
        print(f'[INFO] Windows .oxt created: {WIN_OXT}')
    else:
        raise RuntimeError('Windows .oxt not found after build!')

def main():
    build_linux_oxt()
    build_windows_oxt()
    print('[INFO] All builds complete.')

if __name__ == '__main__':
    main()
