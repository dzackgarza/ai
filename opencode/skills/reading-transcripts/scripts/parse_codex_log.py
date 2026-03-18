import json
import sys

def parse_codex_jsonl(file_path):
    if file_path == "-":
        f = sys.stdin
        print("=== Codex CLI Transcript (from stdin) ===\n")
    else:
        try:
            f = open(file_path, 'r', encoding='utf-8')
            print(f"=== Codex CLI Transcript: {file_path} ===\n")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            sys.exit(1)
            
    try:
        for line in f:
            if not line.strip():
                continue
                
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            event_type = event.get("type")
            payload = event.get("payload", {})
            
            if event_type == "response_item":
                item_type = payload.get("type")
                
                if item_type == "message":
                    role = payload.get("role", "unknown").upper()
                    if role == "DEVELOPER" or role == "UNKNOWN":
                        continue
                    
                    print(f"\n[{role}]")
                    for block in payload.get("content", []):
                        btype = block.get("type")
                        if btype == "input_text" or btype == "text":
                            print(block.get("text", "").strip())
                    print("-" * 60)
                    
                elif item_type == "reasoning":
                    text = payload.get('text', '').strip()
                    if text:
                        print(f"\n🤔 [Thinking...]\n{text}")
                        print("-" * 60)
                    
                elif item_type in ["function_call", "custom_tool_call"]:
                    print(f"\n[ASSISTANT]")
                    tool_name = payload.get("name", "unknown")
                    inputs = payload.get("arguments", {})
                    if isinstance(inputs, str):
                        try:
                            inputs = json.loads(inputs)
                        except:
                            pass
                    if isinstance(inputs, dict):
                        inputs = json.dumps(inputs, indent=2)
                    print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
                    print("-" * 60)
                    
                elif item_type in ["function_call_output", "custom_tool_call_output"]:
                    print(f"\n[USER]")
                    output = payload.get("output", "")
                    if len(str(output)) > 500:
                        output = str(output)[:500] + "\n...[truncated]..."
                    print(f"✅ [Tool Result]\n{str(output).strip()}")
                    print("-" * 60)
                
            elif event_type == "event_msg":
                msg_type = payload.get("type")
                if msg_type == "user_message":
                    print(f"\n[USER]")
                    print(payload.get("message", "").strip())
                    print("-" * 60)
                elif msg_type == "agent_message":
                    phase = payload.get("phase", "")
                    print(f"\n[ASSISTANT ({phase})]")
                    print(payload.get("message", "").strip())
                    print("-" * 60)
                
    finally:
        if file_path != "-":
            f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_codex_log.py <path-to-jsonl-file | ->")
        sys.exit(1)
        
    try:
        parse_codex_jsonl(sys.argv[1])
    except BrokenPipeError:
        sys.exit(0)
