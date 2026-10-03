import re
import sys

def clean_html_code_blocks(text):
    # Regex to extract content from <div class="codehilite">...</div> blocks
    # Specifically looking for <pre><span></span><code>...</code></pre>
    
    # First, replace the specific nested structure with markdown code blocks
    pattern = r'<div class="codehilite">\s*<div class="codehilite">\s*<pre><span></span><code>(.*?)</code></pre>\s*</div>\s*</div>'
    
    def repl(match):
        code = match.group(1)
        # Remove all HTML spans
        code = re.sub(r'<span[^>]*>', '', code)
        code = re.sub(r'</span>', '', code)
        # Fix basic HTML entities
        code = code.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
        return '```lean\n' + code.strip() + '\n```'
        
    cleaned = re.sub(pattern, repl, text, flags=re.DOTALL)
    
    # Also clean up any generic codehilite blocks if they missed the specific structure
    pattern2 = r'<div class="codehilite">\s*<pre><span></span><code>(.*?)</code></pre>\s*</div>'
    cleaned = re.sub(pattern2, repl, cleaned, flags=re.DOTALL)
    
    # Fix the weird pandoc output if we parse that instead
    pattern_pandoc = r'<div class="codehilite">\s*<div class="codehilite">\s*(.*?)\s*</div>\s*</div>'
    def repl_pandoc(match):
        code = match.group(1)
        code = re.sub(r'<[^>]+>', '', code) # strip all html tags
        # Replace 4-space indents at the start of lines to avoid double indent
        code = re.sub(r'^    ', '', code, flags=re.MULTILINE)
        return '```lean\n' + code.strip() + '\n```'
    
    cleaned = re.sub(pattern_pandoc, repl_pandoc, cleaned, flags=re.DOTALL)
    
    # Remove any remaining raw HTML tags (like <a class="hover-link">, <span class="kbd">)
    cleaned = re.sub(r'<a[^>]*hover-link[^>]*>#</a>', '', cleaned)
    cleaned = re.sub(r'<span class="kbd">(.*?)</span>', r'`\1`', cleaned)
    
    return cleaned

with open('/home/dzack/ai/opencode/skills/lean4/skills/lean4/references/official-style-guide.md', 'r') as f:
    text = f.read()

text = clean_html_code_blocks(text)

with open('/home/dzack/ai/opencode/skills/lean4/skills/lean4/references/official-style-guide.md', 'w') as f:
    f.write(text)

print("Cleaned!")
