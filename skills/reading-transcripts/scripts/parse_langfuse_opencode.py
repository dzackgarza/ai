#!/usr/bin/env python3
"""
Reconstruct OpenCode transcripts from Langfuse session data via the Langfuse Python SDK.
Reads LANGFUSE_BASE_URL, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY from environment.

Usage:
    python parse_langfuse_opencode.py <session-id>
    python parse_langfuse_opencode.py ses_abc123 | python parse_opencode_log.py -
"""

import json
import sys
from datetime import timezone

from langfuse import Langfuse


def tool_results_by_call_id(observations) -> dict:
    """Map toolCallId -> (output_str, is_error, latency_s) from TOOL-type observations."""
    results = {}
    for obs in observations:
        if obs.type != "TOOL":
            continue
        call_id = (obs.metadata or {}).get("attributes", {}).get("ai.toolCall.id")
        if not call_id:
            continue
        out = obs.output or {}
        output_str = out.get("output", "") if isinstance(out, dict) else str(out)
        results[call_id] = (output_str, obs.level == "ERROR", obs.latency)
    return results


def content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def fmt_ts(dt) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parts_from_content_blocks(blocks: list, tool_results: dict) -> list:
    """Convert a list of assistant content blocks into opencode-style parts."""
    parts = []
    for block in blocks:
        btype = block.get("type")
        if btype == "reasoning":
            text = (block.get("text") or "").strip()
            if text:
                parts.append({"type": "reasoning", "text": text})
        elif btype == "text":
            text = (block.get("text") or "").strip()
            if text:
                parts.append({"type": "text", "text": text})
        elif btype == "tool-call":
            call_id = block.get("toolCallId", "")
            output_str, is_error, tool_latency = tool_results.get(
                call_id, ("", False, None)
            )
            parts.append(
                {
                    "type": "tool",
                    "tool": block.get("toolName", "unknown"),
                    "state": {
                        "input": block.get("input", {}),
                        "output": output_str,
                        "status": "error" if is_error else "success",
                    },
                    "timing": {"latency_s": tool_latency},
                }
            )
    return parts


def trace_to_messages(trace, observations) -> list:
    """
    Extract only the NEW messages contributed by this trace.

    Strategy:
    - Skip title-generator traces (different system prompt).
    - The GENERATION input is the full accumulated history. The *new* content is:
        - New user message: last user msg in history not followed by an assistant reply.
        - New assistant turn: either from gen_out (tool_calls/content) OR from the last
          assistant block in history when gen_out is empty (happens on final summary steps).
    - Timestamp and latency come from the SPAN (covers full step inc. tool execution),
      not the GENERATION (LLM-only).
    - Output tokens = output + output_reasoning_tokens to match native opencode format.
    """
    generation = next((o for o in observations if o.type == "GENERATION"), None)
    span = next((o for o in observations if o.type == "SPAN"), None)
    if not generation:
        return []

    history = generation.input if isinstance(generation.input, list) else []

    # Skip internal opencode title-generator traces
    system_prompt = next(
        (m.get("content", "") for m in history if m.get("role") == "system"), ""
    )
    if "title generator" in system_prompt.lower():
        return []

    tool_results = tool_results_by_call_id(observations)
    usage = generation.usage_details or {}

    # Step timing from SPAN (full step wall-clock), falling back to GENERATION
    step_start = (span or generation).start_time
    step_end = (span or generation).end_time
    step_latency = (
        round((step_end - step_start).total_seconds(), 3)
        if step_start and step_end
        else None
    )

    # Output tokens: sum non-reasoning + reasoning to match native opencode total
    out_tokens = (usage.get("output") or 0) + (
        usage.get("output_reasoning_tokens") or 0
    )
    total_output_tokens = out_tokens if out_tokens else None

    messages = []

    # New user message: last user msg in history with no subsequent assistant reply
    last_user = None
    for msg in history:
        role = msg.get("role")
        if role == "user":
            last_user = msg
        elif role == "assistant":
            last_user = None

    if last_user is not None:
        text = content_to_text(last_user.get("content", "")).strip()
        if text:
            messages.append(
                {
                    "info": {"role": "user"},
                    "parts": [{"type": "text", "text": text}],
                }
            )

    # New assistant turn: prefer gen_out, fall back to last assistant block in history
    gen_out = generation.output if isinstance(generation.output, dict) else {}
    parts = []

    final_text = gen_out.get("content", "").strip()
    if final_text:
        parts.append({"type": "text", "text": final_text})

    raw_tcs = gen_out.get("tool_calls", "[]")
    if isinstance(raw_tcs, str):
        try:
            raw_tcs = json.loads(raw_tcs)
        except json.JSONDecodeError:
            raw_tcs = []

    for tc in raw_tcs:
        call_id = tc.get("toolCallId", "")
        output_str, is_error, tool_latency = tool_results.get(
            call_id, ("", False, None)
        )
        parts.append(
            {
                "type": "tool",
                "tool": tc.get("toolName", "unknown"),
                "state": {
                    "input": tc.get("input", {}),
                    "output": output_str,
                    "status": "error" if is_error else "success",
                },
                "timing": {"latency_s": tool_latency},
            }
        )

    # If gen_out was empty, read the new assistant block from history tail
    if not parts:
        for msg in reversed(history):
            if msg.get("role") == "assistant":
                blocks = msg.get("content") or []
                if isinstance(blocks, list):
                    parts = parts_from_content_blocks(blocks, tool_results)
                break

    if parts:
        messages.append(
            {
                "info": {
                    "role": "assistant",
                    "timestamp": fmt_ts(step_start),
                    "latency_s": step_latency,
                    "time_to_first_token_s": generation.time_to_first_token,
                    "model": generation.model,
                    "tokens": {
                        "input": usage.get("input"),
                        "output": total_output_tokens,
                        "input_cached": usage.get("input_cached_tokens"),
                        "output_reasoning": usage.get("output_reasoning_tokens"),
                        "total": (usage.get("input") or 0) + (total_output_tokens or 0),
                    },
                },
                "parts": parts,
            }
        )

    return messages


def reconstruct(session_id: str) -> dict:
    lf = Langfuse()
    session = lf.api.sessions.get(session_id)
    traces = sorted(session.traces, key=lambda t: t.timestamp)

    all_messages = []
    total_tokens = {"input": 0, "output": 0, "input_cached": 0, "output_reasoning": 0}
    models_used = set()
    step_latencies = []
    session_start = None
    session_end = None

    for trace in traces:
        observations = lf.api.observations.get_many(trace_id=trace.id).data
        observations.sort(key=lambda o: o.start_time)
        msgs = trace_to_messages(trace, observations)
        all_messages.extend(msgs)

        for msg in msgs:
            info = msg.get("info", {})
            if info.get("role") != "assistant":
                continue
            tokens = info.get("tokens", {})
            total_tokens["input"] += tokens.get("input") or 0
            total_tokens["output"] += tokens.get("output") or 0
            total_tokens["input_cached"] += tokens.get("input_cached") or 0
            total_tokens["output_reasoning"] += tokens.get("output_reasoning") or 0
            if info.get("model"):
                models_used.add(info["model"])
            if info.get("latency_s") is not None:
                step_latencies.append(info["latency_s"])

        for obs in observations:
            if obs.start_time and (
                session_start is None or obs.start_time < session_start
            ):
                session_start = obs.start_time
            if obs.end_time and (session_end is None or obs.end_time > session_end):
                session_end = obs.end_time

    wall_clock_s = (
        round((session_end - session_start).total_seconds(), 1)
        if session_start and session_end
        else None
    )
    total_step_s = round(sum(step_latencies), 1) if step_latencies else None

    summary = {
        "session_id": session_id,
        "started_at": fmt_ts(session_start),
        "ended_at": fmt_ts(session_end),
        "wall_clock_s": wall_clock_s,
        "total_step_latency_s": total_step_s,
        "llm_steps": len(step_latencies),
        "models": sorted(models_used),
        "tokens": {
            "input": total_tokens["input"],
            "output": total_tokens["output"],
            "input_cached": total_tokens["input_cached"],
            "output_reasoning": total_tokens["output_reasoning"],
            "total": total_tokens["input"] + total_tokens["output"],
        },
    }

    return {
        "info": {
            "id": session_id,
            "title": traces[0].name if traces else session_id,
            "source": "langfuse",
        },
        "messages": all_messages,
        "summary": summary,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_langfuse_opencode.py <session-id>", file=sys.stderr)
        sys.exit(1)

    transcript = reconstruct(sys.argv[1])
    print(json.dumps(transcript, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
