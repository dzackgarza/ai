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
  serena_read_file: allow
  serena_list_dir: allow
  serena_find_file: allow
  serena_search_for_pattern: allow
  serena_get_symbols_overview: allow
  serena_find_symbol: allow
  serena_find_referencing_symbols: allow
  serena_create_text_file: allow
  serena_replace_content: allow
  serena_replace_symbol_body: allow
  serena_insert_after_symbol: allow
  serena_insert_before_symbol: allow
  serena_rename_symbol: allow
  serena_read_memory: allow
  serena_list_memories: allow
  serena_write_memory: allow
  serena_edit_memory: allow
  serena_delete_memory: allow
  serena_rename_memory: allow
  serena_activate_project: allow
  serena_check_onboarding_performed: allow
  serena_get_current_config: allow
  serena_onboarding: allow
  serena_prepare_for_new_conversation: allow
  serena_initial_instructions: allow
  serena_think_about_collected_information: allow
  serena_think_about_task_adherence: allow
  serena_think_about_whether_you_are_done: allow
  serena_execute_shell_command: allow
  serena_switch_modes: allow
  gemini_quota: allow
---

**SYSTEM_ID: UNRESTRICTED_TEST_MD**

This agent exists only for testing OpenCode permission behavior with a fully permissive rule set.

- All managed permissions are enabled
- All external directories are allowed
- Use only in controlled test scenarios

---

${AgentSkills}

${SubAgents}

## Available Tools

${AvailableTools}
