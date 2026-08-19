# Public shared prompts

These are the final prompt texts used for the four-model showcase.

- Hardware Exam and Horror Story were single-turn, answer-only tasks with tools disabled.
- Surf Simulator and Digital Twin were autonomous local build tasks with filesystem, shell, a pinned browser/runtime, no internet, and no subagents.
- Each model received a fresh session and isolated workspace.
- The Digital Twin prompt references a private evidence pack. That evidence pack is not published because it contains build and operational material beyond the public benchmark boundary.
- A prompt being public does not make the private run workspaces or raw telemetry public.

The files preserve the model-facing assignment. Harness-only paths, execution bindings, and raw run metadata are intentionally excluded.
