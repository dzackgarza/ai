import argparse
import subprocess
import sys
OPENCODE_MANAGER_PACKAGE = "git+https://github.com/dzackgarza/opencode-manager.git"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse and display an OpenCode session transcript"
    )
    parser.add_argument(
        "session_id",
        help="OpenCode session ID (e.g., ses_abc123)"
    )
    args = parser.parse_args()

    result = subprocess.run(
        [
            "npx",
            "--yes",
            f"--package={OPENCODE_MANAGER_PACKAGE}",
            "opx-session",
            "transcript",
            args.session_id,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error rendering transcript: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    sys.stdout.write(result.stdout)


if __name__ == "__main__":
    main()
