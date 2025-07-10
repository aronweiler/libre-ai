import uno
from com.sun.star.awt import XActionListener
from com.sun.star.awt.MessageBoxType import MESSAGEBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from com.sun.star.beans import PropertyValue
from com.sun.star.task import XJobExecutor
import os
import json

CONFIG_PATH = os.path.expanduser("~/.libreai_config.json")

PROVIDERS = [
    ("OpenAI", ["api_key", "model_name", "params"]),
    ("Anthropic", ["api_key", "model_name", "params"]),
    ("Google", ["api_key", "model_name", "params"]),
    ("Ollama", ["endpoint", "model_name", "params"]),
]

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)

def get_env_or_config(key, config):
    return os.environ.get(key.upper()) or config.get(key, "")

class ConfigDialog(XJobExecutor):
    def __init__(self, ctx):
        self.ctx = ctx
        self.config = load_config()
        self.dialog = None

    def trigger(self, args):
        self.show_dialog()

    def show_dialog(self):
        smgr = self.ctx.ServiceManager
        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", self.ctx)
        parent = toolkit.getDesktopWindow()
        dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialogModel", self.ctx)
        dialog.Width = 300
        dialog.Height = 250
        dialog.Title = "AI Provider Configuration"

        # Provider dropdown
        provider_names = [p[0] for p in PROVIDERS]
        dialog.insertByName("providerLabel", self._make_label("Provider:", 10, 10, 60, 15))
        dialog.insertByName("providerDropdown", self._make_dropdown("providerDropdown", provider_names, 80, 10, 150, 15))

        # API key / endpoint / model / params fields (dynamically shown)
        dialog.insertByName("apiKeyLabel", self._make_label("API Key:", 10, 40, 60, 15))
        dialog.insertByName("apiKeyField", self._make_textfield("apiKeyField", 80, 40, 150, 15, True))
        dialog.insertByName("endpointLabel", self._make_label("Endpoint:", 10, 70, 60, 15))
        dialog.insertByName("endpointField", self._make_textfield("endpointField", 80, 70, 150, 15, False))
        dialog.insertByName("modelLabel", self._make_label("Model:", 10, 100, 60, 15))
        dialog.insertByName("modelField", self._make_textfield("modelField", 80, 100, 150, 15, False))
        dialog.insertByName("paramsLabel", self._make_label("Params (JSON):", 10, 130, 90, 15))
        dialog.insertByName("paramsField", self._make_textfield("paramsField", 100, 130, 130, 15, False))

        # Save/Cancel buttons
        dialog.insertByName("saveButton", self._make_button("Save", 60, 180, 60, 20))
        dialog.insertByName("cancelButton", self._make_button("Cancel", 140, 180, 60, 20))

        # Set initial values
        provider = self.config.get("provider", "OpenAI")
        dialog.getByName("providerDropdown").SelectedItem = provider
        dialog.getByName("apiKeyField").Text = get_env_or_config("api_key", self.config)
        dialog.getByName("endpointField").Text = get_env_or_config("endpoint", self.config)
        dialog.getByName("modelField").Text = get_env_or_config("model_name", self.config)
        dialog.getByName("paramsField").Text = json.dumps(self.config.get("params", {}))

        # Show/hide fields based on provider
        self._update_fields(dialog, provider)
        dialog.getByName("providerDropdown").addItemListener(lambda e: self._update_fields(dialog, e.SelectedItem))

        # Button actions
        dialog.getByName("saveButton").addActionListener(lambda e: self._save(dialog))
        dialog.getByName("cancelButton").addActionListener(lambda e: self._close(dialog))

        self.dialog = dialog
        toolkit.createDialog(dialog).execute()

    def _make_label(self, text, x, y, w, h):
        model = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.awt.UnoControlFixedTextModel", self.ctx)
        model.PositionX = x
        model.PositionY = y
        model.Width = w
        model.Height = h
        model.Label = text
        return model

    def _make_dropdown(self, name, items, x, y, w, h):
        model = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.awt.UnoControlListBoxModel", self.ctx)
        model.PositionX = x
        model.PositionY = y
        model.Width = w
        model.Height = h
        model.StringItemList = tuple(items)
        model.Name = name
        return model

    def _make_textfield(self, name, x, y, w, h, masked):
        model = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.awt.UnoControlEditModel", self.ctx)
        model.PositionX = x
        model.PositionY = y
        model.Width = w
        model.Height = h
        model.Name = name
        model.EchoChar = "*" if masked else ""
        return model

    def _make_button(self, label, x, y, w, h):
        model = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.awt.UnoControlButtonModel", self.ctx)
        model.PositionX = x
        model.PositionY = y
        model.Width = w
        model.Height = h
        model.Label = label
        return model

    def _update_fields(self, dialog, provider):
        # Show/hide fields based on provider
        if provider == "Ollama":
            dialog.getByName("apiKeyLabel").Enabled = False
            dialog.getByName("apiKeyField").Enabled = False
            dialog.getByName("endpointLabel").Enabled = True
            dialog.getByName("endpointField").Enabled = True
        else:
            dialog.getByName("apiKeyLabel").Enabled = True
            dialog.getByName("apiKeyField").Enabled = True
            dialog.getByName("endpointLabel").Enabled = False
            dialog.getByName("endpointField").Enabled = False

    def _save(self, dialog):
        provider = dialog.getByName("providerDropdown").SelectedItem
        api_key = dialog.getByName("apiKeyField").Text
        endpoint = dialog.getByName("endpointField").Text
        model_name = dialog.getByName("modelField").Text
        try:
            params = json.loads(dialog.getByName("paramsField").Text)
        except Exception:
            self._show_error("Params must be valid JSON.")
            return
        config = {"provider": provider, "model_name": model_name, "params": params}
        if provider == "Ollama":
            config["endpoint"] = endpoint
        else:
            config["api_key"] = api_key
        save_config(config)
        self._close(dialog)

    def _close(self, dialog):
        dialog.endExecute()

    def _show_error(self, msg):
        toolkit = self.ctx.ServiceManager.createInstanceWithContext("com.sun.star.awt.Toolkit", self.ctx)
        parent = toolkit.getDesktopWindow()
        box = toolkit.createMessageBox(parent, MESSAGEBOX, BUTTONS_OK, "Error", msg)
        box.execute()
"""
Configuration dialog for provider selection and parameter entry.
"""


# Real configuration dialog using UNO API
import uno
from com.sun.star.awt.PosSize import POS, SIZE

def show_config_dialog():
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx).getCurrentComponent()
    parent_win = doc.CurrentController.Frame.ContainerWindow
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)

    width, height = 400, 320
    dialog = toolkit.createWindow({
        'Type': uno.getConstantByName('com.sun.star.awt.WindowClass.TOP'),
        'Parent': parent_win,
        'Bounds': (100, 100, width, height),
        'WindowAttributes': 0x10 | 0x20  # SIZEABLE | MOVEABLE
    })
    dialog.setVisible(True)

    # Provider dropdown
    provider_label = toolkit.createLabel()
    provider_label.setPosSize(20, 20, 120, 20, POS | SIZE)
    provider_label.setText("Provider:")
    dialog.addChild(provider_label)

    provider_dropdown = toolkit.createComboBox()
    provider_dropdown.setPosSize(150, 20, 200, 20, POS | SIZE)
    provider_dropdown.addItems(("OpenAI", "Anthropic", "Google", "Ollama"), 0)
    dialog.addChild(provider_dropdown)

    # API key
    api_label = toolkit.createLabel()
    api_label.setPosSize(20, 60, 120, 20, POS | SIZE)
    api_label.setText("API Key:")
    dialog.addChild(api_label)

    api_input = toolkit.createTextField()
    api_input.setPosSize(150, 60, 200, 20, POS | SIZE)
    api_input.setEchoChar("*")
    dialog.addChild(api_input)

    # Model name
    model_label = toolkit.createLabel()
    model_label.setPosSize(20, 100, 120, 20, POS | SIZE)
    model_label.setText("Model Name:")
    dialog.addChild(model_label)

    model_input = toolkit.createTextField()
    model_input.setPosSize(150, 100, 200, 20, POS | SIZE)
    dialog.addChild(model_input)

    # Params (temperature)
    temp_label = toolkit.createLabel()
    temp_label.setPosSize(20, 140, 120, 20, POS | SIZE)
    temp_label.setText("Temperature:")
    dialog.addChild(temp_label)

    temp_input = toolkit.createTextField()
    temp_input.setPosSize(150, 140, 200, 20, POS | SIZE)
    dialog.addChild(temp_input)

    # Save and Cancel buttons
    save_button = toolkit.createButton()
    save_button.setPosSize(80, 220, 100, 30, POS | SIZE)
    save_button.setLabel("Save")
    dialog.addChild(save_button)

    cancel_button = toolkit.createButton()
    cancel_button.setPosSize(220, 220, 100, 30, POS | SIZE)
    cancel_button.setLabel("Cancel")
    dialog.addChild(cancel_button)

    # Status label
    status_label = toolkit.createLabel()
    status_label.setPosSize(20, 180, 360, 20, POS | SIZE)
    status_label.setText("")
    dialog.addChild(status_label)

    # Load config if exists
    from extension.config import load_config, save_config
    config = load_config()
    provider_map = {"OpenAI": "openai", "Anthropic": "anthropic", "Google": "google", "Ollama": "ollama"}
    if config:
        provider_dropdown.setText(config.get("provider", "OpenAI"))
        api_input.setText(config.get("api_key", ""))
        model_input.setText(config.get("model_name", ""))
        temp_input.setText(str(config.get("params", {}).get("temperature", "")))

    def save_clicked(_):
        provider = provider_dropdown.getText()
        api_key = api_input.getText()
        model_name = model_input.getText()
        try:
            temperature = float(temp_input.getText())
        except Exception:
            temperature = 0.7
        if not provider:
            status_label.setText("Provider is required.")
            return
        if not api_key:
            status_label.setText("API key is required.")
            return
        if not model_name:
            status_label.setText("Model name is required.")
            return
        if not (0.0 <= temperature <= 2.0):
            status_label.setText("Temperature must be between 0.0 and 2.0.")
            return
        save_config({
            "provider": provider_map.get(provider, "openai"),
            "api_key": api_key,
            "model_name": model_name,
            "params": {"temperature": temperature}
        })
        status_label.setText("Configuration saved.")
        dialog.setVisible(False)

    def cancel_clicked(_):
        dialog.setVisible(False)

    save_button.addActionListener(lambda e: save_clicked(e))
    cancel_button.addActionListener(lambda e: cancel_clicked(e))
