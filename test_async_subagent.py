import pexpect
import time
import sys

def main():
    print("Starting interactive opencode session...")
    
    # We use minimal agent to test async_command
    child = pexpect.spawn("opencode", ["--agent", "Minimal"], encoding="utf-8", timeout=60)
    child.logfile_read = sys.stdout
    
    try:
        child.expect(r"Ask anything", timeout=10)
        time.sleep(2) 
        
        print("\n\n>>> SENDING ASYNC SUBAGENT INSTRUCTION <<<")
        child.send("Use the async_subagent tool to launch the 'Reviewer: Code' agent and tell it to 'Output the exact text: WATERMELON-TANGO'. Say 'Launched' when done.\r")
        
        child.expect(r"Launched", timeout=20)
        
        print("\n\n>>> MODEL RESPONDED, WAITING FOR SUBAGENT RESULT <<<")
        
        # Now wait for the async command to return and the model to pick it up
        child.expect(r"WATERMELON-TANGO", timeout=40)
        print("\n\n>>> SUCCESS! The subagent ran headless and woke the parent. <<<")
        
        child.send("/quit\r")
        time.sleep(1)
        
    except pexpect.TIMEOUT:
        print("\n\n>>> TIMEOUT: Expected output not found. <<<")
    except Exception as e:
        print(f"\n\n>>> ERROR: {e}")
        
    finally:
        if child.isalive():
            child.terminate()

if __name__ == "__main__":
    main()
