import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone as tz
from pathlib import Path


def parse_opencode_json(file_path: Path) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    info = data.get("info", {})
    print(
        f"=== OpenCode Transcript: {info.get('title', 'Unknown')} ({info.get('id', 'Unknown')}) ===\n"
    )

    for msg in data.get("messages", []):
        msg_info = msg.get("info", {})
        role = msg_info.get("role", "unknown").upper()

        # Timing/model header — handle both native opencode format and langfuse-enriched format
        meta_parts = []

        # Timestamp: langfuse uses info.timestamp (ISO str), native uses info.time.created (ms epoch)
        ts = msg_info.get("timestamp")
        if not ts:
            t = msg_info.get("time") or {}
            if isinstance(t, dict) and t.get("created"):
                ts = datetime.fromtimestamp(t["created"] / 1000, tz=tz.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
        if ts:
            meta_parts.append(ts)

        # Model: langfuse uses a plain string, native uses a dict
        model = msg_info.get("model")
        if isinstance(model, dict):
            model = model.get("modelID")
        if model:
            meta_parts.append(str(model))

        # Latency fields — only present in langfuse-enriched format
        if msg_info.get("latency_s") is not None:
            meta_parts.append(f"llm {msg_info['latency_s']:.1f}s")
        if msg_info.get("time_to_first_token_s") is not None:
            meta_parts.append(f"first token {msg_info['time_to_first_token_s']:.1f}s")

        # Native format latency from time.created / time.completed
        if not msg_info.get("latency_s"):
            t = msg_info.get("time") or {}
            if isinstance(t, dict) and t.get("created") and t.get("completed"):
                native_latency = (t["completed"] - t["created"]) / 1000
                meta_parts.append(f"llm {native_latency:.1f}s")

        tokens = msg_info.get("tokens", {})
        if tokens.get("total"):
            tok_parts = [f"in {tokens['input']:,}"]
            if tokens.get("input_cached"):
                tok_parts.append(f"{tokens['input_cached']:,} cached")
            tok_parts.append(f"out {tokens['output']:,}")
            if tokens.get("output_reasoning"):
                tok_parts.append(f"{tokens['output_reasoning']:,} reasoning")
            meta_parts.append("tokens: " + ", ".join(tok_parts))

        header = f"\n[{role}]"
        if meta_parts:
            header += f"  // {' | '.join(meta_parts)}"
        print(header)

        for part in msg.get("parts", []):
            ptype = part.get("type")
            if ptype == "text":
                print(part.get("text", "").strip())
            elif ptype == "reasoning":
                print(
                    f"🤔 [Thinking...]\n{part.get('text', '').strip()}\n[End of Thinking]"
                )
            elif ptype == "tool":
                tool_name = part.get("tool", "unknown_tool")
                state = part.get("state", {})
                timing = part.get("timing", {})
                inputs = json.dumps(state.get("input", {}), indent=2)
                tool_header = f"🛠️  [Tool Use: {tool_name}]"
                if timing.get("latency_s") is not None:
                    tool_header += f" (tool took {timing['latency_s']:.2f}s)"
                print(f"{tool_header}\n{inputs}")

                output = state.get("output", "")
                status = state.get("status", "")
                err_flag = "❌ ERROR" if status == "error" else "✅"

                if output:
                    res_content = str(output)
                    if len(res_content) > 500:
                        res_content = res_content[:500] + "\n...[truncated]..."
                    print(f"\n{err_flag} [Tool Result]\n{res_content.strip()}")
            elif ptype in ("step-start", "step-finish", "patch"):
                continue
            else:
                print(f"[{ptype} block]")
        print("-" * 60)

    # Summary block (present when data comes from langfuse)
    summary = data.get("summary")
    if summary:
        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        if summary.get("started_at"):
            print(f"  Started:         {summary['started_at']}")
        if summary.get("ended_at"):
            print(f"  Ended:           {summary['ended_at']}")
        if summary.get("wall_clock_s") is not None:
            print(f"  Wall clock:      {summary['wall_clock_s']}s")
        if summary.get("total_llm_latency_s") is not None:
            print(f"  LLM time:        {summary['total_llm_latency_s']}s")
        if summary.get("llm_steps") is not None:
            print(f"  LLM steps:       {summary['llm_steps']}")
        if summary.get("models"):
            print(f"  Models:          {', '.join(summary['models'])}")
        tok = summary.get("tokens", {})
        if tok.get("total"):
            print(f"  Tokens total:    {tok['total']:,}")
            print(f"    Input:         {tok.get('input', 0):,}")
            print(f"    Output:        {tok.get('output', 0):,}")
            if tok.get("input_cached"):
                print(f"    Cached:        {tok['input_cached']:,}")
            if tok.get("output_reasoning"):
                print(f"    Reasoning:     {tok['output_reasoning']:,}")
        print("=" * 60)


def export_session(session_id: str) -> Path:
    """Export an OpenCode session to a temp file and return the file path."""
    tmp_path = Path(tempfile.mktemp(suffix=".json"))
    with open(tmp_path, "w", encoding="utf-8") as tmp:
        result = subprocess.run(
            ["opencode", "export", session_id],
            stdout=tmp,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error exporting session: {result.stderr}", file=sys.stderr)
            tmp_path.unlink(missing_ok=True)
            sys.exit(1)
    return tmp_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse and display an OpenCode session transcript"
    )
    parser.add_argument(
        "session_id",
        help="OpenCode session ID (e.g., ses_abc123)"
    )
    args = parser.parse_args()

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        result = subprocess.run(
            ["opencode", "export", args.session_id],
            stdout=tmp,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error exporting session: {result.stderr}", file=sys.stderr)
            sys.exit(1)

    try:
        parse_opencode_json(tmp_path)
    finally:
        tmp_path.unlink()


if __name__ == "__main__":
    main()
