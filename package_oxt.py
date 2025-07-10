import os
import shutil
import zipfile

EXT_DIR = os.path.join(os.path.dirname(__file__), 'extension')
OXT_NAME = 'libreai.oxt'
OXT_PATH = os.path.join(os.path.dirname(__file__), OXT_NAME)

# Files and folders to include in the .oxt
INCLUDE = [
    'main.py',
    'uno_extension.py',
    'manifest.xml',
    'setup.cfg',
    'llm_providers/',
    'tools/',
    'ui/',
    'config.py',
    'logging_utils.py',
    '__init__.py',
]

def package_oxt():
    with zipfile.ZipFile(OXT_PATH, 'w', zipfile.ZIP_DEFLATED) as oxt:
        for item in INCLUDE:
            abs_path = os.path.join(EXT_DIR, item)
            if os.path.isdir(abs_path):
                for root, _, files in os.walk(abs_path):
                    for f in files:
                        rel_dir = os.path.relpath(root, EXT_DIR)
                        rel_file = os.path.join(rel_dir, f)
                        oxt.write(os.path.join(root, f), rel_file)
            elif os.path.isfile(abs_path):
                oxt.write(abs_path, item)
    print(f'Packaged extension as {OXT_PATH}')

if __name__ == '__main__':
    package_oxt()
