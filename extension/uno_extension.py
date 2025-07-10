"""
LibreOffice UNO registration and entry point for the extension.
"""
import sys
import os

# Ensure the parent directory and pythonpath/ are on sys.path
ext_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(ext_dir)
pythonpath_dir = os.path.join(parent_dir, 'pythonpath')
if pythonpath_dir not in sys.path:
    sys.path.insert(0, pythonpath_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import uno
import unohelper
from com.sun.star.task import XJobExecutor
from extension.main import run

class LibreAIAgent(unohelper.Base, XJobExecutor):
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        run(args)


# UNO registration helper
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    LibreAIAgent,
    "org.libreai.LibreAIAgent",
    ("com.sun.star.task.Job",),
)

# Required for registration: called by LibreOffice during extension registration
def writeRegistryInfo(serviceManager, registryKey):
    return g_ImplementationHelper.writeRegistryInfo(serviceManager, registryKey)
