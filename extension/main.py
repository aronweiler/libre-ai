"""
LibreOffice Writer AI Extension Entry Point
"""
import uno
from extension.orchestrator import Orchestrator

def run(*args):
    orchestrator = Orchestrator()
    # Example: show sidebar and config dialog on startup
    from extension.ui.sidebar import create_sidebar
    from extension.ui.config_dialog import show_config_dialog
    create_sidebar()
    show_config_dialog()
    orchestrator.start()
