# LibreAI LibreOffice Writer Extension

## Features
- AI-powered editing and conversation in LibreOffice Writer
- Supports OpenAI, Anthropic, Google, and Ollama via LangChain
- User-friendly sidebar and configuration dialog
- Robust agentic architecture with safe, atomic document editing
- Cross-platform: Windows, Linux, macOS

## Installation
1. Build the `.oxt` package:
   - Zip the contents of the `extension/` directory (including `uno_extension.py`, `manifest.xml`, and all submodules).
   - Rename the zip file to `libreai.oxt`.
2. Open LibreOffice Writer.
3. Go to `Tools > Extensions Manager` and add `libreai.oxt`.

## Configuration
- Use the sidebar or configuration dialog to select and configure your LLM provider (OpenAI, Anthropic, Google, Ollama).
- API keys and settings are stored securely in your user profile.

## Usage
- Open the sidebar from the LibreAI menu.
- Enter your prompt and interact with the AI agent.
- The agent can edit, insert, or replace text in your document.

## Development
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `python -m unittest discover tests`

## Packaging
- To create a distributable `.oxt` file, zip the contents of the `extension/` directory and rename the file extension to `.oxt`.

## Cross-Platform
- Tested on Windows, Linux, and macOS.
- All configuration and data are stored in platform-appropriate locations.
