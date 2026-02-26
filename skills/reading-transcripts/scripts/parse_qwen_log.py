import json
import sys

def parse_qwen_jsonl(file_path):
    if file_path == "-":
        f = sys.stdin
        print("=== Qwen Code Transcript (from stdin) ===\n")
    else:
        try:
            f = open(file_path, 'r', encoding='utf-8')
            print(f"=== Qwen Code Transcript: {file_path} ===\n")
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
                
            # Qwen uses type user, assistant, system, tool_result
            event_type = event.get("type", "unknown")
            msg = event.get("message", {})
            
            # Skip pure telemetry blocks
            if event_type == "system" and "ui_telemetry" in event.get("subtype", ""):
                continue
            
            if not msg:
                continue
                
            role = msg.get("role", event_type).upper()
            if role == "MODEL":
                role = "ASSISTANT"
                
            print(f"\n[{role}]")
            
            parts = msg.get("parts", [])
            for part in parts:
                if not isinstance(part, dict):
                    continue
                    
                # Standard text or thinking text
                if "text" in part:
                    text = part["text"].strip()
                    if part.get("thought") is True:
                        print(f"🤔 [Thinking...]\n{text}")
                    else:
                        print(text)
                
                # Tool calls (functionCall in Qwen)
                elif "functionCall" in part:
                    fcall = part["functionCall"]
                    tool_name = fcall.get("name", "unknown_tool")
                    inputs = json.dumps(fcall.get("args", {}), indent=2)
                    print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
                
                # Tool results (functionResponse in Qwen)
                elif "functionResponse" in part:
                    fresp = part["functionResponse"]
                    resp_data = fresp.get("response", {})
                    if isinstance(resp_data, dict):
                        output = resp_data.get("output", "")
                    else:
                        output = str(resp_data)
                        
                    if len(output) > 500:
                        output = output[:500] + "\n...[truncated]..."
                    print(f"✅ [Tool Result]\n{str(output).strip()}")
                    
                else:
                    print(f"[{list(part.keys())[0]} block]")
            
            print("-" * 60)
            
    finally:
        if file_path != "-":
            f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_qwen_log.py <path-to-jsonl-file | ->")
        sys.exit(1)
        
    try:
        parse_qwen_jsonl(sys.argv[1])
    except BrokenPipeError:
        sys.exit(0)
