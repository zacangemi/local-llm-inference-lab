# Methodology

## Two result layers

### Raw inference characterization

Each model received a deployment appropriate to its architecture and backend. Measurements covered fit, placement, context, TTFT, prefill, decode, MTP, concurrency, vision, thermals, RAM availability, paging, and release behavior.

This layer was not forced into one identical launch configuration. A dense 27B model that fits in VRAM and a 113.82 GiB sparse MoE require different placement strategies.

### Shared capability showcase

Every model received the same four task definitions:

1. Hardware Exam
2. Horror Story
3. 3D Surf Simulator
4. Digital Twin

Each task used a fresh agent session and isolated workspace. Answer-only tasks had tools disabled. Application tasks could use only the supplied local filesystem, shell, browser, and pinned runtime; internet access and subagents were prohibited. The backend restarted between cases so state did not cross task boundaries.

## Acceptance hierarchy

For every application task, three questions were kept separate:

1. Did the inference engine complete its requests?
2. Did the submitted deliverable run?
3. Did it satisfy the product and visual requirements?

An HTTP success answers only the first question. A model-authored completion claim, non-empty image, or different file hash is not sufficient acceptance evidence.

## Rerun policy

A rerun was allowed only when a demonstrated prompt, isolation, modality, or harness defect invalidated the attempt. A disappointing result was not grounds for rerunning until lucky. Invalid attempts remain in the private failure ledger and informed later harness changes.

Post-campaign repairs were diagnostic only. They distinguished an empty artifact from a packaging defect, but never changed a failed scored submission into a pass.

## Controls

- Model artifacts and backend builds were pinned within each campaign.
- Backend state restarted between showcase cases.
- Prompt definitions froze after demonstrated prompt defects were corrected.
- Fixed-work MTP comparisons used the same prompt and output budget.
- Qwen context, KV, and concurrency cells used three fresh-server trials per condition.
- Raw results, development failures, and selected attempts were retained privately.
- Performance, capability, and subjective quality were reported separately.

## Comparability limits

- llama.cpp native timings and vLLM gateway measurements are not placed in one unlabeled ranking.
- Aggregate concurrency throughput is not batch-one decode.
- Prompt-token totals in long agents include substantial prefix-cache reuse.
- Step and Qwen reasoning output makes wall time a distinct usability cost.
- Quantization, backend, modality, context, and placement differ by model and are disclosed.

## Qwen status caveat

The raw Qwen vLLM campaign completed 48/48 baseline, context, KV, and concurrency trials and 12/12 MTP trials. Internal review retained a clean-room process caveat: agents were resident during the raw campaign under the rule then in force. Values are published as measured campaign evidence, not described as publication-final benchmark results, until the planned sentinel replication closes that procedural gap.

Qwen's thinking, deterministic capability, one-shot application, agentic, and vision probes are separately labeled as a qualifying pilot.

## Public evidence model

The private corpus includes operational data that does not belong on the internet. This public export provides normalized CSV tables, consolidated interpretation, metric definitions, frozen prompt text, failure documentation, deterministic charts, and automated privacy validation.
