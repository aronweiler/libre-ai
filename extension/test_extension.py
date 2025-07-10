"""
Manual test script for extension logic (not for UNO runtime).
"""
from extension.orchestrator import Orchestrator

def main():
    orchestrator = Orchestrator()
    result = orchestrator.handle_user_request("Summarize this document.")
    print(result)

if __name__ == '__main__':
    main()
