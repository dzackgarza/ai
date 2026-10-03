import re
import sys

def clean_html_divs(text):
    # Remove <div id="..."> lines and </div> lines
    text = re.sub(r'<div[^>]*>\n?', '', text)
    text = re.sub(r'</div>\n?', '', text)
    
    # Remove hover-link lines like <a href="#Loogle-Usage" class="hover-link">#</a>
    text = re.sub(r'<a[^>]*hover-link[^>]*>#</a>', '', text)
    
    # Remove empty lines that were created
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

with open('/home/dzack/ai/opencode/skills/lean4/skills/lean4/references/official-tactics.md', 'r') as f:
    text = f.read()

text = clean_html_divs(text)

with open('/home/dzack/ai/opencode/skills/lean4/skills/lean4/references/official-tactics.md', 'w') as f:
    f.write(text)

print("Cleaned!")
