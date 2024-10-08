import sys
import json
from email_agent_model import run_email_processing

def main():
    try:
        # print("Email processing agent started")
        result = run_email_processing()
        print(f" {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error in agent: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()