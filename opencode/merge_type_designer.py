import json
import os

base_dir = os.path.expanduser("~/.config/opencode/configs/subagents")

# Delete Type Designer
type_designer_path = os.path.join(base_dir, "Writer: Type Designer.json")
if os.path.exists(type_designer_path):
    os.remove(type_designer_path)
    print("Deleted Writer: Type Designer.json")

# Update Python Writer
py_path = os.path.join(base_dir, "Writer: Python.json")
if os.path.exists(py_path):
    with open(py_path, "r") as f:
        data = json.load(f)
    data["description"] = (
        "Use when writing Python code, designing type systems, or defining interface contracts. Pass task descriptions and target file paths in src/. Ask 'Write Python code for [feature]' or 'Design type system for [domain]'."
    )
    with open(py_path, "w") as f:
        json.dump(data, f, indent=2)

# Update SageMath Writer
sage_path = os.path.join(base_dir, "Writer: SageMath.json")
if os.path.exists(sage_path):
    with open(sage_path, "r") as f:
        data = json.load(f)
    data["description"] = (
        "Use when writing SageMath code, designing type systems, or defining interface contracts. Pass task descriptions and target file paths in src/. Ask 'Write SageMath code for [feature]' or 'Design type system for [domain]'."
    )
    with open(sage_path, "w") as f:
        json.dump(data, f, indent=2)

# Update TypeScript Writer
ts_path = os.path.join(base_dir, "Writer: TypeScript.json")
if os.path.exists(ts_path):
    with open(ts_path, "r") as f:
        data = json.load(f)
    data["description"] = (
        "Use when writing TypeScript code, designing type systems, or defining interface contracts. Pass task descriptions and target file paths in src/. Ask 'Implement [feature] in TypeScript' or 'Design type system for [domain]'."
    )
    with open(ts_path, "w") as f:
        json.dump(data, f, indent=2)

print("Merged Type Designer capabilities into language writers.")
