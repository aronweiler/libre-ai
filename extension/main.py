
# Main entry: orchestrator, agent, and LLM provider integration

from extension.agent import ToolCallingAgent
from extension.llm_providers.provider_factory import get_provider_from_config
from extension.config import load_config
from extension.conversation_manager import ConversationManager

class LibreAIMain:
    def __init__(self, max_tokens=100000):
        self.config = load_config()
        self.provider = get_provider_from_config(self.config)
        self.agent = ToolCallingAgent()
        self.conversation = ConversationManager(max_tokens=max_tokens, summarizer=self._summarize)

    def reload_provider(self):
        self.config = load_config()
        self.provider = get_provider_from_config(self.config)

    def process_user_request(self, user_message):
        self.conversation.add_message("user", user_message)
        prompt = self._build_prompt()
        ai_response = self.provider.generate(prompt)
        self.conversation.add_message("ai", ai_response)
        tool_result = None
        if self._is_tool_call(ai_response):
            task_spec = self._parse_tool_call(ai_response)
            tool_result = self.agent.perform_task(task_spec)
        return {"ai_response": ai_response, "tool_result": tool_result, "conversation": self.conversation.get_history()}

    def _build_prompt(self):
        # Compose prompt from conversation history
        history = "\n".join([
            f"User: {m['content']}" if m['role'] == 'user' else f"AI: {m['content']}"
            for m in self.conversation.get_history()
        ])
        return f"{history}\nAI:"

    def _is_tool_call(self, ai_response):
        return ai_response.strip().startswith("{\"tool\":")

    def _parse_tool_call(self, ai_response):
        import json
        return json.loads(ai_response)

    def _summarize(self, history):
        # Use the provider to summarize conversation history
        summary_prompt = "Summarize the following conversation, preserving all key instructions, agent responses, and important context.\n" + \
            "\n".join([f"{m['role']}: {m['content']}" for m in history])
        return self.provider.generate(summary_prompt)
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
