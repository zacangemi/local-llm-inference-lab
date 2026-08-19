# Failures, invalid attempts, and what changed

Failure is separated into three categories:

- **Model failure:** the model received a valid test and did not satisfy it.
- **Harness-invalid attempt:** a prompt, isolation, modality, or runner defect made the attempt unusable for comparison.
- **Operational boundary:** the machine or backend exposed a real limit that belongs in the result.

## GPT-OSS-120B

- Early fit attempts with symmetric tensor splits ran out of VRAM because CPU-expert placement relieved the wrong GPU.
- The first Surf prompt accidentally specified a 2D medium; that attempt was invalidated and the corrected 3D prompt was frozen.
- The selected Surf app did not execute, and its capture files were placeholders.
- The Digital Twin was served from the wrong root, had unresolved module imports, and supplied placeholder captures.
- A diagnostic import repair revealed crude latent geometry. The scored result remains failed.

**Change:** prompts froze the intended medium; application acceptance began checking imports, browser state, and real capture dimensions.

## Laguna S 2.1

- Two Surf attempts were invalid because the model could see material outside the intended isolated workspace.
- The selected isolated Surf run produced a runnable canvas after extensive repair, but missed required handoff files and failed operator gameplay.
- The first Digital Twin attempt was invalid because generic image access exposed attachments to a text-only deployment.
- The valid text-only retry spent two full output-limited turns reasoning about coordinates and created no application.

**Change:** every long-agent workspace received its own private project root, and modality boundaries became explicit.

## Qwen3.6-27B-FP8

- The first agentic launches correctly failed admission because required server tool flags were absent.
- One failed MTP release left positively identified worker processes holding GPU memory after the API parent exited.
- Warm-start MTP at concurrency eight could trigger software thermal slowdown.
- The Surf app was substantial, but its alleged gameplay capture still showed the title state.
- The Digital Twin ran, but its capture automation did not wait for mode transitions; distinct hashes came from animation noise.

**Change:** process cleanup records the pre-launch set and terminates only new matching workers. Visual acceptance requires delayed state checks and content inspection.

## Step 3.7 Flash

- Combining MTP and vision failed deterministically at the post-image draft-position boundary. It was not an OOM or corrupt artifact.
- Digital Twin attempt one became invalid when automatic compaction replaced the assignment with a lossy summary.
- With compaction disabled, attempt two exceeded the 90K context.
- Attempt three reached the context ceiling and ended with broken relative imports, one blank capture, no README, and five missing captures.
- The Surf app entered gameplay but showed no convincing visible surfer or surfable wave.
- A minimal diagnostic import correction revealed the strongest latent Twin design. The submission still failed.

**Change:** terminal finish reasons became explicit, compaction became a controlled variable, and future visual tests will provide a known-good module scaffold.

## Shared lessons

1. Healthy inference is not product completion.
2. A model's final summary is untrusted evidence.
3. Non-empty or different images do not prove the requested state.
4. Context management is part of agent-system design.
5. Diagnostic repairs explain failures; they do not rewrite them.
6. Reruns are for invalid experiments, not disappointing outcomes.
