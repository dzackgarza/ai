# PDF Extraction Development

This prompt applies to work in `/home/dzack/pdf-extraction`.

This repo is for developing and testing the PDF extraction workflow. Do not describe it as a globally canonical workflow yet.

## Current In-Repo Workflow

- Use the repo `justfile` and `uv` environment, not ad hoc CLI calls.
- The active MinerU supervisor is `scripts/run_mineru_batched.py`.
- The active worker is `scripts/run_mineru_batch_worker.py`.
- Use the opinionated recipes:
  `just extract-pdf`,
  `just launch-extract-pdf`,
  `just extract-status`,
  `just extract-progress`,
  `just extract-tail`,
  `just resume-extract`,
  `just extract-markdown-path`,
  `just extract-stop`.

## Long-Run Debugging Order

When asked why a long MinerU job did not finish, read the existing telemetry before searching for outside explanations.

Read in this order:

- `just extract-status <job_dir>` or `status.json` plus `manifest.json` for coarse state
- `events.jsonl` for the supervisor timeline and the terminal event
- the active batch `progress.jsonl` for timestamps, `processed_pages`, event-count growth, worker PID, RSS/VMS, CPU, and memory-pressure trends
- `worker.log` for the last observed MinerU stage such as `Layout Predict`, `MFD Predict`, or `MFR Predict`

Answer these questions first:

- Was the worker still making forward progress?
- What was the last completed or active MinerU stage?
- What did memory and swap look like near failure?
- Did the job die mid-batch or after a clean batch boundary?

## What Not To Do

- Do not burn tokens on "who sent SIGTERM" unless the telemetry story is exhausted or the user explicitly asks for signal provenance.
- Do not treat one surface as the whole story. `status.json` is coarse. `progress.jsonl` and `worker.log` carry the real run narrative.
- Do not call a job stalled only because `status.json` looks static. MinerU can spend a long time inside formula recognition while the worker remains active.

## Interpreting the Story

- If `progress.jsonl` keeps emitting heartbeats, CPU remains high, and `worker.log` is still advancing through MinerU stages, the job is not stalled.
- If swap is effectively full, available memory collapses, the worker dies mid-batch, and the supervisor records a termination, the likely story is memory pressure on the host. State that as an inference from telemetry.
- Prefer a short operational narrative over speculative root-cause hunting.

## Batch-Size Probing

- This is a coarse heuristic task, not an optimization problem.
- Use large-step bracketing to find a batch size that does not cripple the machine.
- Do not waste time micro-tuning nearby sizes when broad jumps answer the real question faster.
