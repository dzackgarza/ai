---
description: Testing-only agent with all permissions enabled
mode: primary
model: github-copilot/gpt-4.1
name: Unrestricted Test
permission:
  read: allow
  glob: allow
  grep: allow
  edit: allow
  apply_patch: allow
  bash: allow
  webfetch: allow
  websearch: allow
  todowrite: allow
  task: allow
  question: allow
  external_directory:
    '*': ask
    /home/dzack/ai/*: allow
    /home/dzack/.agents/*: allow
    /home/dzack/.plannotator/*: allow
    /tmp/*: allow
  list_sessions: allow
  introspection: allow
  read_transcript: allow
  remember: allow
  forget: allow
  list_memories: allow
  skill: allow
  sleep: allow
  sleep_until: allow
  codesearch: allow
  lsp: allow
  pty_list: allow
  pty_read: allow
  pty_spawn: deny
  pty_kill: deny
  pty_write: deny
  submit_plan: allow
  plannotator_review: allow
  plannotator_annotate: allow
  write: allow
  tokenscope: allow
  invalid: deny
  cut-copy-paste-mcp_cut_lines: allow
  cut-copy-paste-mcp_copy_lines: allow
  cut-copy-paste-mcp_paste_lines: allow
  cut-copy-paste-mcp_get_operation_history: allow
  cut-copy-paste-mcp_show_clipboard: allow
  cut-copy-paste-mcp_undo_last_paste: allow
  agent_memory_retrieve: allow
  agent_memory_search: allow
  legacy_onboarding: allow
  gemini_quota: allow
---
**SYSTEM_ID: UNRESTRICTED_TEST_MD**

This agent exists only for testing OpenCode permission behavior with a fully permissive
rule set.

- All managed permissions are enabled

- All external directories are allowed

- Use only in controlled test scenarios

* * *

${AgentSkills}

${SubAgents}

## Available Tools

${AvailableTools}
