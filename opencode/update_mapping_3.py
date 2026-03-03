import os

base_dir = os.path.expanduser("~/.config/opencode")
manage_path = os.path.join(base_dir, "manage_permissions.py")

with open(manage_path, "r") as f:
    content = f.read()

old_mapping = """AGENT_MAPPING = {
    # Primary Agents
    "Minimal": "minimal",
    "Plan": "planning",
    "Build": "builder",
    "Interactive": "minimal",
    "Ralph Planner": "planning",
    "Repository Steward": "planning",
    "LatticeAgent": "minimal",
    "Zotero Librarian": "readonly",
    
    # Subagents - Writers
    "Writer: General Code": "src_writer",
    "Writer: Python": "src_writer",
    "Writer: TypeScript": "src_writer",
    "Writer: SageMath": "src_writer",
    "Writer: Tests": "test_writer",
    "Writer: Documentation": "src_writer",
    "Writer: Type Designer": "src_writer",
    "Writer: Refactorer": "src_writer",
    
    # Subagents - Reviewers
    "Reviewer: Code": "readonly",
    "Reviewer: Plans": "readonly",
    "Reviewer: Test Compliance": "readonly",
    "Reviewer: Semantic Audit": "readonly",
    "Reviewer: Plan Contract": "readonly",
    
    # Subagents - Researchers
    "Researcher: Code Base": "readonly",
    "Researcher: Documentation": "readonly",
    "Researcher: Repo Explorer": "readonly",
    
    # Subagents - Lattice
    "(Lattice) Researcher: Documentation": "readonly",
    "(Lattice) Reviewer: Documentation Librarian": "readonly",
    "(Lattice) Reviewer: Checklist Completionist": "readonly",
    "(Lattice) Reviewer: Test Coverage": "readonly",
    "(Lattice) Writer: Test Methods": "test_writer",
    "(Lattice) Writer: Interface Designer": "src_writer",
    "(Lattice) Writer: Interface Implementer": "src_writer",
    "(Lattice) Writer: TDD": "test_writer",
    "(Lattice) Writer: Algorithm Porter": "src_writer"
}"""

new_mapping = """AGENT_MAPPING = {
    # Primary Agents
    "Minimal": "minimal",
    "Plan": "planning",
    "Build": "builder",
    "Interactive": "minimal",
    "Ralph Planner": "planning",
    "Repository Steward": "planning",
    "(Lattice) Build": "builder",
    "Zotero Librarian": "readonly",
    
    # Subagents - Writers
    "Writer: General Code": "src_writer",
    "Writer: Python": "src_writer",
    "Writer: TypeScript": "src_writer",
    "Writer: SageMath": "src_writer",
    "Writer: Tests": "test_writer",
    "Writer: Documentation": "src_writer",
    "Writer: Refactorer": "src_writer",
    
    # Subagents - Reviewers
    "Reviewer: Code": "readonly",
    "Reviewer: Plans": "readonly",
    "Reviewer: Test Compliance": "readonly",
    "Reviewer: Semantic Audit": "readonly",
    "Reviewer: Plan Contract": "readonly",
    
    # Subagents - Researchers
    "Researcher: Code Base": "readonly",
    "Researcher: Documentation": "readonly",
    "Researcher: Repo Explorer": "readonly",
    
    # Subagents - Lattice
    "(Lattice) Researcher: Documentation": "readonly",
    "(Lattice) Reviewer: Documentation Librarian": "readonly",
    "(Lattice) Reviewer: Checklist Completionist": "readonly",
    "(Lattice) Reviewer: Test Coverage": "readonly",
    "(Lattice) Writer: Test Methods": "test_writer",
    "(Lattice) Writer: Interface Designer": "src_writer",
    "(Lattice) Writer: Interface Implementer": "src_writer",
    "(Lattice) Writer: TDD": "test_writer",
    "(Lattice) Writer: Algorithm Porter": "src_writer"
}"""

content_split = content.split("AGENT_MAPPING = {")
new_content = (
    content_split[0]
    + new_mapping
    + "\n\n"
    + "def apply_profiles():"
    + content.split("def apply_profiles():")[1]
)

with open(manage_path, "w") as f:
    f.write(new_content)

print("Updated mapping.")
