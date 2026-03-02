#!/usr/bin/env python3
"""
Reconstruct OpenCode transcripts from Langfuse session data.

Key insight: each OpenCode trace's GENERATION input accumulates the full
conversation history. The LAST trace's GENERATION input IS the complete
transcript. We just walk it and enrich each assistant turn with per-step
metadata (timing, tokens, model) from the corresponding trace.

Usage:
    python parse_langfuse_opencode.py <session-id>
    python parse_langfuse_opencode.py ses_abc123 | python parse_opencode_log.py -
"""

import json
import sys
from datetime import timezone

from langfuse import get_client


def fmt_ts(dt):
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _gen(trace):
    return next((o for o in trace.observations if o.type == "GENERATION"), None)


def _span(trace):
    return next((o for o in trace.observations if o.type == "SPAN"), None)


def is_title_gen(trace):
    gen = _gen(trace)
    if not gen:
        return True
    history = gen.input if isinstance(gen.input, list) else []
    sys_prompt = next(
        (m.get("content", "") for m in history if m.get("role") == "system"), ""
    )
    return "title generator" in sys_prompt.lower()


def extract_step_meta(trace):
    """Timing/token/model metadata for one agent step."""
    gen = _gen(trace)
    span = _span(trace)
    if not gen:
        return {}
    anchor = span or gen
    s, e = anchor.start_time, anchor.end_time
    latency = round((e - s).total_seconds(), 3) if s and e else None
    usage = gen.usage_details or {}
    out_tok = (usage.get("output") or 0) + (usage.get("output_reasoning_tokens") or 0)
    tool_timings = {}
    for obs in trace.observations:
        if obs.type == "TOOL":
            cid = (obs.metadata or {}).get("attributes", {}).get("ai.toolCall.id")
            if cid:
                tool_timings[cid] = obs.latency
    return {
        "timestamp": fmt_ts(s),
        "latency_s": latency,
        "time_to_first_token_s": gen.time_to_first_token,
        "model": gen.model,
        "tokens": {
            "input": usage.get("input"),
            "output": out_tok or None,
            "input_cached": usage.get("input_cached_tokens"),
            "output_reasoning": usage.get("output_reasoning_tokens"),
            "total": (usage.get("input") or 0) + (out_tok or 0),
        },
        "tool_timings": tool_timings,
    }


def tool_obs_map(trace):
    """Map toolCallId -> (output_str, is_error, latency) from TOOL observations."""
    result = {}
    for obs in trace.observations:
        if obs.type != "TOOL":
            continue
        cid = (obs.metadata or {}).get("attributes", {}).get("ai.toolCall.id")
        if not cid:
            continue
        out = obs.output or {}
        result[cid] = (
            out.get("output", "") if isinstance(out, dict) else str(out),
            obs.level == "ERROR",
            obs.latency,
        )
    return result


def content_blocks(msg):
    c = msg.get("content", [])
    if isinstance(c, str):
        return [{"type": "text", "text": c}] if c.strip() else []
    return c if isinstance(c, list) else []


def walk_history(history, step_metas):
    """Walk conversation history, emit messages with per-step enrichment."""
    messages = []
    asst_idx = 0
    i = 0
    while i < len(history):
        msg = history[i]
        role = msg.get("role")

        if role == "system":
            i += 1
            continue

        if role == "user":
            blocks = content_blocks(msg)
            text = "\n".join(
                b.get("text", "") for b in blocks if b.get("type") == "text"
            ).strip()
            if text:
                messages.append(
                    {
                        "info": {"role": "user"},
                        "parts": [{"type": "text", "text": text}],
                    }
                )
            i += 1
            continue

        if role == "assistant":
            meta = step_metas[asst_idx] if asst_idx < len(step_metas) else {}
            timings = meta.get("tool_timings", {})
            parts = []
            for b in content_blocks(msg):
                bt = b.get("type")
                if bt == "reasoning":
                    t = (b.get("text") or "").strip()
                    if t:
                        parts.append({"type": "reasoning", "text": t})
                elif bt == "text":
                    t = (b.get("text") or "").strip()
                    if t:
                        parts.append({"type": "text", "text": t})
                elif bt == "tool-call":
                    parts.append(
                        {
                            "type": "tool",
                            "tool": b.get("toolName", "unknown"),
                            "state": {
                                "input": b.get("input", {}),
                                "output": "",
                                "status": "pending",
                            },
                            "timing": {"latency_s": timings.get(b.get("toolCallId"))},
                            "_call_id": b.get("toolCallId"),
                        }
                    )

            # Look ahead for tool-result message and merge
            if i + 1 < len(history) and history[i + 1].get("role") == "tool":
                results = {}
                for b in content_blocks(history[i + 1]):
                    if b.get("type") == "tool-result":
                        out = b.get("output", "")
                        if isinstance(out, dict):
                            out = out.get("value", str(out))
                        results[b.get("toolCallId", "")] = (
                            str(out),
                            b.get("isError", False),
                        )
                for p in parts:
                    if p["type"] == "tool" and p.get("_call_id") in results:
                        out_str, is_err = results[p["_call_id"]]
                        p["state"]["output"] = out_str
                        p["state"]["status"] = "error" if is_err else "success"
                i += 2
            else:
                i += 1

            # Strip internal _call_id
            for p in parts:
                p.pop("_call_id", None)

            info = {"role": "assistant"}
            info.update({k: v for k, v in meta.items() if k != "tool_timings"})
            messages.append({"info": info, "parts": parts})
            asst_idx += 1
            continue

        i += 1  # skip tool messages already consumed, or unknown roles

    return messages


def reconstruct(session_id: str) -> dict:
    lf = get_client()
    session = lf.api.sessions.get(session_id)
    stubs = sorted(session.traces, key=lambda t: t.timestamp)

    # Fetch full traces, separate title-gen from real
    all_traces = [lf.api.trace.get(s.id) for s in stubs]
    title_traces = [t for t in all_traces if is_title_gen(t)]
    real_traces = [t for t in all_traces if not is_title_gen(t)]

    if not real_traces:
        return {
            "info": {"id": session_id, "title": session_id, "source": "langfuse"},
            "messages": [],
            "summary": {},
        }

    # Title from title-gen trace output (a plain string)
    title = session_id
    for t in title_traces:
        g = _gen(t)
        if g and isinstance(g.output, str) and g.output.strip():
            title = g.output.strip()
            break

    # Per-step metadata
    step_metas = [extract_step_meta(t) for t in real_traces]

    # Full conversation = last real trace's GENERATION input
    last_gen = _gen(real_traces[-1])
    history = last_gen.input if isinstance(last_gen.input, list) else []

    messages = walk_history(history, step_metas)

    # Append last trace's own output (not yet in history)
    last_meta = step_metas[-1]
    raw_out = last_gen.output
    last_out = raw_out if isinstance(raw_out, dict) else None
    last_out_str = raw_out.strip() if isinstance(raw_out, str) else None
    has_tokens = (last_gen.usage_details or {}).get(
        "output_reasoning_tokens", 0
    ) > 0 or (last_gen.usage_details or {}).get("output", 0) > 0

    if last_out or last_out_str or has_tokens:
        parts = []
        if last_out_str:
            # Plain string output (e.g. final text-only response)
            parts.append({"type": "text", "text": last_out_str})
        elif last_out:
            text = (last_out.get("content") or "").strip()
            if text:
                parts.append({"type": "text", "text": text})
            tobs = tool_obs_map(real_traces[-1])
            raw_tcs = last_out.get("tool_calls", "[]")
            if isinstance(raw_tcs, str):
                try:
                    raw_tcs = json.loads(raw_tcs)
                except json.JSONDecodeError:
                    raw_tcs = []
            for tc in raw_tcs:
                cid = tc.get("toolCallId", "")
                out_str, is_err, tlat = tobs.get(cid, ("", False, None))
                parts.append(
                    {
                        "type": "tool",
                        "tool": tc.get("toolName", "unknown"),
                        "state": {
                            "input": tc.get("input", {}),
                            "output": out_str,
                            "status": "error" if is_err else "success",
                        },
                        "timing": {"latency_s": tlat},
                    }
                )
        info = {"role": "assistant"}
        info.update({k: v for k, v in last_meta.items() if k != "tool_timings"})
        messages.append({"info": info, "parts": parts})

    # Session bounds from ALL traces (including title-gen)
    s_start = s_end = None
    for t in all_traces:
        for obs in t.observations:
            if obs.start_time and (s_start is None or obs.start_time < s_start):
                s_start = obs.start_time
            if obs.end_time and (s_end is None or obs.end_time > s_end):
                s_end = obs.end_time

    wall_s = round((s_end - s_start).total_seconds(), 1) if s_start and s_end else None
    tok = {"input": 0, "output": 0, "input_cached": 0, "output_reasoning": 0}
    models, lats = set(), []
    for m in step_metas:
        t = m.get("tokens", {})
        tok["input"] += t.get("input") or 0
        tok["output"] += t.get("output") or 0
        tok["input_cached"] += t.get("input_cached") or 0
        tok["output_reasoning"] += t.get("output_reasoning") or 0
        if m.get("model"):
            models.add(m["model"])
        if m.get("latency_s") is not None:
            lats.append(m["latency_s"])

    return {
        "info": {"id": session_id, "title": title, "source": "langfuse"},
        "messages": messages,
        "summary": {
            "session_id": session_id,
            "started_at": fmt_ts(s_start),
            "ended_at": fmt_ts(s_end),
            "wall_clock_s": wall_s,
            "total_step_latency_s": round(sum(lats), 1) if lats else None,
            "llm_steps": len(lats),
            "models": sorted(models),
            "tokens": {**tok, "total": tok["input"] + tok["output"]},
        },
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_langfuse_opencode.py <session-id>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(reconstruct(sys.argv[1]), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
