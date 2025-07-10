# LLM Provider Plugin Architecture Design for LibreOffice AI Extension

## Purpose
This document details the design for a flexible, extensible, and user-friendly provider plugin system for integrating multiple LLM (Large Language Model) providers into the LibreOffice Writer AI extension. The system leverages LangChain for unified AI interactions and supports runtime configuration and provider selection via a user interface.

---

## 1. Architectural Overview

### Key Concepts
- **Provider Abstraction Layer:** All LLM providers inherit from a common LangChain base class, enabling a unified interface for AI interactions.
- **Plugin Architecture:** Each provider (OpenAI, Anthropic, Google, Ollama, etc.) is implemented as a plugin class that can be dynamically loaded and configured.
- **Runtime Selection:** The user can select their preferred provider and configure credentials and parameters at runtime.
- **UI Configuration Panel:** A user interface component allows users to select a provider, enter API keys, endpoints, model names, and other parameters, and save these settings securely.

---

## 2. Provider Abstraction and LangChain Integration

### Provider Interface
- All provider classes inherit from the appropriate LangChain base class (e.g., `BaseLLM` or `ChatOpenAI`, etc.).
- Each provider implements a standardized interface, e.g.:

```python
class ProviderBase:
    def generate(self, prompt: str, **kwargs) -> str:
        """Send a prompt to the provider and return the response."""
```

- At runtime, the extension instantiates the selected provider with user-supplied configuration.

### Supported Providers
- **OpenAI** (via LangChain's OpenAI integration)
- **Anthropic** (via LangChain's Anthropic integration)
- **Google** (via LangChain's Google integration)
- **Ollama** (via LangChain's Ollama integration)

Each provider class wraps the appropriate LangChain LLM class and exposes a unified `generate()` method.

---

## 3. Configuration Management


### User-Facing Configuration Dialog
- UI component accessible from the sidebar or menu.
- Allows users to:
    - Select a provider from a dropdown (OpenAI, Anthropic, Google, Ollama)
    - Enter and edit:
        - API keys
        - Endpoints
        - Model names
        - Model parameters (max tokens, temperature, etc.)
        - **Conversation length management:**
            - Set maximum conversation token limit (e.g., 100,000 tokens)
    - Save and load settings

### Configuration Storage
- Store settings using LibreOffice’s configuration system (UNO API) or a secure config file in the user’s profile directory.
- Sensitive data (API keys) should be stored securely (avoid plain text if possible).
- Support environment variables as an alternative for credentials.

---


## 4. Runtime Provider Loading and Conversation Length Management

- On extension startup or when the user changes settings:
    - Load the selected provider and configuration from storage.
    - Instantiate the corresponding provider class with the supplied credentials and parameters.
    - Use this instance for all AI interactions via LangChain.
    - **Conversation Compaction:**
        - Monitor the total token count of the ongoing conversation history.
        - When the conversation reaches the user-specified token limit, automatically summarize the conversation (conversation compaction/summarization).
        - Replace the conversation history with the summary, so that the conversation can continue without exceeding the limit.
        - Notify the user (e.g., via a message in the UI) when summarization occurs.
        - Summarization should ensure that critical parts of the existing conversation are preserved (i.e. the summarization prompt should ensure that key parts of the conversation are preserved, such as previous communications with agents, key interactions, etc.)

--- 

## 5. UI Component Design

### Layout
- Dropdown: Provider selection
- Input fields:
    - API key (masked input)
    - Endpoint URL (if required)
    - Model name
    - Model parameters (max tokens, temperature, etc.)
- Save/Cancel buttons
- Validation and error messages for incorrect or missing values

### Implementation
- Use LibreOffice UNO API to create the dialog (optionally design with Glade and load as a `.ui` file).
- Dynamically show/hide fields based on provider selection.
- Validate input before saving.

---

## 6. Security Considerations
- Do not log or expose API keys in error messages or logs.
- Encrypt sensitive data if possible.
- Support environment variable overrides for credentials.

---

## 7. Example Provider Class Skeleton

```python
from langchain.llms import OpenAI, Anthropic, GooglePalm, Ollama

class OpenAIProvider(OpenAI):
    def __init__(self, api_key: str, model_name: str, **params):
        super().__init__(openai_api_key=api_key, model_name=model_name, **params)
    def generate(self, prompt: str, **kwargs) -> str:
        return self(prompt, **kwargs)

# Similar classes for Anthropic, Google, Ollama...
```

---

## 8. Documentation and User Guidance
- Provide clear instructions for obtaining API keys and configuring each provider.
- Offer troubleshooting tips for common errors (invalid key, network issues, etc.).

---

## 9. Summary Table

| Provider   | Required Configurations             | LangChain Integration Class | Notes                                 |
|------------|------------------------------------|-----------------------------|---------------------------------------|
| OpenAI     | API Key, Model Name, Params        | OpenAI                      | https://platform.openai.com/          |
| Anthropic  | API Key, Model Name, Params        | Anthropic                   | https://console.anthropic.com/        |
| Google     | API Key, Model Name, Params        | GooglePalm                  | Gemini/PaLM APIs                      |
| Ollama     | Endpoint URL, Model Name, Params   | Ollama                      | Local LLM, https://ollama.com/        |

---

## 10. Implementation Guidance
- Keep provider classes modular and easy to extend for new providers.
- Ensure the UI is intuitive and validates input before saving.
- Regularly review security practices for handling credentials.
- Test each provider integration with sample prompts and parameters.

---

This design enables flexible, secure, and user-friendly integration of multiple LLM providers in your LibreOffice AI extension, leveraging LangChain for unified AI interactions and runtime configurability.