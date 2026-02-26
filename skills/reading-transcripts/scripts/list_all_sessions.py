import os
import glob
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path

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
            sessions.append({
                "harness": "Claude Code",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(jsonl)
            })
    return sessions

def get_opencode_sessions():
    sessions = []
    # opencode logs are also in ~/.local/share/opencode/logs/ as .txt sometimes
    logs_dir = Path(os.path.expanduser("~/.local/share/opencode/logs/"))
    if logs_dir.exists():
        for txt in logs_dir.glob("*.txt"):
            if "ses_" in txt.name:
                mtime = txt.stat().st_mtime
                # Extract session ID from filename like 20260224_040548_ses_37250e920ffeEGr8.txt
                parts = txt.name.split("_")
                ses_id = ""
                for i, p in enumerate(parts):
                    if p == "ses" and i+1 < len(parts):
                        ses_id = f"ses_{parts[i+1].split('.')[0]}"
                        break
                
                if ses_id:
                    sessions.append({
                        "harness": "OpenCode",
                        "time": mtime,
                        "project": "global",
                        "identifier": ses_id
                    })
    
    # If we couldn't find logs, fallback to CLI
    if not sessions:
        try:
            result = subprocess.run(["opencode", "session", "list", "--json"], capture_output=True, text=True)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for s in data:
                    sessions.append({
                        "harness": "OpenCode",
                        "time": s.get("updatedAt", 0) / 1000,
                        "project": "global",
                        "title": s.get("title", ""),
                        "identifier": s.get("id", "")
                    })
        except:
            pass
            
    return sessions

def get_codex_sessions():
    sessions = []
    sessions_dir = Path(os.path.expanduser("~/.codex/sessions/"))
    if not sessions_dir.exists():
        return sessions
        
    for jsonl in sessions_dir.rglob("*.jsonl"):
        mtime = jsonl.stat().st_mtime
        sessions.append({
            "harness": "Codex",
            "time": mtime,
            "project": "global",
            "identifier": str(jsonl)
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
            sessions.append({
                "harness": "Kilocode",
                "time": mtime,
                "project": "global",
                "identifier": task_dir.name
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
            sessions.append({
                "harness": "Gemini",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(json_file)
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
            sessions.append({
                "harness": "Qwen",
                "time": mtime,
                "project": proj_dir.name,
                "identifier": str(jsonl)
            })
    return sessions

def parse_amp_time(time_str):
    """Convert Amp's '1m ago', '2d ago', '1w ago' to a Unix timestamp."""
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
                # Amp format: Title  Last Updated  Visibility  Messages  Thread ID
                parts = line.split()
                thread_id = [p for p in parts if p.startswith("T-")]
                
                if thread_id:
                    tid = thread_id[0]
                    # Title is everything before 'ago' minus the number/unit
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
    print("Scanning all agent harnesses for recent sessions...\n")
    
    all_sessions = []
    all_sessions.extend(get_claude_sessions())
    all_sessions.extend(get_codex_sessions())
    all_sessions.extend(get_kilocode_sessions())
    all_sessions.extend(get_gemini_sessions())
    all_sessions.extend(get_qwen_sessions())
    all_sessions.extend(get_opencode_sessions())
    all_sessions.extend(get_amp_sessions())
    
    # Sort by time, most recent first
    all_sessions.sort(key=lambda x: x.get("time", 0), reverse=True)
    
    # Deduplicate OpenCode (sometimes we get multiple hits for the same session)
    seen_identifiers = set()
    deduped_sessions = []
    for s in all_sessions:
        if s["identifier"] not in seen_identifiers:
            seen_identifiers.add(s["identifier"])
            deduped_sessions.append(s)
    
    # Print formatted table
    print(f"{'HARNESS':<15} | {'PROJECT':<30} | {'LAST MODIFIED':<20} | {'IDENTIFIER / FILE'}")
    print("-" * 130)
    
    for s in deduped_sessions[:40]: # Show top 40
        harness = s["harness"]
        project = s["project"]
        
        # Format time
        if s["time"] > 0:
            dt = datetime.fromtimestamp(s["time"])
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            time_str = "Unknown"
            
        ident = s["identifier"]
        
        # Truncate long paths to make it readable
        if ident.startswith(os.path.expanduser("~")):
            ident = "~" + ident[len(os.path.expanduser("~")):]
            
        # Add title if available (OpenCode/Amp)
        if s.get("title"):
            ident = f"{ident} ({s['title'][:40]}...)"
            
        print(f"{harness:<15} | {project[:28]:<30} | {time_str:<20} | {ident}")

if __name__ == "__main__":
    main()
