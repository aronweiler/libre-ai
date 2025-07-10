"""
Tool-Calling Agent: Receives task specs, performs edits, handles retries, returns results.
"""
from extension.tools import document_tools


import logging
from extension.tools import document_tools

class ToolAgent:
    def perform_edit_task(self, task_spec: dict) -> dict:
        """
        Receives a task specification, performs the requested edits (with retries if needed),
        and returns a result dict with status, any errors, and a summary of changes.
        """
        log = []
        errors = []
        status = "failure"
        summary = ""
        max_retries = task_spec.get("constraints", {}).get("max_retries", 3)
        for attempt in range(1, max_retries + 1):
            try:
                # Example: parse description and call tool functions
                desc = task_spec.get("description", "")
                ctx = task_spec.get("document_context", {})
                # This is a placeholder: real implementation would parse desc and call tools
                # For demo, just call a sample tool
                if "bold" in desc.lower():
                    # Example: apply bold to first paragraph
                    ok = document_tools.set_bold(0, 10, True)
                    log.append("Applied bold to first 10 chars.")
                    if not ok:
                        raise Exception("Failed to apply bold.")
                status = "success"
                summary = "Task executed successfully."
                break
            except Exception as e:
                errors.append(str(e))
                log.append(f"Attempt {attempt} failed: {e}")
        else:
            summary = "Task failed after retries."
        return {
            "status": status,
            "summary": summary,
            "errors": errors,
            "log": log
        }

    def execute_task(self, task_spec):
        # Backward compatibility: call perform_edit_task
        return self.perform_edit_task(task_spec)
