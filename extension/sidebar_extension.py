"""
UNO Sidebar Panel implementation for LibreAI.
"""
import sys
import os
# Ensure the parent directory of this file is on sys.path
ext_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(ext_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import uno
import unohelper
from com.sun.star.ui import XSidebarPanel
from extension.ui.sidebar import create_sidebar

class SidebarPanel(unohelper.Base, XSidebarPanel):
    def __init__(self, ctx):
        self.ctx = ctx
        self.panel = None
    def getComponent(self):
        if self.panel is None:
            self.panel = create_sidebar()
        return self.panel

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    SidebarPanel,
    "org.libreai.SidebarPanel",
    ("com.sun.star.ui.SidebarPanel",),
)
