import argparse
import sys
import subprocess
import os

OPENCODE_MANAGER_PACKAGE = "git+https://github.com/dzackgarza/opencode-manager.git"


def main():
    parser = argparse.ArgumentParser(
        description="Unified transcript parser for all agent CLIs"
    )
    parser.add_argument(
        "--harness",
        type=str,
        required=True,
        choices=["claude", "opencode", "codex", "kilocode", "gemini", "qwen", "amp"],
        help="Which agent CLI produced this transcript",
    )
    parser.add_argument("identifier", type=str, help="File path or ID to parse")

    args = parser.parse_args()

    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    # Map harnesses to their respective parser scripts
    script_map = {
        "claude": f"{scripts_dir}/parse_claude_log.py",
        "codex": f"{scripts_dir}/parse_codex_log.py",
        "kilocode": f"{scripts_dir}/parse_kilocode_log.py",
        "gemini": f"{scripts_dir}/parse_gemini_log.py",
        "qwen": f"{scripts_dir}/parse_qwen_log.py",
        "amp": f"{scripts_dir}/parse_amp_log.py",
    }

    try:
        if args.harness == "opencode":
            session_id = args.identifier
            subprocess.run(
                [
                    "npx",
                    "--yes",
                    f"--package={OPENCODE_MANAGER_PACKAGE}",
                    "opx-session",
                    "transcript",
                    session_id,
                ],
                check=True,
            )

        elif args.harness == "amp":
            subprocess.run(["python", script_map["amp"], args.identifier], check=True)

        else:
            # File-based parsers
            if args.identifier == "-":
                # Handle piped stdin
                subprocess.run(
                    ["python", script_map[args.harness], "-"],
                    stdin=sys.stdin,
                    check=True,
                )
            else:
                subprocess.run(
                    ["cat", args.identifier], stdout=subprocess.PIPE, check=True
                )
                subprocess.run(
                    f"cat {args.identifier} | python {script_map[args.harness]} -",
                    shell=True,
                    check=True,
                )

    except subprocess.CalledProcessError as e:
        print(f"Error parsing transcript: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
