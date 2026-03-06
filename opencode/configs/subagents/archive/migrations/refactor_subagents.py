import os
import json

base_dir = os.path.expanduser("~/.config/opencode/configs/subagents")
prompts_dir = "/home/dzack/ai/prompts/subagents"
worker_prompts_dir = "/home/dzack/ai/prompts/worker_agents"

# Step 1: Deletions
to_delete = ["ops_engineer.json", "precedent-finder.json"]
for f in to_delete:
    p = os.path.join(base_dir, f)
    if os.path.exists(p):
        os.remove(p)

# Step 2: Renaming map
rename_map = {
    "general_code_writer.json": "Writer: General Source.json",
    "python_code_writer.json": "Writer: Python.json",
    "plan-reviewer.json": "Reviewer: Plans.json",
    "test-compliance-reviewer.json": "Reviewer: Test Compliance.json",
    "Semantic Auditor.json": "Reviewer: Semantic Audit.json",
    "codebase-explorer.json": "Researcher: Code Base.json",
    "Researcher.json": "Researcher: Documentation.json",
    "Repo Explorer.json": "Researcher: Repo Explorer.json",
    "plan-contract-validator.json": "Reviewer: Plan Contract.json",
    "project-initializer.json": "Writer: Project Initializer.json",
    "type_designer.json": "Writer: Type Designer.json",
    "Refactorer.json": "Writer: Refactorer.json",
    # Lattice ones
    "lattice_internet_researcher.json": "(Lattice) Internet Researcher.json",
    "lattice_documentation_librarian.json": "(Lattice) Documentation Librarian.json",
    "lattice_checklist_completionist.json": "(Lattice) Checklist Completionist.json",
    "lattice_test_coverage_auditor.json": "(Lattice) Test Coverage Auditor.json",
    "lattice_test_method_writer.json": "(Lattice) Test Method Writer.json",
    "lattice_interface_designer.json": "(Lattice) Interface Designer.json",
    "lattice_interface_implementer.json": "(Lattice) Interface Implementer.json",
    "lattice_tdd_writer.json": "(Lattice) TDD Writer.json",
    "lattice_algorithm_porter.json": "(Lattice) Algorithm Porter.json",
}

for old_name, new_name in rename_map.items():
    old_p = os.path.join(base_dir, old_name)
    new_p = os.path.join(base_dir, new_name)
    if os.path.exists(old_p):
        os.rename(old_p, new_p)

# Step 3: Merge Code Reviewer and Code Quality
cr_path = os.path.join(base_dir, "code-reviewer.json")
cq_path = os.path.join(base_dir, "Code Quality.json")
if os.path.exists(cr_path) and os.path.exists(cq_path):
    with open(cr_path, "r") as f:
        cr_data = json.load(f)
    with open(cq_path, "r") as f:
        cq_data = json.load(f)

    cr_data["description"] = (
        "Use when reviewing code post-implementation. Audits code against Clean Code standards, Design Patterns, correctness, and spec compliance. Flag non-substantive tests and suggest refactoring improvements."
    )

    with open(os.path.join(base_dir, "Reviewer: Code.json"), "w") as f:
        json.dump(cr_data, f, indent=2)

    os.remove(cr_path)
    os.remove(cq_path)

# Step 4: Merge Test Writer and Test Engineer
tw_path = os.path.join(base_dir, "test-writer.json")
te_path = os.path.join(base_dir, "test_engineer.json")
if os.path.exists(tw_path) and os.path.exists(te_path):
    with open(tw_path, "r") as f:
        tw_data = json.load(f)

    tw_data["description"] = (
        "Use when writing new tests following TDD or designing test strategies to improve existing coverage. Can write/edit tests in tests/ and test/ directories only."
    )

    with open(os.path.join(base_dir, "Writer: Tests.json"), "w") as f:
        json.dump(tw_data, f, indent=2)

    os.remove(tw_path)
    os.remove(te_path)

# Step 5: Create SageMath Writer from Python Writer
py_path = os.path.join(base_dir, "Writer: Python.json")
if os.path.exists(py_path):
    with open(py_path, "r") as f:
        py_data = json.load(f)

    py_data["description"] = (
        "Use when writing SageMath code. Pass SageMath task descriptions and target file paths in src/. Ask 'Write SageMath code for [feature]' or 'Implement [algorithm] in SageMath'."
    )
    # Update prompt path to a non-existent one that can be created later, or just fallback to python for now
    py_data["prompt"] = py_data["prompt"].replace(
        "python_code_writer.md", "sagemath_code_writer.md"
    )

    with open(os.path.join(base_dir, "Writer: SageMath.json"), "w") as f:
        json.dump(py_data, f, indent=2)

print("Subagents renamed and merged successfully.")
