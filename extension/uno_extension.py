"""
LibreOffice UNO registration and entry point for the extension.
"""
import uno
import unohelper
from com.sun.star.task import XJobExecutor
from extension.main import run

class LibreAIAgent(unohelper.Base, XJobExecutor):
    def __init__(self, ctx):
        self.ctx = ctx
    def trigger(self, args):
        run(args)

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    LibreAIAgent,
    "org.libreai.LibreAIAgent",
    ("com.sun.star.task.Job",),
)
