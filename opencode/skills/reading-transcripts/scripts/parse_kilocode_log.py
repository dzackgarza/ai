import json
import sys

def parse_kilocode_json(file_path):
    if file_path == "-":
        content = sys.stdin.read()
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from stdin: {e}")
            sys.exit(1)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
    if not isinstance(data, list):
        print("Error: Expected a JSON array of messages.")
        sys.exit(1)

    print(f"=== Kilocode Transcript ===\n")

    for msg in data:
        role = msg.get("role", "unknown").upper()
        print(f"\n[{role}]")
        
        content_blocks = msg.get("content", [])
        if isinstance(content_blocks, str):
            print(content_blocks.strip())
            print("-" * 60)
            continue
            
        for block in content_blocks:
            if not isinstance(block, dict):
                continue
                
            btype = block.get("type")
            
            if btype == "text":
                text = block.get("text", "").strip()
                if "<environment_details>" in text:
                    print("[Environment details truncated]")
                else:
                    print(text)
            elif btype == "tool_use":
                tool_name = block.get("name", "unknown_tool")
                inputs = json.dumps(block.get("input", {}), indent=2)
                print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
            elif btype == "tool_result":
                res = block.get("content", "")
                if isinstance(res, list):
                    res_str = "".join(str(b.get("text", "")) for b in res if isinstance(b, dict))
                else:
                    res_str = str(res)
                if len(res_str) > 500:
                    res_str = res_str[:500] + "\n...[truncated]..."
                err_flag = "❌ ERROR" if block.get("is_error") else "✅"
                print(f"{err_flag} [Tool Result]\n{res_str.strip()}")
            else:
                print(f"[{btype} block]")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_kilocode_log.py <path-to-json-file | ->")
        sys.exit(1)
        
    try:
        parse_kilocode_json(sys.argv[1])
    except BrokenPipeError:
        sys.exit(0)
