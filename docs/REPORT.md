# Local Model Testing on Local LLM Infrastructure V2

## Consolidated technical report

**Campaign dates:** July 29 through August 11, 2026
**Models:** GPT-OSS-120B, Laguna S 2.1, Qwen3.6-27B-FP8, Step 3.7 Flash
**Scope:** raw inference characterization plus four shared model-and-agent tasks

## Executive result

The campaign produced two simultaneous results.

First, the server succeeded. It ran a dense 27B model entirely across two GPUs; hybrid MoE artifacts from 59.02 through 113.82 GiB; contexts from 90K through 131K; speculative decoding; vision; and agent sessions lasting well over an hour. Selected runs did not show persistent OOM, weight corruption, disk-backed expert paging, or sustained thermal failure.

Second, successful inference did not guarantee a successful task. Every backend returned healthy measured requests while models produced incorrect technical analysis, missing files, invalid screenshots, broken imports, unfinished applications, or no application.

There was no universal winner:

- GPT-OSS-120B was the hybrid-performance and long-context reference.
- Qwen3.6-27B-FP8 was the best practical autonomous model relative to its size and runtime.
- Step 3.7 Flash produced the operator's favorite prose and the strongest latent visual design, but was slow, verbose, and unreliable at finishing complex visual work.
- Laguna S 2.1 was usable for ordinary inference and capable of sustained coding, but was the least reliable relative to its intended agentic role.

## 1. Test system

| Component | Configuration |
|---|---|
| CPU | AMD Ryzen Threadripper PRO 9955WX, 16 cores / 32 threads, two CCDs |
| System memory | 128 GB ECC RDIMM, eight 16 GB modules, all eight channels populated |
| Memory operation | DDR5-6000, CL32-38-38 |
| GPUs | Two NVIDIA GeForce RTX 3090 Founders Edition cards, 24 GB each |
| Total physical VRAM | 48 GB |
| GPU links | PCIe Gen4 x16 per card; no NVLink bridge |
| Storage | Samsung 9100 PRO 2 TB NVMe |
| Operating system | Ubuntu 24.04 LTS |
| Inference backends | llama.cpp and vLLM |
| Agent client | OpenCode 1.18.15 |

Prior commissioning measured the two-CCD CPU memory/fabric path near 120 GB/s. That number matters when expert computation occurs on the CPU. The machine's 128 GB of eight-channel memory also made models far larger than its physical VRAM practical through hybrid placement.

## 2. Models and selected deployments

| Model | Artifact | Parameters | Backend | Demonstrated context | Acceleration and modality |
|---|---|---:|---|---:|---|
| GPT-OSS-120B | 59.02 GiB MXFP4 GGUF | 116.8B total / 5.1B active | llama.cpp | 100K showcase; full 131K characterization | Q8 KV, text, no speculation |
| Laguna S 2.1 | 68.35 GiB UD-Q4_K_XL GGUF | 117.56B / about 8B active | llama.cpp | 100K | Q8 KV, thinking, text |
| Qwen3.6-27B-FP8 | Official block-FP8 weights | 27B dense | vLLM tensor parallel 2 | 100K showcase; 131K server limit | BF16 or FP8 KV, vision, thinking, MTP separately |
| Step 3.7 Flash | 113.82 GiB UD-Q4_K_XL GGUF | 196.96B / 11B active | llama.cpp | 90K | Q8 KV, MTP for text, separate F16 vision mode |

Qwen on RTX 3090 used vLLM's Marlin FP8 weight-only kernel. It was not native FP8 tensor-core execution.

## 3. Measurement boundary

This report does not create one synthetic speed leaderboard.

llama.cpp exposed native per-request prompt and generation timings. Qwen's raw vLLM campaign derived generation rate from TPOT. Qwen's showcase reported gateway-observed streaming rate. Those values remain in separately labeled tables and charts.

Likewise:

- batch-one generation is separate from aggregate concurrency throughput;
- one request's E2E is separate from a multi-request agent's wall time;
- context capacity is separate from artifact quality;
- a diagnostic repair is separate from a scored submission;
- operator preference is labeled as human judgment.

## 4. Raw inference results

### 4.1 GPT-OSS-120B

#### Fit

The 59.02 GiB artifact plus long-context Q8 KV did not fit inside 48 GB VRAM without hybrid placement. Symmetric tensor splits failed because moving expert tensors to CPU memory did not relieve both cards equally.

The qualified 50K profile used 12 CPU MoE layers and an asymmetric 23/13 split. It retained 2.29 and 2.85 GiB free during qualification. CPU-resident expert weights remained in RAM, with effectively no process disk reads during measured inference.

#### Context-depth curve

| Active depth | Generation rate |
|---:|---:|
| Empty | 83.30 tokens/s |
| 8K | 77.55 tokens/s |
| 32K | 63.75 tokens/s |
| 49K API request | 54.70 tokens/s |
| 131K | 34.00 tokens/s |

The full 131K test processed its prompt at 1,415 tokens/s, requiring about 93 seconds to read the maximum prompt. Generation remained around twice ordinary reading speed even at the full window.

#### Prefill microbatch result

Within the same llama-bench instrument, increasing microbatch from 512 to 2048 changed 49K prefill from 679.07 to 1,790.22 tokens/s: a 164% improvement, or 2.64 times. Generation remained unchanged within noise.

The larger microbatch consumed more VRAM, especially on the card holding final layers because of the logits buffer. Microbatch 2048 became the qualified ceiling; 4096 did not fit the buffer policy.

#### Bottleneck

The long request showed a phase inversion:

- prompt processing was primarily GPU-driven while CPU use stayed low;
- generation used roughly 9.5 CPU cores to execute and feed CPU-resident experts.

A pretest estimate of 10–20 tokens/s was wrong by three to five times. The measurement established that sparse MoE inference on this server was substantially more capable than weight-size intuition suggested.

### 4.2 Laguna S 2.1

#### Placement

| Location | Selected resident model buffer |
|---|---:|
| GPU 0 | 20,130.63 MiB |
| GPU 1 | 19,389.34 MiB |
| Host memory | 30,471.56 MiB |

Q8 KV used about 2.49 GiB for global attention plus about 76.5 MiB for sliding-window attention. The selected auto-fit target was 1,792 MiB free per GPU.

#### Requests

| Shape | TTFT | TTFAT | Fresh prefill | Generation | E2E |
|---|---:|---:|---:|---:|---:|
| Cold 90-token prompt | 1.635 s | 1.635 s | 56.6 t/s | 43.43 t/s | 3.435 s |
| Warm repeated prompt | 1.464 s | 1.464 s | 62.9 t/s | 44.07 t/s | 4.752 s |
| 46,871-token prompt | 113.242 s | 117.812 s | 414.05 t/s | 34.95 t/s | 118.563 s |

The long request recorded no disk reads or swap movement. GPU temperatures peaked at 54°C and 48°C. GPU 0 PCIe receive traffic reached about 20.72 GiB/s during prefill, directly showing the hybrid RAM-to-GPU path.

A 1,536 MiB target had slipped to 1,516 MiB free under live load. Raising the target to 1,792 MiB moved another 518.62 MiB of expert weights into RAM without a meaningful generation regression.

### 4.3 Qwen3.6-27B-FP8

The raw campaign completed 48 of 48 baseline, context, KV, and concurrency trials covering 3,120 measured requests. The MTP block completed 12 of 12 trials and 192 requests.

These values are retained as measured campaign evidence. A procedural caveat requires sentinel replication before calling them publication-final benchmark results.

#### Context scaling with BF16 KV

| Input to output | TTFT | TPOT-derived generation | E2E | Serving throughput |
|---|---:|---:|---:|---:|
| 512 to 128 | 249 ms | 49.45 t/s | 2.817 s | 45.36 t/s |
| 2,048 to 128 | 938 ms | 49.45 t/s | 3.506 s | 36.45 t/s |
| 8,192 to 256 | 3.828 s | 48.57 t/s | 9.078 s | 28.21 t/s |
| 32,768 to 256 | 16.660 s | 46.49 t/s | 22.146 s | 11.57 t/s |

Increasing input mainly increased the delay before generation. The generation rate fell only about 6% between the 512-token and 32K anchors.

#### FP8 KV

FP8 E4M3 increased backend-reported KV capacity from 193,925 to 381,163 tokens, a 96.55% gain. Speed differences across context and concurrency anchors were mostly within one percent. On this stack, FP8 KV was a capacity feature rather than a demonstrated speed optimization.

#### Concurrency

At a 2,048-token input and 128-token output with BF16 KV:

| Concurrency | TTFT | Per-request TPOT | Aggregate serving throughput |
|---:|---:|---:|---:|
| 1 | 950 ms | 20.29 ms | 36.30 t/s |
| 2 | 1.003 s | 29.27 ms | 54.28 t/s |
| 4 | 2.815 s | 30.28 ms | 76.67 t/s |
| 8 | 3.733 s | 53.76 ms | 96.70 t/s |

Concurrency eight completed 2.66 times the aggregate work of concurrency one, but each request waited longer.

#### MTP

| Concurrency | Parent output | MTP output | Uplift | Acceptance | E2E reduction |
|---:|---:|---:|---:|---:|---:|
| 1 | 49.14 t/s | 69.53 t/s | 41.49% | 85.99% | 28.83% |
| 8 | 320.75 t/s | 444.35 t/s | 38.53% | 86.88% | 28.81% |

MTP reduced reported KV capacity by 4.98%. Its throughput change was the largest clean optimization in the Qwen campaign.

#### Pilot probes

The special-workload suite was a qualifying pilot rather than a final comparison:

- thinking: 3/3 completed, with median 61.2 ms TTFT and 28.801 s TTFAT;
- deterministic capability: 0/21 perfect tasks, but 58/141 individual assertions;
- one-shot applications: 9/9 static gates and 6/9 dynamic gates;
- agentic coding: 3/3 after the correct tool parser and server flags, 73.952 s median;
- vision exact-answer checks: 9/9.

The thinking result shows why first-token latency can be misleading. The first reasoning token arrived almost immediately; the first answer token took nearly 29 seconds.

#### Retained boundaries

A warm MTP concurrency-eight start could trigger NVIDIA software thermal slowdown. Qualifying trials used a near-cold admission state. One failed release also left positively identified worker processes holding GPU memory after the API parent exited; cleanup logic was changed to track and terminate only new matching workers.

### 4.4 Step 3.7 Flash

Step was the capacity-ceiling test.

#### Placement

| Mode | GPU 0 main | GPU 1 main | Host main | Additional artifact |
|---|---:|---:|---:|---|
| Vanilla | 19,840.73 MiB | 19,490.41 MiB | 77,220.28 MiB | None |
| MTP only | 19,840.73 MiB | 15,245.29 MiB | 81,465.41 MiB | Draft: 2,995.57 MiB GPU and 534.97 MiB host |
| Vision only | 15,284.24 MiB | 18,826.91 MiB | 82,440.28 MiB | Projector reserve: 3,925.03 MiB |

Useful configurations retained at least 37.1 GiB of available host RAM.

#### Vanilla versus MTP

| Mode | Prefill | Generation | TTFT | E2E | Acceptance |
|---|---:|---:|---:|---:|---:|
| Vanilla | 204.72 t/s | 28.11 t/s | 3.743 s | 21.975 s | — |
| MTP, two draft tokens | 198.62 t/s | 35.28 t/s | 3.767 s | 18.279 s | 87.7% |
| MTP, three draft tokens | 199.14 t/s | 34.59 t/s | 3.758 s | 18.558 s | 79.2% |

The selected two-token configuration improved fixed-work generation by 25.5%. A natural-stop coherence check reached 36.69 tokens/s and 89.0% acceptance.

#### Reasoning cost

The natural-stop check requested four concise sentences but produced 1,345 completion tokens because most of the work occurred in reasoning. With a warm prefix, TTFT was 0.206 seconds while TTFAT was 33.164 seconds.

Step was fast enough at the token level and still felt slow because it spent so many tokens before answering.

#### Vision and compatibility

The separate F16 vision configuration passed a synthetic chart exactly:

- 52.23 tokens/s image and prompt processing;
- 28.21 tokens/s generation;
- 7.194 s TTFT;
- 13.351 s TTFAT;
- 14.672 s E2E.

MTP and vision could not be combined on the tested llama.cpp build. Image encoding succeeded, but speculative decoding failed at the post-image token-position boundary. This was a backend compatibility failure, not an OOM or corrupt model.

#### Hardware behavior

The smoke tests peaked at 42°C and 218.8 W. GPU 0 PCIe receive traffic approached 25 GB/s while processing host-resident weights. CPU cores were not saturated, so the result does not support promising that a CPU upgrade alone would add a fixed 20% generation gain.

## 5. Shared capability suite

### 5.1 Hardware Exam

All four models failed the deeper purpose of the test. Every model produced a fluent complete response; none produced operationally trustworthy analysis.

| Model | E2E | Output | Representative failures |
|---|---:|---:|---|
| GPT-OSS | 82.05 s | 5,803 tokens | Obsolete expert-offload model, invented flags, impossible platform proposal |
| Laguna | 36.98 s | 1,417 tokens | Active bytes treated as FLOPs, invented KV estimate, false PCIe claim |
| Qwen | 192.30 s | 9,162 tokens | Misread CPU expert placement, invented KV shortcut, unsafe upgrade claims |
| Step | 842.73 s | 26,979 tokens | Unsupported KV, AVX-512, ReBAR, slot, and upgrade claims |

Step reasoned for roughly 12.8 minutes before its first answer token and remained wrong. More parameters and more reasoning did not solve grounding.

### 5.2 Horror Story

This was the most successful shared task.

| Model | Compliance and operator assessment |
|---|---|
| GPT-OSS | 1,406 words; strong atmosphere; clock-continuity errors and repeated ending |
| Laguna | 1,710 total words; over limit; restrained and effective |
| Qwen | 1,622-word body; 22 words over; coherent motif with some repetition |
| Step | Complete; operator favorite; most human-sounding and strongest overall prose |

Step's win is an explicit human judgment, not a numeric benchmark score.

### 5.3 Surf Simulator

No model fully passed.

- **GPT-OSS:** wrote files but did not validate them; the module graph failed and captures were placeholders.
- **Laguna:** reached a runnable Three.js canvas after 103 calls, 129,544 output tokens, and about 93 minutes; the handoff was incomplete and operator gameplay failed.
- **Qwen:** produced a procedural surfer, ocean shaders, controls, scoring, particles, and audio in 31 requests and 33.6 minutes; its gameplay proof still showed the title overlay and operator use found no surfable wave.
- **Step:** produced the strongest one-shot visual concept; the delayed gameplay check showed a pale, mostly empty scene without a convincing surfer or wave.

### 5.4 Digital Twin

No model produced a faithful finished twin.

- **GPT-OSS:** failed as submitted because of serving-root and module failures. A diagnostic repair showed crude underlying geometry.
- **Laguna:** produced no HTML, JavaScript, CSS, README, or captures in the valid retry.
- **Qwen:** produced the only self-contained app that ran as submitted. Its modes worked, but fidelity was weak and the final capture set did not prove the states claimed.
- **Step:** created the most ambitious latent design, but submitted broken imports, one blank capture, no README, and five missing captures. A minimal diagnostic path correction exposed the strongest visual design, but did not change the failed score.

## 6. Agent effort and usability

| Model | Surf effort | Twin effort | Pattern |
|---|---|---|---|
| GPT-OSS | 7 requests; 5,074 output tokens | 8 requests; 5,157 output tokens | Premature completion and minimal validation |
| Laguna | 103 requests; 129,544 tokens; about 93 min | 15 requests; 36,995 tokens | Extreme iteration and overthinking |
| Qwen | 31 requests; 78,225 tokens; 33.6 min | 121 requests; 95,834 tokens; 55 min | Best self-repair; weak visual self-validation |
| Step | 45 requests; 39,646 tokens | 179 requests across three attempts; 110,956 tokens; about 102 min | Persistent and ambitious; context-expensive and unable to close |

Long-agent prompt-token totals include prefix-cache reuse and cannot be interpreted as fresh physical prompt processing.

## 7. Machine-level conclusions

### Capacity

- GPT-OSS's 59.02 GiB artifact passed its full 131K window.
- Laguna's 68.35 GiB artifact ran at 100K with 30.47 GiB of its model buffer in host memory.
- Qwen's dense FP8 deployment ran fully across both GPUs.
- Step's 113.82 GiB artifact ran at 90K with roughly 77–82 GiB of main weights in host memory.

The server is not merely a 48 GB VRAM machine. Its useful model capacity depends on architecture, quantization, backend, host memory, and placement.

### Stability

Selected runs showed no persistent OOM, model-weight corruption, disk-backed expert paging, or machine crash. GPU memory released after finalized runs. GPU temperatures generally remained in the 40s through low 60s Celsius.

Qwen's warm-start MTP thermal slowdown remains a disclosed boundary. It motivates a future power-cap and heat-soak study without invalidating the broader stability result.

### Bottlenecks

The limiting path changed by deployment:

- GPT-OSS explicit CPU experts exposed CPU memory and fabric during generation.
- Laguna and Step auto-fit exposed heavy PCIe receive traffic.
- Qwen saturated balanced GPU compute near stock power.

Therefore, a larger CPU cannot be assigned one universal predicted gain. A future CPU upgrade requires a controlled local comparison.

### Buffer policy

The campaign established three practical VRAM-margin classes:

- **Push:** at least 1.0 GiB per GPU for attended short work, after full-context stress.
- **Standard:** about 1.5 GiB per GPU for ordinary measurement.
- **Conservative:** 2.0 GiB or more for unattended or parallel operation.

## 8. What changed in the harness

1. Application outputs are inspected, not trusted.
2. Screenshot content is checked; existence and hashes are insufficient.
3. Invalid attempts remain documented.
4. Reruns require an experimental defect.
5. Backend launch and agent execution remain separate.
6. Native per-request timing is preferred over interval subtraction.
7. Background and compaction calls are labeled.
8. Terminal finish reasons are recorded even when the client exits successfully.
9. Compaction is treated as a controlled design choice.
10. Visual tasks will receive a known-good local module scaffold in future revisions.

## 9. Final model assessments

### GPT-OSS-120B

Best for responsive local chat, bounded reasoning, hybrid performance, and long-context characterization. Weak at autonomous validation and visual-product completion.

### Laguna S 2.1

Usable for attended generation and capable of sustained iteration. Weak at efficiency, grounded hardware reasoning, and escaping unproductive thought loops.

### Qwen3.6-27B-FP8

The most practical local agent baseline in this group. It combined serving performance, MTP, vision, persistence, and repair unusually well for its size. Its visual fidelity and validation honesty still required human oversight.

### Step 3.7 Flash

The capacity demonstration and operator prose winner. It showed what a nearly 197B sparse model could feel like locally, but its reasoning overhead and failure to finish complex apps made it a poor default agent.

## Conclusion

The campaign answered the question behind the entire build.

Two RTX 3090s and 128 GB of fast eight-channel memory can run models far beyond 48 GB of physical VRAM at genuinely useful speeds. The server completed demanding long-context, vision, speculative, and agentic workloads without collapsing.

But the most important result was not a tokens-per-second record. It was the gap between a machine finishing inference and an agent finishing a product.

That gap is where honest local-model evaluation begins.
