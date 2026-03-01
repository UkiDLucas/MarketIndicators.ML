# Lock-Free Handoff Protocol

## Goal
Allow ingestion, normalization, and prediction to run repeatedly without reader/writer lock contention.

## Protocol

1. Write-then-publish
- Writers generate outputs in temporary paths first.
- On completion, writer performs atomic rename (`os.replace`) to canonical path.

2. Immutable published artifacts
- Once published, a file is treated as immutable.
- Re-runs publish a new file version or replace atomically, never partial rewrite.

3. Reader discipline
- Readers consume only canonical published paths.
- Readers never open temp files.

4. Failure behavior
- If a stage fails, it must not replace canonical outputs.
- Partial temp files are safe to delete on next run.

5. Optional run partitioning (next step)
- Introduce `OUTPUT/runs/<RUN_ID>/...` for parallel execution.
- Publish `OUTPUT/latest.json` atomically to point to active run.

## Why this avoids locks
- Readers always see complete files.
- Writers never hold a long-lived lock on published files.
- Atomic rename provides point-in-time switch semantics.
