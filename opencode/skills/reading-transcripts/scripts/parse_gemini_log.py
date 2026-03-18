import json
import sys

def parse_gemini_json(file_path):
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

    print(f"=== Gemini CLI Transcript: {data.get('sessionId', 'Unknown')} ===\n")

    for msg in data.get("messages", []):
        role = msg.get("type", "unknown").upper()
        
        # User message
        if role == "USER":
            print(f"\n[USER]")
            content = msg.get("content", [])
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    print(block.get("text", "").strip())
            print("-" * 60)
            
        # Assistant message
        elif role == "GEMINI":
            print(f"\n[ASSISTANT]")
            
            # Normal text content
            text_content = msg.get("content", "")
            if text_content:
                print(text_content.strip())
                
            # Tool calls
            tool_calls = msg.get("toolCalls", [])
            for tool in tool_calls:
                tool_name = tool.get("name", "unknown_tool")
                inputs = json.dumps(tool.get("args", {}), indent=2)
                print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
                
                # Try to extract the tool result which Gemini embeds inside the same message block
                result_display = tool.get("resultDisplay", "")
                if not result_display:
                    results = tool.get("result", [])
                    for res in results:
                        if isinstance(res, dict) and "functionResponse" in res:
                            resp = res["functionResponse"].get("response", {})
                            if isinstance(resp, dict):
                                result_display = str(resp.get("output", ""))
                                break
                            
                status = tool.get("status", "success")
                err_flag = "❌ ERROR" if status == "error" else "✅"
                
                if result_display:
                    res_str = str(result_display)
                    if len(res_str) > 500:
                        res_str = res_str[:500] + "\n...[truncated]..."
                    print(f"\n{err_flag} [Tool Result]\n{res_str.strip()}")
            print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_gemini_log.py <path-to-json-file | ->")
        sys.exit(1)
        
    try:
        parse_gemini_json(sys.argv[1])
    except BrokenPipeError:
        sys.exit(0)
