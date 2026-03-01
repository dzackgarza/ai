#!/usr/bin/env python3
"""
Reconstruct OpenCode transcripts from Langfuse session data via the Langfuse Python SDK.
Reads LANGFUSE_BASE_URL, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY from environment.

Usage:
    python parse_langfuse_opencode.py <session-id>
    python parse_langfuse_opencode.py ses_abc123 | python parse_opencode_log.py -

Architecture notes:
    Each OpenCode agent step = one Langfuse trace with 3 observation types:
      - SPAN:       full step wall-clock (use for step timing)
      - GENERATION: LLM call — input=full history, output=gen_out dict, usage/TTFT
      - TOOL:       one per tool call — has tool call ID, output, latency

    Key invariant (how OpenCode instruments traces):
      - gen_out (GENERATION output) contains tool_calls + text content for step N
      - Reasoning blocks for step N appear in step N+1's GENERATION history as the
        new assistant block at index N (0-based among assistant turns)
      - The last step typically has gen_out=None (pure reasoning, no tool/text output)
      - Trace 0 is always the title-generator; skip it

    Lookahead pattern:
      - Collect all real (non-title-gen) traces upfront
      - For step i, grab reasoning from real_traces[i+1].history.assistant_blocks[i]
"""

import json
import sys
from datetime import timezone

from langfuse import get_client


def fmt_ts(dt) -> str | None:
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_history(trace) -> list:
    gen = next((o for o in trace.observations if o.type == "GENERATION"), None)
    if not gen:
        return []
    return gen.input if isinstance(gen.input, list) else []


def is_title_gen(trace) -> bool:
    history = get_history(trace)
    sys_prompt = next(
        (m.get("content", "") for m in history if m.get("role") == "system"), ""
    )
    return "title generator" in sys_prompt.lower()


def assistant_blocks(history: list) -> list:
    """Return list of content-block-lists, one per assistant turn in history."""
    return [
        (m.get("content") or []) if isinstance(m.get("content"), list) else []
        for m in history
        if m.get("role") == "assistant"
    ]


def tool_results_map(trace) -> dict:
    """Map toolCallId -> (output_str, is_error, latency_s) from TOOL observations."""
    results = {}
    for obs in trace.observations:
        if obs.type != "TOOL":
            continue
        call_id = (obs.metadata or {}).get("attributes", {}).get("ai.toolCall.id")
        if not call_id:
            continue
        out = obs.output or {}
        output_str = out.get("output", "") if isinstance(out, dict) else str(out)
        results[call_id] = (output_str, obs.level == "ERROR", obs.latency)
    return results


def parts_from_reasoning_blocks(blocks: list) -> list:
    """Extract reasoning parts from an assistant history content block list."""
    parts = []
    for block in blocks:
        if block.get("type") == "reasoning":
            text = (block.get("text") or "").strip()
            if text:
                parts.append({"type": "reasoning", "text": text})
    return parts


def parts_from_gen_out(gen_out: dict, tool_results: dict) -> list:
    """Extract text + tool parts from GENERATION output dict."""
    parts = []
    text = (gen_out.get("content") or "").strip()
    if text:
        parts.append({"type": "text", "text": text})

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
    return parts


def reconstruct(session_id: str) -> dict:
    lf = get_client()
    session = lf.api.sessions.get(session_id)

    # Fetch full traces (includes inline observations) and filter title-gen
    all_traces = sorted(session.traces, key=lambda t: t.timestamp)
    real_traces = []
    for t_stub in all_traces:
        trace = lf.api.trace.get(t_stub.id)
        if not is_title_gen(trace):
            real_traces.append(trace)

    all_messages = []
    total_tokens = {"input": 0, "output": 0, "input_cached": 0, "output_reasoning": 0}
    models_used = set()
    step_latencies = []
    session_start = None
    session_end = None

    for step_idx, trace in enumerate(real_traces):
        gen = next((o for o in trace.observations if o.type == "GENERATION"), None)
        span = next((o for o in trace.observations if o.type == "SPAN"), None)
        if not gen:
            continue

        history = gen.input if isinstance(gen.input, list) else []
        usage = gen.usage_details or {}
        tool_results = tool_results_map(trace)

        # Timing from SPAN (full step wall-clock)
        anchor = span or gen
        step_start = anchor.start_time
        step_end = anchor.end_time
        step_latency = (
            round((step_end - step_start).total_seconds(), 3)
            if step_start and step_end
            else None
        )

        # Track session bounds
        for obs in trace.observations:
            if obs.start_time and (
                session_start is None or obs.start_time < session_start
            ):
                session_start = obs.start_time
            if obs.end_time and (session_end is None or obs.end_time > session_end):
                session_end = obs.end_time

        # Output tokens: sum output + reasoning to match native opencode total
        out_tokens = (usage.get("output") or 0) + (
            usage.get("output_reasoning_tokens") or 0
        )
        total_output_tokens = out_tokens or None

        # ── New user message ──────────────────────────────────────────────────
        # Last user msg in history not followed by an assistant reply
        last_user = None
        for msg in history:
            if msg.get("role") == "user":
                last_user = msg
            elif msg.get("role") == "assistant":
                last_user = None

        if last_user is not None:
            content = last_user.get("content", "")
            if isinstance(content, list):
                text = "\n".join(
                    b.get("text", "")
                    for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            else:
                text = str(content)
            text = text.strip()
            if text:
                all_messages.append(
                    {
                        "info": {"role": "user"},
                        "parts": [{"type": "text", "text": text}],
                    }
                )

        # ── New assistant turn ────────────────────────────────────────────────
        # Reasoning for step N is stored in step N+1's history at index step_idx
        reasoning_parts = []
        if step_idx + 1 < len(real_traces):
            next_history = get_history(real_traces[step_idx + 1])
            asst = assistant_blocks(next_history)
            if step_idx < len(asst):
                reasoning_parts = parts_from_reasoning_blocks(asst[step_idx])

        # Content/tool parts from gen_out
        gen_out = gen.output if isinstance(gen.output, dict) else {}
        content_parts = parts_from_gen_out(gen_out, tool_results) if gen_out else []

        parts = reasoning_parts + content_parts

        if parts or total_output_tokens:
            all_messages.append(
                {
                    "info": {
                        "role": "assistant",
                        "timestamp": fmt_ts(step_start),
                        "latency_s": step_latency,
                        "time_to_first_token_s": gen.time_to_first_token,
                        "model": gen.model,
                        "tokens": {
                            "input": usage.get("input"),
                            "output": total_output_tokens,
                            "input_cached": usage.get("input_cached_tokens"),
                            "output_reasoning": usage.get("output_reasoning_tokens"),
                            "total": (usage.get("input") or 0)
                            + (total_output_tokens or 0),
                        },
                    },
                    "parts": parts,
                }
            )

        # Accumulate totals
        total_tokens["input"] += usage.get("input") or 0
        total_tokens["output"] += total_output_tokens or 0
        total_tokens["input_cached"] += usage.get("input_cached_tokens") or 0
        total_tokens["output_reasoning"] += usage.get("output_reasoning_tokens") or 0
        if gen.model:
            models_used.add(gen.model)
        if step_latency is not None:
            step_latencies.append(step_latency)

    wall_clock_s = (
        round((session_end - session_start).total_seconds(), 1)
        if session_start and session_end
        else None
    )

    summary = {
        "session_id": session_id,
        "started_at": fmt_ts(session_start),
        "ended_at": fmt_ts(session_end),
        "wall_clock_s": wall_clock_s,
        "total_step_latency_s": round(sum(step_latencies), 1)
        if step_latencies
        else None,
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

    title = next(
        (t.name for t in all_traces if not is_title_gen(lf.api.trace.get(t.id))),
        session_id,
    )

    return {
        "info": {"id": session_id, "title": title, "source": "langfuse"},
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
