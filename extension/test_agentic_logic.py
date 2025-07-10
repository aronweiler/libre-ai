"""
Test script for agentic orchestrator and tool-calling agent.
"""
from extension.orchestrator import Orchestrator

def main():
    orchestrator = Orchestrator()
    request = "Make the first paragraph bold."
    result = orchestrator.handle_user_request(request)
    print(result)

if __name__ == "__main__":
    main()
