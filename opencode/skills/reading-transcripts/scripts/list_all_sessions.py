import os
import glob
import subprocess
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

def count_turns_claude(path):
    """Count user turns in Claude JSONL session."""
    turns = 0
    with open(path) as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "user":
                    turns += 1
            except:
                pass
    return turns

def count_turns_qwen(path):
    """Count user turns in Qwen JSONL session."""
    turns = 0
    with open(path) as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "user":
                    turns += 1
            except:
                pass
    return turns

def count_turns_opencode(path):
    """Count user turns from OpenCode database."""
    import sqlite3
    db_path = Path(os.path.expanduser("~/.local/share/opencode/opencode.db"))
    if not db_path.exists():
        return 0
    
    # Extract session ID from path
    session_id_prefix = None
    path_str = str(path)
    if "ses_" in path_str:
        parts = path_str.split("ses_")
        if len(parts) > 1:
            id_part = parts[1].split(".")[0]
            if "_TOO" in id_part:
                id_part = id_part.split("_TOO")[0]
            session_id_prefix = "ses_" + id_part
    
    if not session_id_prefix:
        return 0
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM message WHERE session_id LIKE ? AND json_extract(data, '$.role') = 'user'",
            (session_id_prefix + "%",)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
    except Exception:
        return 0

def count_turns_kilocode(path):
    """Count user turns in Kilocode JSON session."""
    turns = 0
    try:
        with open(path) as f:
            data = json.load(f)
            for msg in data:
                if msg.get("role") == "user":
                    turns += 1
    except:
        pass
    return turns

def count_turns_codex(path):
    """Count user turns in Codex JSONL session."""
    turns = 0
    with open(path) as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "response_item" and data.get("payload", {}).get("role") == "user":
                    turns += 1
            except:
                pass
    return turns

def count_turns_gemini(path):
    """Count user turns in Gemini JSON session."""
    turns = 0
    try:
        with open(path) as f:
            data = json.load(f)
            for msg in data:
                if msg.get("role") == "user":
                    turns += 1
    except:
        pass
    return turns

def parse_datetime(dt_str):
    """Parse ISO 8601 datetime string. Requires full datetime with time, not just date."""
    if not dt_str:
        return None
    # Reject bare dates (no time component)
    if len(dt_str) == 10 and dt_str[4] == '-' and dt_str[7] == '-':
        raise argparse.ArgumentTypeError(
            f"Bare date '{dt_str}' not allowed. Must include time: YYYY-MM-DDTHH:MM:SS"
        )
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid datetime format: '{dt_str}'. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"
        )

def get_claude_sessions():
    sessions = []
    projects_dir = Path(os.path.expanduser("~/.claude/projects/"))
    if not projects_dir.exists():
        return sessions

    for proj_dir in projects_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        for jsonl in proj_dir.glob("*.jsonl"):
            mtime = jsonl.stat().st_mtime
            turns = count_turns_claude(str(jsonl))
            sessions.append({
                "harness": "Claude Code",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(jsonl),
                "turns": turns
            })
    return sessions

def get_opencode_sessions():
    """Get OpenCode sessions from database with turn counts."""
    import sqlite3
    sessions = []
    
    db_path = Path(os.path.expanduser("~/.local/share/opencode/opencode.db"))
    if not db_path.exists():
        return sessions
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.id, s.title, s.time_created, s.time_updated,
                   COUNT(CASE WHEN json_extract(m.data, '$.role') = 'user' THEN 1 END) as user_turns
            FROM session s
            LEFT JOIN message m ON s.id = m.session_id
            GROUP BY s.id
            ORDER BY s.time_updated DESC
        """)
        
        for row in cursor.fetchall():
            session_id, title, time_created, time_updated, user_turns = row
            sessions.append({
                "harness": "OpenCode",
                "time": time_updated / 1000 if time_updated else time_created / 1000,
                "project": "global",
                "title": title or "",
                "identifier": session_id,
                "turns": user_turns
            })
        
        conn.close()
    except Exception:
        pass
    
    return sessions

def get_codex_sessions():
    sessions = []
    sessions_dir = Path(os.path.expanduser("~/.codex/sessions/"))
    if not sessions_dir.exists():
        return sessions

    for jsonl in sessions_dir.rglob("*.jsonl"):
        mtime = jsonl.stat().st_mtime
        turns = count_turns_codex(str(jsonl))
        sessions.append({
            "harness": "Codex",
            "time": mtime,
            "project": "global",
            "identifier": str(jsonl),
            "turns": turns
        })
    return sessions

def get_kilocode_sessions():
    sessions = []
    tasks_dir = Path(os.path.expanduser("~/.kilocode/cli/global/tasks/"))
    if not tasks_dir.exists():
        return sessions

    for task_dir in tasks_dir.iterdir():
        if not task_dir.is_dir():
            continue
        hist_file = task_dir / "api_conversation_history.json"
        if hist_file.exists():
            mtime = hist_file.stat().st_mtime
            turns = count_turns_kilocode(str(hist_file))
            sessions.append({
                "harness": "Kilocode",
                "time": mtime,
                "project": "global",
                "identifier": task_dir.name,
                "turns": turns
            })
    return sessions

def get_gemini_sessions():
    sessions = []
    tmp_dir = Path(os.path.expanduser("~/.gemini/tmp/"))
    if not tmp_dir.exists():
        return sessions

    for proj_dir in tmp_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        chats_dir = proj_dir / "chats"
        if not chats_dir.exists():
            continue

        for json_file in chats_dir.glob("*.json"):
            mtime = json_file.stat().st_mtime
            turns = count_turns_gemini(str(json_file))
            sessions.append({
                "harness": "Gemini",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(json_file),
                "turns": turns
            })
    return sessions

def get_qwen_sessions():
    sessions = []
    projects_dir = Path(os.path.expanduser("~/.qwen/projects/"))
    if not projects_dir.exists():
        return sessions

    for proj_dir in projects_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        chats_dir = proj_dir / "chats"
        if not chats_dir.exists():
            continue

        for jsonl in chats_dir.glob("*.jsonl"):
            mtime = jsonl.stat().st_mtime
            turns = count_turns_qwen(str(jsonl))
            sessions.append({
                "harness": "Qwen",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(jsonl),
                "turns": turns
            })
    return sessions

def parse_amp_time(time_str):
    now = time.time()
    if not time_str or not time_str.endswith(" ago"):
        return 0
    val_str = time_str.replace(" ago", "").strip()
    try:
        if val_str.endswith("m"):
            return now - (int(val_str[:-1]) * 60)
        elif val_str.endswith("h"):
            return now - (int(val_str[:-1]) * 3600)
        elif val_str.endswith("d"):
            return now - (int(val_str[:-1]) * 86400)
        elif val_str.endswith("w"):
            return now - (int(val_str[:-1]) * 604800)
        elif val_str.endswith("mo"):
            return now - (int(val_str[:-2]) * 2592000)
    except:
        pass
    return 0

def get_amp_sessions():
    sessions = []
    try:
        result = subprocess.run(["amp", "threads", "list"], capture_output=True, text=True)
        if result.returncode != 0:
            return sessions
        lines = result.stdout.strip().split("\n")
        if len(lines) > 2:
            for line in lines[2:]:
                if not line.strip(): continue
                parts = line.split()
                thread_id = [p for p in parts if p.startswith("T-")]
                if thread_id:
                    tid = thread_id[0]
                    time_idx = -1
                    for i, p in enumerate(parts):
                        if p == "ago":
                            time_idx = i
                            break
                    if time_idx > 0:
                        title = " ".join(parts[:time_idx-1])
                        time_str = f"{parts[time_idx-1]} ago"
                        mtime = parse_amp_time(time_str)
                    else:
                        title = "Unknown"
                        mtime = 0
                    sessions.append({
                        "harness": "Amp",
                        "time": mtime,
                        "project": "global",
                        "title": title,
                        "identifier": tid
                    })
    except:
        pass
    return sessions

def main():
    parser = argparse.ArgumentParser(
        description="List all agent harness sessions with optional date filtering"
    )
    parser.add_argument(
        "--after",
        type=parse_datetime,
        help="Show sessions after this datetime (ISO 8601: YYYY-MM-DDTHH:MM:SS). Required: full datetime, not just date.",
    )
    parser.add_argument(
        "--before",
        type=parse_datetime,
        help="Show sessions before this datetime (ISO 8601: YYYY-MM-DDTHH:MM:SS). Required: full datetime, not just date.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=40,
        help="Maximum number of sessions to display (default: 40). Use 0 for no limit.",
    )
    parser.add_argument(
        "--harness",
        type=str,
        choices=["claude", "opencode", "codex", "kilocode", "gemini", "qwen", "amp"],
        help="Filter to a single harness only.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of formatted table.",
    )
    parser.add_argument(
        "--min-turns",
        type=int,
        default=0,
        help="Minimum number of turns to include.",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        help="Maximum number of turns to include.",
    )
    args = parser.parse_args()

    if not args.json:
        print("Scanning all agent harnesses for recent sessions...\n")
    all_sessions = []
    
    # Build session list based on harness filter
    if args.harness:
        harness_map = {
            "claude": get_claude_sessions,
            "opencode": get_opencode_sessions,
            "codex": get_codex_sessions,
            "kilocode": get_kilocode_sessions,
            "gemini": get_gemini_sessions,
            "qwen": get_qwen_sessions,
            "amp": get_amp_sessions,
        }
        all_sessions.extend(harness_map[args.harness]())
    else:
        all_sessions.extend(get_claude_sessions())
        all_sessions.extend(get_codex_sessions())
        all_sessions.extend(get_kilocode_sessions())
        all_sessions.extend(get_gemini_sessions())
        all_sessions.extend(get_qwen_sessions())
        all_sessions.extend(get_opencode_sessions())
        all_sessions.extend(get_amp_sessions())
    
    all_sessions.sort(key=lambda x: x.get("time", 0), reverse=True)
    seen_identifiers = set()
    deduped_sessions = []
    for s in all_sessions:
        if s["identifier"] not in seen_identifiers:
            seen_identifiers.add(s["identifier"])
            deduped_sessions.append(s)

    # Apply date filtering
    filtered_sessions = deduped_sessions
    if args.after:
        after_ts = args.after.timestamp()
        filtered_sessions = [s for s in filtered_sessions if s.get("time", 0) > after_ts]
    if args.before:
        before_ts = args.before.timestamp()
        filtered_sessions = [s for s in filtered_sessions if s.get("time", 0) < before_ts]

    # Apply turn count filtering
    if args.min_turns > 0:
        filtered_sessions = [s for s in filtered_sessions if (s.get("turns") or 0) >= args.min_turns]
    if args.max_turns is not None:
        filtered_sessions = [s for s in filtered_sessions if (s.get("turns") or 0) <= args.max_turns]

    total_found = len(filtered_sessions)

    # Apply limit
    if args.limit > 0:
        display_sessions = filtered_sessions[:args.limit]
        shown_count = len(display_sessions)
    else:
        display_sessions = filtered_sessions
        shown_count = total_found

    if args.json:
        # JSON output
        output = {
            "sessions": display_sessions,
            "total_found": total_found,
            "shown": shown_count,
            "filters": {
                "after": args.after.isoformat() if args.after else None,
                "before": args.before.isoformat() if args.before else None,
                "harness": args.harness,
                "min_turns": args.min_turns if args.min_turns > 0 else None,
                "max_turns": args.max_turns
            }
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        # Table output
        print(f"{'HARNESS':<15} | {'PROJECT':<30} | {'LAST MODIFIED':<20} | {'TURNS':>7} | {'IDENTIFIER / FILE'}")
        print("-" * 140)
        
        for s in display_sessions:
            harness = s["harness"]
            project = s["project"]
            if s["time"] > 0:
                dt = datetime.fromtimestamp(s["time"])
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = "Unknown"
            ident = s["identifier"]
            if ident.startswith(os.path.expanduser("~")):
                ident = "~" + ident[len(os.path.expanduser("~")):]
            if s.get("title"):
                ident = f"{ident} ({s['title'][:40]}...)"
            
            turns_str = str(s.get("turns", "N/A")) if s.get("turns") is not None else "N/A"
            print(f"{harness:<15} | {project[:28]:<30} | {time_str:<20} | {turns_str:>7} | {ident}")

        # Print summary if truncation occurred or to show total
        if args.limit > 0 and shown_count < total_found:
            print(f"\n[Showing {shown_count} of {total_found} sessions. Use --limit N to adjust.]")
        elif total_found == 0:
            print(f"\n[No sessions found matching criteria.]")
        else:
            print(f"\n[Total: {total_found} sessions]")

if __name__ == "__main__":
    main()
