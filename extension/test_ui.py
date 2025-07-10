"""
Test script for UI components (sidebar and config dialog).
"""
from extension.ui.sidebar import create_sidebar
from extension.ui.config_dialog import show_config_dialog

def main():
    create_sidebar()
    show_config_dialog()

if __name__ == "__main__":
    main()
