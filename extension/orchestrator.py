"""
Agentic Orchestrator: Handles user requests, context extraction, and task specification.
"""
from extension.agent import ToolAgent
from extension.tools.document_tools import get_document_context

class Orchestrator:
    def __init__(self):
        self.agent = ToolAgent()

    def start(self):
        # Entry point for the extension
        # TODO: Connect to UI and event loop
        pass

    def handle_user_request(self, request):
        context = get_document_context()
        # For demo: extract a simple task spec
        task_spec = self.create_task_spec(request, context)
        result = self.agent.execute_task(task_spec)
        return result

    def create_task_spec(self, request, context):
        # Example: create a structured task spec
        # In production, use NLP to parse request and extract intent, context, constraints
        return {
            "task_id": "1",
            "description": request,
            "document_context": context,
            "constraints": {"max_retries": 3},
            "rationale": "User request parsed by orchestrator."
        }
