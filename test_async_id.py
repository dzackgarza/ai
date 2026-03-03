import pexpect
import time
import sys


def main():
    print("Starting interactive opencode session...")

    # We use minimal agent to test async_command
    child = pexpect.spawn(
        "opencode", ["--agent", "Minimal"], encoding="utf-8", timeout=60
    )
    child.logfile_read = sys.stdout

    try:
        child.expect(r"Ask anything", timeout=10)
        time.sleep(2)

        print("\n\n>>> SENDING ASYNC SUBAGENT INSTRUCTION <<<")
        child.send(
            "Use the async_subagent tool to launch the 'Reviewer: Code' agent and tell it to 'Output the exact text: WATERMELON-TANGO'. Say 'Launched' when done.\r"
        )

        child.expect(r"Launched", timeout=20)

        print("\n\n>>> WAITING FOR SESSION ID INJECTION <<<")
        # Now wait for the session ID to be injected
        child.expect(r"Subagent Session ID: (ses_[a-zA-Z0-9]+)", timeout=30)
        session_id = child.match.group(1)
        print(f"\n\n>>> SUCCESS! Captured Session ID: {session_id} <<<")

        print("\n\n>>> WAITING FOR COMPLETION <<<")
        child.expect(r"WATERMELON-TANGO", timeout=40)
        print("\n\n>>> SUCCESS! The subagent completed. <<<")

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
