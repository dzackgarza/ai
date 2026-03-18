import sys
import os
import subprocess

def parse_amp_log(thread_id):
    if not thread_id:
        print("Error: Must provide a thread ID (e.g. T-...)")
        sys.exit(1)
        
    try:
        # We just wrap the native markdown command!
        subprocess.run(["amp", "threads", "markdown", thread_id], check=True)
    except FileNotFoundError:
        print("Error: 'amp' command not found. Is it installed and in your PATH?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error executing amp command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_amp_log.py <thread-id>")
        sys.exit(1)
        
    parse_amp_log(sys.argv[1])
