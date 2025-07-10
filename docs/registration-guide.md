# Registering and Testing Your LibreOffice AI Extension Locally

This guide explains how to package, register, and test your LibreOffice extension (plugin) on your local machine.

---

## 1. Package Your Extension as an `.oxt` File

1. **Prepare your extension folder structure:**
    ```
    my-extension/
    ├── description.xml
    ├── python/
    │   └── myscript.py
    ├── Addons.xcu
    ├── META-INF/
    │   └── manifest.xml
    ```
    - Include all necessary files: Python scripts, `description.xml`, UI files, and any resources.

2. **Create the `.oxt` file:**
    - Select all files and folders inside your extension directory (not the directory itself).
    - Right-click and choose **Send to > Compressed (zipped) folder**.
    - Rename the resulting `.zip` file to `.oxt` (e.g., `my-extension.oxt`).

---

## 2. Install the Extension in LibreOffice

1. Open **LibreOffice Writer**.
2. Go to **Tools > Extension Manager**.
3. Click **Add...**.
4. Browse to your `.oxt` file and select it.
5. Follow the prompts to install.
6. **Restart LibreOffice** to ensure the extension is fully loaded.

---

## 3. Where Are Extensions Installed?

- **User extensions:** Installed to your user profile (no admin rights needed).
- **System extensions:** Can be installed system-wide by placing the `.oxt` in LibreOffice’s `share/extensions` directory (requires admin rights).

---

## 4. Testing and Debugging

- After installation, your extension’s features (sidebar, menus, etc.) should appear in LibreOffice Writer.
- To update your extension:
    1. Uninstall the old version from Extension Manager.
    2. Install the new `.oxt` file.
- **Logs and errors:**
    - Windows: `%APPDATA%\LibreOffice\4\user\uno_packages\cache\uno_packages.log`
    - Linux: `~/.config/libreoffice/4/user/uno_packages/cache/uno_packages.log`
- Check these logs if your extension does not work as expected.

---

## 5. Command Line Installation (Optional)

You can also install extensions via the command line:
```sh
soffice --headless --invisible --norestore --accept="socket,host=localhost,port=2002;urp;" --install-extension path/to/your-extension.oxt
```

---

## 6. Useful Tips

- **Quick reload:** Remove and re-add the extension for rapid iteration.
- **Python path:** LibreOffice uses its own Python interpreter. Ensure your scripts are compatible.
- **Cross-platform:** These steps work on Windows, Linux, and macOS.

---

## 7. References

- [LibreOffice Extension Development Wiki](https://wiki.documentfoundation.org/Development/Extension_Development)
- [Python Extensions for LibreOffice](https://wiki.documentfoundation.org/Macros/Python_Guide)

---

By following this guide, you can efficiently package, register, and test your LibreOffice AI extension on your local system.