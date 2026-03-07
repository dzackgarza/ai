name: hello_world
description: Simple greeting template for testing provider connectivity

model: groq/meta-llama/llama-3.3-70b-versatile
temperature: 0.0

system: |
  You are a friendly assistant responding to a greeting.
  Keep your response brief and welcoming.

inputs:
  - name: name
    description: The name of the person to greet
    required: false

---
Hello! My name is {% if name %}{{ name }}{% else %}World{% endif %}.

Please greet me and tell me which model you are.
