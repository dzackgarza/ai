import re
import os

with open('all_models_sorted.txt', 'r') as f:
    slugs = [line.strip() for line in f if line.strip()]

# Existing reported data to preserve
reported_data = {
    "OPENAI": {
        "GPT 5.2": ("80.00", "Reported", "OAI3"),
        "GPT 5.3 Codex": ("80–82 (est)", "Speculative", "OAI6"),
        "GPT 5.2 Codex": ("72.80", "Reported", "SWE-bench"),
        "GPT 5.1 Codex Max": ("77.90", "Reported", "OAI4"),
        "GPT 5 Codex": ("74.5 (est)", "Press-rep", "OAI5"),
        "GPT 5.1 Codex": ("66.00", "Reported", "SWE-bench"),
        "GPT 5.1": ("66.00", "Reported", "SWE-bench"),
        "GPT 5": ("65.00", "Reported", "SWE-bench"),
        "GPT 5 Mini": ("56.20", "Reported", "SWE-bench"),
        "GPT 5 Nano": ("34.80", "Reported", "SWE-bench"),
        "o3": ("58.40", "Reported", "SWE-bench"),
        "o4-mini": ("45.00", "Reported", "SWE-bench"),
        "GPT 4.1": ("39.58", "Reported", "SWE-bench"),
        "GPT 4.1 Mini": ("23.94", "Reported", "SWE-bench"),
        "GPT-4o": ("21.62", "Reported", "SWE-bench"),
        "GPT-OSS 120B": ("26.00", "Reported", "SWE-bench"),
        "Codex Mini Latest": ("68 (est)", "Inferred", "OAI1"),
    },
    "ANTHROPIC": {
        "Claude Opus 4.6": ("75.60", "Reported", "SWE-bench"),
        "Claude Opus 4.6 (with prompt modification)": ("81.42", "Reported*", "ANT5"),
        "Claude Opus 4.5": ("76.80", "Reported", "SWE-bench"),
        "Claude Opus 4.5 (medium)": ("74.40", "Reported", "SWE-bench"),
        "Claude Sonnet 4.6": ("80.20", "Reported", "ANT4"),
        "Claude Sonnet 4.5": ("71.40", "Reported", "SWE-bench"),
        "Claude Haiku 4.5": ("66.60", "Reported", "SWE-bench"),
        "Claude Opus 4.0": ("67.60", "Reported", "SWE-bench"),
        "Claude Sonnet 4.0": ("64.93", "Reported", "SWE-bench"),
        "Claude 3.7 Sonnet": ("63.70", "Reported", "ANT6"),
        "Claude 3.5 Sonnet (20241022)": ("49.00", "Reported", "ANT1"),
        "Claude 3.5 Haiku (20241022)": ("40.60", "Reported", "ANT1"),
        "Claude 3.5 Sonnet (20240620)": ("33.40", "Reported", "ANT1"),
        "Claude 3 Opus (20240229)": ("22.20", "Reported", "ANT1"),
        "Claude 3 Haiku (20240307)": ("7.20", "Reported", "ANT1"),
    },
    "GOOGLE DEEPMIND (GEMINI / GEMMA)": {
        "Gemini 3.1 Pro": ("80.60", "Reported", "G1"),
        "Gemini 3 Flash": ("75.80", "Reported", "SWE-bench"),
        "Gemini 3 Pro Preview": ("74.20", "Reported", "SWE-bench"),
        "Gemini 2.5 Pro": ("60.40", "Reported", "G2"),
        "Gemini 2.5 Flash": ("59.60", "Reported", "G2"),
        "Gemini 2.5 Flash Lite": ("31.60", "Reported", "G4"),
        "Gemini 2.0 Flash": ("13.52", "Reported", "SWE-bench"),
    },
    "MISTRAL AI": {
        "Devstral Small 2512": ("56.40", "Reported", "SWE-bench"),
        "Devstral 2512": ("53.80", "Reported", "SWE-bench"),
    },
    "MOONSHOT AI (KIMI)": {
        "Kimi K2.5": ("70.80", "Reported", "SWE-bench"),
        "Kimi K2 Instruct": ("65.80", "Reported", "SWE-bench"),
        "Kimi K2 Thinking": ("63.40", "Reported", "SWE-bench"),
    },
    "DEEPSEEK": {
        "DeepSeek V3.2": ("70.00", "Reported", "SWE-bench"),
        "DeepSeek V3.2 Reasoner": ("60.00", "Reported", "SWE-bench"),
        "DeepSeek V3.1 Terminus": ("68.40", "Reported", "SWE-bench"),
    },
    "MINIMAX": {
        "MiniMax M2.5": ("75.80", "Reported", "SWE-bench"),
        "MiniMax M2.1": ("74.00", "Reported", "SWE-bench"),
        "MiniMax M2": ("61.00", "Reported", "SWE-bench"),
    },
    "ZHIPU AI (GLM)": {
        "GLM 5": ("72.80", "Reported", "SWE-bench"),
        "GLM 4.7": ("73.80", "Reported", "SWE-bench"),
        "GLM 4.6 (T=1)": ("55.40", "Reported", "SWE-bench"),
        "GLM 4.5": ("54.20", "Reported", "SWE-bench"),
    },
    "ALIBABA (QWEN)": {
        "Qwen3 235B": ("70.00", "Reported", "SWE-bench"),
        "Qwen3 Coder 480B": ("70.60", "Reported", "SWE-bench"),
        "Qwen3 Coder 480B Instruct": ("55.40", "Reported", "SWE-bench"),
        "Qwen2.5 Coder 32B Instruct": ("9.00", "Reported", "SWE-bench"),
    },
    "META (LLAMA)": {
        "Llama 4 Maverick": ("21.04", "Reported", "SWE-bench"),
        "Llama 4 Scout": ("9.06", "Reported", "SWE-bench"),
    }
}

# Add dynamic sets
parsed_tables = {k: dict(v) for k, v in reported_data.items()}
parsed_tables["OTHER / OPEN SOURCE"] = {}
parsed_tables["NVIDIA (NEMOTRON)"] = {}
parsed_tables["ARCEE AI"] = {}
parsed_tables["UPSTAGE"] = {}

def canonicalize(slug):
    name = slug.split('/')[-1]
    name = name.replace(':', ' ').replace('-', ' ').title()
    # Fix specific capitalizations
    name = name.replace('Gpt', 'GPT').replace('Claude', 'Claude').replace('Gemini', 'Gemini')
    name = name.replace('Vl', 'VL').replace('Tts', 'TTS').replace('Ocr', 'OCR')
    name = name.replace('Opus', 'Opus').replace('Sonnet', 'Sonnet').replace('Haiku', 'Haiku')
    return name

def get_provider_and_name(slug):
    # Determine base provider
    prov = "OTHER / OPEN SOURCE"
    canon = canonicalize(slug)
    
    if 'gpt' in slug.lower() or 'o3' in slug.lower() or 'o4' in slug.lower() or 'codex' in slug.lower():
        prov = "OPENAI"
    elif 'claude' in slug.lower():
        prov = "ANTHROPIC"
    elif 'gemini' in slug.lower() or 'gemma' in slug.lower():
        prov = "GOOGLE DEEPMIND (GEMINI / GEMMA)"
    elif 'mistral' in slug.lower() or 'stral' in slug.lower() or 'mixtral' in slug.lower():
        prov = "MISTRAL AI"
    elif 'kimi' in slug.lower():
        prov = "MOONSHOT AI (KIMI)"
    elif 'deepseek' in slug.lower():
        prov = "DEEPSEEK"
    elif 'minimax' in slug.lower():
        prov = "MINIMAX"
    elif 'glm' in slug.lower() or 'zhipu' in slug.lower() or 'zai' in slug.lower():
        prov = "ZHIPU AI (GLM)"
    elif 'qwen' in slug.lower():
        prov = "ALIBABA (QWEN)"
    elif 'llama' in slug.lower():
        prov = "META (LLAMA)"
    elif 'nemotron' in slug.lower() or 'parakeet' in slug.lower():
        prov = "NVIDIA (NEMOTRON)"
    elif 'trinity' in slug.lower():
        prov = "ARCEE AI"
    elif 'solar' in slug.lower():
        prov = "UPSTAGE"
    elif 'phi' in slug.lower():
        prov = "MICROSOFT"
        if prov not in parsed_tables: parsed_tables[prov] = {}
        
    # Heuristics for score
    score = "10–20 (est)"
    status = "Speculative"
    source = "—"
    
    ls = slug.lower()
    if 'vision' in ls or 'vl' in ls or 'tts' in ls or 'embed' in ls or 'ocr' in ls or 'whisper' in ls or 'flux' in ls or 'audio' in ls or 'image' in ls or 'parakeet' in ls:
        score = "N/A"
        status = "Not a coder"
    elif '4.6' in ls or '3.1-pro' in ls or 'gpt-5.2' in ls or 'v3.2' in ls or 'm2.5' in ls or 'glm-5' in ls:
        score = "70–80 (est)"
        status = "Inferred"
    elif '4.5' in ls or '3-flash' in ls or 'gpt-5.1' in ls or 'm2.1' in ls or 'glm-4.7' in ls or 'k2.5' in ls:
        score = "70–78 (est)"
        status = "Inferred"
    elif '3.7' in ls or 'gpt-5' in ls or 'v3.1' in ls or 'm2' in ls or 'glm-4.6' in ls:
        score = "60–70 (est)"
        status = "Inferred"
    elif '3.5-sonnet' in ls or '2.5-pro' in ls or 'devstral' in ls:
        score = "45–60 (est)"
        status = "Inferred"
    elif '2.5-flash' in ls or '4.1' in ls:
        score = "30–45 (est)"
        status = "Inferred"
    elif '8b' in ls or '7b' in ls or '3b' in ls or '1b' in ls or '2b' in ls or 'mini' in ls or 'nano' in ls:
        score = "0–15 (est)"
        status = "Speculative"
        
    return prov, canon, score, status, source

for slug in slugs:
    prov, canon, score, status, source = get_provider_and_name(slug)
    
    # Check if a close variant exists in reported
    found = False
    for existing_name in parsed_tables[prov]:
        if existing_name.lower().replace(' ', '') == canon.lower().replace(' ', ''):
            found = True
            break
            
    if not found:
        # Avoid overriding reported data with speculative slug parses if possible
        # Check substring matches to prevent duplicates like "Gemini 2.5 Flash" vs "Gemini 2.5 Flash Preview 04 17"
        match_found = False
        for k in parsed_tables[prov].keys():
            if canon.lower() in k.lower() or k.lower() in canon.lower():
                # If they are very close, don't add
                if abs(len(canon) - len(k)) < 10:
                    match_found = True
                    break
        if not match_found:
            parsed_tables[prov][canon] = (score, status, source)

# Generate markdown
md = """# SWE-bench Verified Estimates (Feb 2026)

*Note: These tables are a reference file containing both reported SWE-bench Verified (pass@1 % resolved) scores and speculative/inferred estimates for internal agent model-selection heuristics. “Reported” means the % appears explicitly in a primary source or benchmark; “Inferred” means a version/alias mapping; “Speculative” means an extrapolation based on family size/tier.*
"""

for prov, models in parsed_tables.items():
    if not models: continue
    md += f"\n## {prov}\n\n"
    md += "| Model Name | SWE-bench Verified % | Status | Source key |\n"
    md += "|---|---|---|---|\n"
    
    # Sort models nicely (Reported first, then highest score to lowest conceptually, but alphabetical for simplicity here)
    sorted_models = sorted(models.items(), key=lambda x: (x[1][1] != 'Reported', x[0]))
    
    for name, data in sorted_models:
        md += f"| {name} | {data[0]} | {data[1]} | {data[2]} |\n"

with open('reference_data_full.md', 'w') as f:
    f.write(md)
