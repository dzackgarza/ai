import json
file_path = "/home/dzack/.local/share/opencode/tool-output/tool_c9b80a4f9001JNA8kbLfC8QiZ2"
with open(file_path, 'r') as f:
    outer_json = json.load(f)
content = outer_json['page_content']
print(f"Content length: {len(content)}")
print(f"Start: {content[:100]!r}")
print(f"End: {content[-100:]!r}")
