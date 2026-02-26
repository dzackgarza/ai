import json
import sys
from pathlib import Path

def parse_transcript(file_path: str):
    if file_path == "-":
        f = sys.stdin
        print("=== Claude Code Transcript (from stdin) ===\n")
    else:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File {file_path} not found.")
            sys.exit(1)
        print(f"=== Claude Code Transcript: {path.name} ===\n")
        f = open(path, 'r', encoding='utf-8')
    
    try:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            
            # Look for lines containing a valid message object
            if 'message' in event and isinstance(event['message'], dict):
                msg = event['message']
                role = msg.get('role', 'unknown').upper()
                content = msg.get('content', '')
                
                print(f"\n[{role}]")
                
                # Simple string messages (usually early user prompts)
                if isinstance(content, str):
                    print(content.strip())
                    
                # Rich blocks (Claude's responses, tool executions, etc)
                elif isinstance(content, list):
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        block_type = block.get('type')
                        
                        if block_type == 'text':
                            print(block.get('text', '').strip())
                        
                        elif block_type == 'thinking':
                            thinking = block.get('thinking', '').strip()
                            print(f"🤔 [Thinking...]\n{thinking}")
                        
                        elif block_type == 'tool_use':
                            tool_name = block.get('name', 'unknown_tool')
                            inputs = json.dumps(block.get('input', {}), indent=2)
                            print(f"🛠️  [Tool Use: {tool_name}]\n{inputs}")
                            
                        elif block_type == 'tool_result':
                            res_content = block.get('content', '')
                            is_error = block.get('is_error', False)
                            err_flag = "❌ ERROR" if is_error else "✅"
                            
                            if isinstance(res_content, list):
                                res_str = "".join(
                                    b.get('text', '') for b in res_content if isinstance(b, dict) and b.get('type') == 'text'
                                )
                            else:
                                res_str = str(res_content)
                                
                            # Truncate giant tool outputs
                            if len(res_str) > 500:
                                res_str = res_str[:500] + "\n...[truncated]..."
                            print(f"{err_flag} [Tool Result]\n{res_str.strip()}")
                print("-" * 60)
    finally:
        if file_path != "-":
            f.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_claude_log.py <path-to-jsonl-file | ->")
        sys.exit(1)
        
    try:
        parse_transcript(sys.argv[1])
    except BrokenPipeError:
        sys.exit(0)
