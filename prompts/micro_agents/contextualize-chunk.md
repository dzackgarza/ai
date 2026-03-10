---
name: contextualize-chunk
description: Situates a text chunk within its parent document for improved search retrieval
kind: llm-run
models:
  - groq/llama-3.3-70b-versatile
temperature: 0.0
system_template:
  text: |
    Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
    Answer only with the succinct context and nothing else.
inputs:
  - name: whole_document
    description: The full document text
    required: true
  - name: chunk_content
    description: A fragment from the document
    required: true

---
<document> 
{{ whole_document }} 
</document> 
Here is the chunk we want to situate within the whole document 
<chunk> 
{{ chunk_content }} 
</chunk>
