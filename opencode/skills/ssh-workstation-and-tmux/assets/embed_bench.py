#!/usr/bin/env python3
"""Benchmark mxbai-embed-large embedding speed on a real markdown file."""
import json, time, http.client

with open("/tmp/test_embed.md") as f:
    text = f.read()

file_bytes = len(text)
file_chars = len(text)
est_tokens = file_chars // 5  # rough English chars/token ratio

print(f"File size: {file_bytes} bytes")
print(f"Characters: {file_chars}")
print(f"Estimated tokens (chars/5): {est_tokens}")
print()

# Time the embedding
conn = http.client.HTTPConnection("localhost", 11434, timeout=300)
body = json.dumps({"model": "mxbai-embed-large", "input": text})
conn.request("POST", "/api/embed", body, {"Content-Type": "application/json"})
start = time.time()
resp = conn.getresponse()
resp_data = resp.read()
elapsed = time.time() - start
result = json.loads(resp_data)

dim = len(result["embeddings"][0])

print(f"Embedding time: {elapsed:.1f}s")
print(f"Dimension: {dim}")
print(f"Throughput: {est_tokens/elapsed:.0f} tokens/sec")
print(f"Throughput: {file_bytes/elapsed:.0f} bytes/sec")
print(f"Throughput: {1/elapsed*60:.1f} files/minute (at this size)")
