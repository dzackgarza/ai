import subprocess
import time

test_models = [
    "cerebras/gpt-oss-120b",
    "google/gemini-flash-latest",
    "groq/llama-3.3-70b-versatile",
    "nvidia/stepfun-ai/step-3.5-flash",
    "opencode/minimax-m2.5-free",
    "openrouter-free/openrouter/free",
    "openrouter-free/stepfun/step-3.5-flash:free",
    "openrouter-free/meta-llama/llama-3.3-70b-instruct:free",
    "openrouter-free/qwen/qwen3-coder:free"
]

results = []

for model in test_models:
    print(f"Testing {model}...")
    start_time = time.time()
    try:
        # Using a very simple prompt to minimize tokens
        res = subprocess.run(
            ["opencode", "run", "-m", model, "hi"],
            capture_output=True,
            text=True,
            timeout=30 # 30s timeout per test
        )
        duration = time.time() - start_time
        if res.returncode == 0:
            status = "✅ PASS"
            output = res.stdout.strip()
        else:
            status = "❌ FAIL"
            output = res.stderr.strip() or res.stdout.strip()
    except subprocess.TimeoutExpired:
        status = "⏱️ TIMEOUT"
        output = "Command timed out after 30s"
    except Exception as e:
        status = "⚠️ ERROR"
        output = str(e)
    
    results.append({
        "model": model,
        "status": status,
        "duration": f"{duration:.2f}s",
        "output": output[:100] + ("..." if len(output) > 100 else "")
    })

print("\n### Free Tier One-Shot Test Results\n")
print("| Model | Status | Time | Output/Error |")
print("|---|---|---|---|")
for r in results:
    print(f"| {r['model']} | {r['status']} | {r['duration']} | {r['output'].replace('\n', ' ')} |")
