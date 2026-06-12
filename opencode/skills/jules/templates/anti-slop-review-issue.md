{
  "schema_version": 1,
  "report_type": "slop",
  "repo_sha": "<commit-sha>",
  "review_scope": {
    "changed_files": [],
    "excluded_files": [],
    "required_surfaces": []
  },
  "findings": [
    {
      "tier": "tier1",
      "label": "SLOP",
      "category": "<category-name>",
      "location": {
        "path": "<file-path>",
        "start_line": 0,
        "end_line": 0
      },
      "pattern": "<pattern-name>",
      "task_narrative": "<what the user originally asked for>",
      "slop_narrative": "<how the agent produced this artifact instead>",
      "why_it_matters": "<how this mechanism lets bad work pass>",
      "user_surprise": "<cost to user vs cost to agent>",
      "existential_justification": "<why this code exists at all>",
      "failure_mode": "<failure-mode-name>",
      "evidence": [
        {
          "kind": "file-read",
          "path": "<file-path>",
          "lines": [1, 50]
        }
      ]
    }
  ],
  "checked_surfaces": [
    {
      "path": "<file-path>",
      "reason": "slop-scan",
      "lines_read": [1, 100],
      "result": "finding"
    }
  ],
  "score": 75,
  "report": "## Slop Audit Summary\n\n### Finding 1\n\n**Pattern:** <pattern-name>\n\n**Concrete evidence:** <evidence details>\n\n**Original requested task narrative:** <what was asked>\n\n**Descent into slop narrative:** <how it went wrong>\n\n**Why this matters:** <impact>\n\n**User surprise analysis:** <surprise factor>\n\n**Existential justification:** <why it exists>\n\n**Failure mode:** <mode-name>"
}
