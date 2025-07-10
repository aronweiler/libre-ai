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
