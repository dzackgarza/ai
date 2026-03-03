import os
import json

base_dir = os.path.expanduser("~/.config/opencode/configs/subagents")

renames = {
    "Writer: General Source.json": "Writer: General Code.json",
    "Writer: Project Initializer.json": "Writer: Documentation.json",
    "(Lattice) Algorithm Porter.json": "(Lattice) Writer: Algorithm Porter.json",
    "(Lattice) Interface Designer.json": "(Lattice) Writer: Interface Designer.json",
    "(Lattice) Interface Implementer.json": "(Lattice) Writer: Interface Implementer.json",
    "(Lattice) TDD Writer.json": "(Lattice) Writer: TDD.json",
    "(Lattice) Test Method Writer.json": "(Lattice) Writer: Test Methods.json",
    "(Lattice) Internet Researcher.json": "(Lattice) Researcher: Documentation.json",
    "(Lattice) Checklist Completionist.json": "(Lattice) Reviewer: Checklist Completionist.json",
    "(Lattice) Documentation Librarian.json": "(Lattice) Reviewer: Documentation Librarian.json",
    "(Lattice) Test Coverage Auditor.json": "(Lattice) Reviewer: Test Coverage.json",
}

for old, new in renames.items():
    old_p = os.path.join(base_dir, old)
    new_p = os.path.join(base_dir, new)
    if os.path.exists(old_p):
        os.rename(old_p, new_p)

# Modify Writer: Documentation to be specifically about docs
docs_p = os.path.join(base_dir, "Writer: Documentation.json")
if os.path.exists(docs_p):
    with open(docs_p, "r") as f:
        data = json.load(f)
    data["description"] = (
        "Use when writing or updating documentation files. Ask 'Document the current project architecture' or 'Write a README for [feature]'."
    )
    with open(docs_p, "w") as f:
        json.dump(data, f, indent=2)

# Create Writer: TypeScript
ts_p = os.path.join(base_dir, "Writer: TypeScript.json")
gen_p = os.path.join(base_dir, "Writer: General Code.json")
if os.path.exists(gen_p):
    with open(gen_p, "r") as f:
        data = json.load(f)
    data["description"] = (
        "Use when writing TypeScript code. Pass task descriptions and target file paths in src/. Ask 'Implement [feature] in TypeScript'."
    )
    data["prompt"] = data.get("prompt", "").replace(
        "general_code_writer", "typescript_code_writer"
    )
    with open(ts_p, "w") as f:
        json.dump(data, f, indent=2)

print("Renaming and adjustments complete.")
