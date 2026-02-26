import json
import sys

def parse_opencode_json(file_path):
    if file_path == "-":
        content = sys.stdin.read()
        
        # OpenCode prints "Exporting session: ses_..." to stdout before the JSON
        if content.startswith("Exporting"):
            try:
                content = content[content.index("\n")+1:]
            except ValueError:
                pass
                
        if not content.strip():
            print("Error: No valid JSON found in stdin.")
            sys.exit(1)
            
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from stdin: {e}")
            sys.exit(1)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    info = data.get("info", {})
    print(f"=== OpenCode Transcript: {info.get('title', 'Unknown')} ({info.get('id', 'Unknown')}) ===\n")

    for msg in data.get("messages", []):
        role = msg.get("info", {}).get("role", "unknown").upper()
        
        # OpenCode often groups assistant actions over multiple messages,
        # but for readability we'll just print the blocks.
        print(f"\n[{role}]")
        
        for part in msg.get("parts", []):
            ptype = part.get("type")
            if ptype == "text":
                print(part.get("text", "").strip())
            elif ptype == "reasoning":
                print(f"🤔 [Thinking...]\n{part.get('text', '').strip()}")
            elif ptype == "tool":
                tool_name = part.get("tool", "unknown_tool")
                state = part.get("state", {})
                inputs = json.dumps(state.get("input", {}), indent=2)
                print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
                
                output = state.get("output", "")
                status = state.get("status", "")
                err_flag = "❌ ERROR" if status == "error" else "✅"
                
                if output:
                    res_content = str(output)
                    if len(res_content) > 500:
                        res_content = res_content[:500] + "\n...[truncated]..."
                    print(f"\n{err_flag} [Tool Result]\n{res_content.strip()}")
            elif ptype in ("step-start", "step-finish", "patch"):
                # Ignore internal agent loop markers and internal state patches
                continue
            else:
                print(f"[{ptype} block]")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_opencode_log.py <path-to-json-file | ->")
        sys.exit(1)
    
    try:
        parse_opencode_json(sys.argv[1])
    except BrokenPipeError:
        # Ignore broken pipe errors from commands like `head` closing stdout
        sys.exit(0)
