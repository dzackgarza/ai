import json
target_ids = [
    "stepfun/step-3.5-flash:free",
    "arcee-ai/trinity-large-preview:free",
    "arcee-ai/trinity-mini:free",
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    "nvidia/nemotron-nano-9b-v2:free",
    "openai/gpt-oss-120b:free",
    "openai/gpt-oss-20b:free",
    "qwen/qwen3-4b:free",
    "qwen/qwen3-coder:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "upstage/solar-pro-3:free",
    "z-ai/glm-4.5-air:free"
]
file_path = "/home/dzack/.local/share/opencode/tool-output/tool_c9b80a4f9001JNA8kbLfC8QiZ2"
with open(file_path, 'r') as f:
    outer_json = json.load(f)
content = outer_json['page_content']
for tid in target_ids:
    if tid in content:
        print(f"FOUND: {tid}")
    else:
        print(f"NOT FOUND: {tid}")
