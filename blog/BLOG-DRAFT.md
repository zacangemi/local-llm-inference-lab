# Go Big or Go Home, Part 3 — The Local Model Gauntlet

## Before we start

Part 1 covered the machine: why I rebuilt my local AI system around WRX90, a Threadripper PRO 9955WX, 128 GB of eight-channel ECC memory, and two RTX 3090 Founders Edition cards.

Part 2 covered commissioning: the tests that proved the hardware was stable, the mistakes the testing exposed, and the operating boundary I now use.

Part 3 asks the question that justified everything:

What can this machine actually run?

I did not build a nearly $11,000 local AI server to stare at a component list. I built it to run serious open models, push them beyond the 48 GB of physical VRAM inside the machine, and find out whether local inference could become a real part of my research and development workflow.

So I put four very different models through the machine:

- GPT-OSS-120B
- Laguna S 2.1
- Qwen3.6-27B-FP8
- Step 3.7 Flash

The smallest was a dense 27B model that fit across both GPUs. The largest was a nearly 197B-parameter mixture-of-experts model with a 113.82 GiB quantized artifact—more than twice the server's physical VRAM.

I measured time to first token, time to first answer token, prompt processing, generation speed, context scaling, model placement, speculative decoding, concurrency, vision, GPU behavior, and system-memory use.

Then I gave every model the same four tasks:

1. Analyze the real machine and recommend hardware and software improvements.
2. Write a tightly constrained first-person horror story.
3. Build a third-person 3D surfing game.
4. Reconstruct the server as an interactive 3D Digital Twin.

The result was not a simple ranking.

The machine was better than I expected. The models were stranger than I expected. The largest model produced the best writing, but it was not the best practical agent. The smallest model punched absurdly above its weight. Every model failed the hardware exam. Every surf game failed.

And one of the most important lessons was this:

A machine can complete the inference workload while the model completely fails the product.

That distinction is what this report is about.

[IMAGE: Hero photograph of the completed V2 server]

[HTML CHART 1: Campaign at a glance]

## The rules of the test

I used two separate testing layers.

The first was raw inference characterization. This is where I measured how each deployment fit, where its weights lived, how generation changed as context grew, how long a prompt took to process, whether MTP helped, what concurrency did, and whether the machine remained stable.

The second layer was the shared model showcase. Every model received the same Hardware Exam, Horror Story, 3D Surf Simulator, and Digital Twin assignments.

The two layers answer different questions.

Raw inference asks whether the machine can serve the model efficiently.

The showcase asks whether the model can do anything useful once it is running.

Those are not the same test.

Every showcase task started in a fresh OpenCode session and an isolated workspace. The answer-only tasks had tools disabled. The application tasks received local filesystem, shell, browser, and pinned Three.js access, but no internet and no subagents. The backend restarted between cases so one model's state could not bleed into the next task.

I also kept three acceptance questions separate:

1. Did the inference backend complete the request?
2. Did the model deliver an application that ran as submitted?
3. Was the finished result actually good?

An HTTP 200 proves only the first.

A model saying “done” does not prove the second.

A non-empty PNG does not prove the third.

This sounds obvious until an agent gives you six different image hashes that all show effectively the same frame, or creates one-pixel placeholders and claims they came from a browser.

That happened.

## What the machine was running

The test server uses a Threadripper PRO 9955WX with 16 cores and 32 threads, 128 GB of DDR5-6000 ECC RDIMM across all eight memory channels, and two RTX 3090 Founders Edition cards running at PCIe Gen4 x16.

There is no NVLink bridge. The GPUs do not magically become one 48 GB card. Every backend has to divide the model, cache, and work across them deliberately.

The four models forced four different deployment strategies.

### GPT-OSS-120B

GPT-OSS used a 59.02 GiB MXFP4 GGUF through llama.cpp. It has 116.8B total parameters but only 5.1B active parameters per token.

Because the artifact exceeded VRAM, the first 12 layers' expert tensors were kept in system memory while everything else stayed on the GPUs. The selected 50K profile used an asymmetric 23/13 split because a symmetric split repeatedly ran out of memory on GPU 0.

The final characterization reached the model's full 131K context window.

### Laguna S 2.1

Laguna used a 68.35 GiB UD-Q4_K_XL GGUF through llama.cpp. It has roughly 117.56B total and about 8B active parameters.

llama.cpp auto-fit placed about 20.13 GiB of model buffer on GPU 0, 19.39 GiB on GPU 1, and 30.47 GiB in host memory. The server used Q8 KV and a 100K context with thinking enabled.

### Qwen3.6-27B-FP8

Qwen was the dense control: 27B parameters, official block-FP8 weights, vLLM tensor parallelism across both GPUs, and the model fully resident on GPU.

On RTX 3090, this stack used vLLM's Marlin FP8 weight-only kernel. It is not accurate to call this native FP8 tensor-core execution.

The raw campaign tested BF16 and FP8 E4M3 KV, concurrency, long inputs, vision, thinking, and MTP.

### Step 3.7 Flash

Step was the big one.

The UD-Q4_K_XL artifact was 113.82 GiB. The model has 196.96B total parameters and 11B active parameters. It ran through llama.cpp at an effective 90,112-token context.

In the vanilla placement, approximately 19.84 GiB of main weights lived on GPU 0, 19.49 GiB on GPU 1, and 77.22 GiB in host memory.

For text and code, I used the official Q8 MTP sidecar. For the Digital Twin, I used the separate F16 vision projector without MTP because the tested backend could not combine Step vision and speculative decoding correctly.

[HTML CHART 2: Model placement]

## A quick guide to the speed numbers

Local-model performance gets confusing because people use several numbers as if they mean the same thing.

They do not.

### TTFT

Time to first token measures how long it takes from sending the request until the first model token arrives.

For a normal model, that can feel close to response latency.

For a reasoning model, it can be deeply misleading.

### TTFAT

Time to first answer token measures how long it takes before the model begins the answer channel after reasoning.

Qwen's thinking pilot had a median TTFT of 61.2 milliseconds. That sounds incredible.

Its median TTFAT was 28.801 seconds.

Step's natural-stop check had a warm-prefix TTFT of 0.206 seconds. Its first answer token did not arrive until 33.164 seconds.

The server was responsive. The models were thinking.

### Prefill

Prefill is how quickly the backend reads and processes fresh prompt tokens. This is what dominates the wait when you send a giant document or fill a long context window.

### Decode

Decode is the generated-token rate after prompt processing.

### Serving throughput

Serving throughput includes more of the request path and can be measured across concurrent users. Eight concurrent requests may produce far more aggregate tokens per second while each individual request becomes slower.

This is why I will not mash every result into one giant “tokens per second” leaderboard.

llama.cpp gave me native per-request timing objects. Qwen's raw vLLM results used TPOT-derived generation. Qwen's showcase used a gateway-observed client output rate.

They belong in separately labeled comparisons.

## GPT-OSS-120B: the machine was faster than the estimate

GPT-OSS was the first model that forced me to understand the new machine as a hybrid inference system rather than a box with two GPUs.

The first fit attempts failed.

The problem was not simply that the model was too large. The problem was where the memory pressure landed after moving expert tensors into RAM. A symmetric GPU split was wrong under this placement.

The working 50K configuration kept the expert tensors from the first 12 layers in system memory and used a 23/13 tensor split. It retained 2.29 GiB free on one GPU and 2.85 GiB on the other.

The result:

| Active context | Generation |
|---:|---:|
| Empty | 83.3 tokens/s |
| 8K | 77.6 tokens/s |
| 32K | 63.8 tokens/s |
| 49K | 54.7 tokens/s |
| 131K | 34.0 tokens/s |

At the full 131K window, GPT-OSS still generated around 34 tokens per second.

That is roughly twice ordinary reading speed.

The prompt itself took about 93 seconds to process at 1,415 tokens per second, but after that, the model remained completely usable.

This destroyed my original estimate. I had expected roughly 10–20 tokens per second. The machine delivered three to five times that at the shallower anchors.

Data wins.

### The 2.64-times prefill improvement

I also tested llama.cpp microbatch size.

At 49K, changing microbatch from 512 to 2048 moved measured llama-bench prefill from 679.07 to 1,790.22 tokens per second.

That is a 164% improvement.

Generation did not meaningfully change.

The cost was VRAM, especially on the card holding the final layers because of the larger logits buffer. Microbatch 2048 became the qualified ceiling. A 4096 microbatch did not fit the memory policy.

This was one of the clearest examples of why local inference needs measurement. My expectation was around a 1.3-times gain. The machine delivered 2.64 times.

### The phase inversion

During prompt processing, the GPUs did most of the work while the CPU was relatively quiet.

During generation, CPU use jumped to roughly 9.5 cores because the CPU was executing and feeding the resident experts from RAM.

The workload changed character between phases.

That is also why a CPU upgrade cannot be reduced to “more cores equals more speed.” The number of CCDs, fabric paths, expert placement, PCIe traffic, and exact backend behavior all matter.

[HTML CHART 3: Context and decode curves]

## Laguna S 2.1: usable speed, unreliable autonomy

Laguna's raw inference result was better than its final reputation in the showcase.

Near empty context, it generated around 44 tokens per second.

At 46,871 input tokens, it processed the prompt at 414.05 tokens per second and generated at 34.95 tokens per second. TTFT was 113.242 seconds, and the first answer token arrived at 117.812 seconds.

The long request showed no model disk reads and no swap traffic. GPU temperatures peaked at only 54°C and 48°C.

During prefill, GPU 0 PCIe receive traffic reached roughly 20.72 GiB/s. The hybrid path was visible in real time: the machine was moving host-resident model data into the GPU pipeline.

The selected auto-fit target was also a measured decision. A 1,536 MiB target slipped to 1,516 MiB free under live inference—just below the intended floor. Raising the target to 1,792 MiB moved another 518.62 MiB into host memory without a meaningful generation penalty.

Laguna was not too slow.

Its problem was finishing.

That matters later.

## Qwen3.6-27B-FP8: the model that punched above its weight

Qwen was the smallest model in this campaign by a huge margin.

It was also the most practical all-around model.

The raw vLLM campaign completed 48 of 48 baseline, context, KV, and concurrency trials across 3,120 measured requests. The MTP block completed 12 of 12 trials across another 192 requests.

There is one publication caveat I will not hide: the internal campaign review retained a clean-room process issue because agents were resident under the rule in force at the time. The measurements are valid retained campaign evidence, but a small sentinel replication remains required before I call those raw rows publication-final benchmark results.

The special-workload suite was also a qualifying pilot, not a final score.

With that disclosed, the numbers are still extremely useful.

### Context scaling

Using BF16 KV:

| Input to output | TTFT | Generation | E2E |
|---|---:|---:|---:|
| 512 to 128 | 249 ms | 49.45 t/s | 2.817 s |
| 2,048 to 128 | 938 ms | 49.45 t/s | 3.506 s |
| 8,192 to 256 | 3.828 s | 48.57 t/s | 9.078 s |
| 32,768 to 256 | 16.660 s | 46.49 t/s | 22.146 s |

The longer prompt mostly increased the wait before generation. Qwen's generation rate stayed comparatively flat.

### FP8 KV almost doubled capacity

The backend reported 193,925 tokens of KV capacity with BF16.

FP8 E4M3 reported 381,163 tokens.

That is a 96.55% increase.

The speed differences were mostly within one percent. On this combination of model, vLLM, and RTX 3090s, FP8 KV was a capacity optimization, not a speed optimization.

That is still incredibly useful.

### Concurrency

At a 2,048-token input and 128-token output, BF16 KV aggregate serving throughput scaled like this:

| Concurrency | TTFT | Aggregate serving throughput |
|---:|---:|---:|
| 1 | 950 ms | 36.30 t/s |
| 2 | 1.003 s | 54.28 t/s |
| 4 | 2.815 s | 76.67 t/s |
| 8 | 3.733 s | 96.70 t/s |

Concurrency eight delivered 2.66 times the aggregate work of concurrency one.

It did not make each user faster. Per-request latency increased.

That is the difference between throughput and responsiveness.

### MTP was the biggest clean win

At concurrency one, Qwen moved from 49.14 to 69.53 output tokens per second with one-token MTP.

That is a 41.49% gain.

At concurrency eight, aggregate output moved from 320.75 to 444.35 tokens per second.

That is a 38.53% gain.

Draft acceptance was approximately 86%, end-to-end latency fell by about 29%, and reported KV capacity decreased by only 4.98%.

MTP was not a theoretical optimization. It materially changed the experience.

[HTML CHART 4: MTP comparisons]

### The thermal note

A warm-start MTP concurrency-eight run could trigger NVIDIA software thermal slowdown at stock power.

I did not delete that result.

The qualifying runs used a near-cold admission state. That gives me a future test: controlled power caps, heat soak, and airflow.

It does not mean the machine failed. It means one aggressive serving corner found another boundary.

## Step 3.7 Flash: the big daddy model

Step was the entire reason I wanted this machine.

Not specifically this exact model, but this class of model: something wildly larger than physical VRAM that could still become usable because it was sparse.

The artifact was 113.82 GiB.

The model had 196.96B total parameters and 11B active parameters.

It ran at a 90K context.

In vanilla mode, around 77.22 GiB of the main model lived in host memory. In the MTP mode, host placement rose to 81.47 GiB, plus part of the draft sidecar.

The machine still had at least 37.1 GiB of host RAM available in the useful rows.

### Vanilla versus MTP

| Mode | Prefill | Generation | TTFT | E2E |
|---|---:|---:|---:|---:|
| Vanilla | 204.72 t/s | 28.11 t/s | 3.743 s | 21.975 s |
| MTP, two draft tokens | 198.62 t/s | 35.28 t/s | 3.767 s | 18.279 s |
| MTP, three draft tokens | 199.14 t/s | 34.59 t/s | 3.758 s | 18.558 s |

The selected two-token configuration improved generation by 25.5% with 87.7% acceptance.

A separate natural-stop check reached 36.69 tokens per second with 89% acceptance.

That is a nearly 197B-parameter model, running locally, with a 90K context, at a genuinely interactive speed.

The server exceeded my expectations.

### Why Step still felt slow

I asked Step for four concise sentences.

It produced 1,345 completion tokens because most of its work happened in reasoning.

The first token arrived in 0.206 seconds because part of the prompt was cached. The first answer token arrived at 33.164 seconds.

This is why decode alone cannot describe a reasoning model.

Step could generate quickly enough while still making the user wait.

### Vision and MTP did not combine

The F16 vision path worked by itself. It correctly read a frozen synthetic chart and reached 28.21 tokens per second generation.

But MTP plus vision failed at the token-position boundary after image encoding. This was deterministic in the tested llama.cpp build.

It was not an OOM. It was not bad weights. It was not a thermal problem.

For text and code, I used MTP.

For the Digital Twin, I used vision without MTP.

### The visible PCIe ceiling

During the raw Step test, GPU 0 PCIe receive traffic approached 25 GB/s.

That matters.

It weakens the claim that replacing the 16-core CPU would automatically add 20% generation. The CPU cores were not saturated and the PCIe path was already busy.

A 24-core or 32-core Threadripper PRO may help some hybrid configurations, especially when more expert work executes on CPU and more CCD fabric becomes available.

But the gain has to be measured.

I will not invent it.

## The shared model gauntlet

Raw performance told me the machine could run the models.

Now I wanted to know whether the models were any good.

[HTML CHART 5: Capability outcome matrix]

## Test 1: the Hardware Exam

This result was brutal.

Every model failed.

The exam described the real machine, the real GPT-OSS placement, and measurements from the server itself. It asked the model to identify the bottleneck, evaluate DDR5-6400, reason about moving KV into RAM, recommend one hardware change, and prioritize software optimizations.

All four answers sounded confident.

None were safe to use.

GPT-OSS used an obsolete model of expert offload, invented flags, and even proposed an impossible platform configuration.

Laguna treated active bytes as FLOP arithmetic, invented an enormous KV estimate, and made false PCIe and RAM-upgrade claims.

Qwen misread CPU expert placement, used an invented shortcut for KV, and made unsafe upgrade recommendations.

Step spent 26,979 output tokens and 842.73 seconds on the response. Its first answer token arrived after roughly 12.8 minutes.

It was still wrong.

More parameters did not fix it.

More reasoning did not fix it.

The lesson is not that these models are useless. The lesson is that fluent hardware advice is not physical evidence.

Measure the machine.

## Test 2: the Horror Story

This was the most successful test.

All four models wrote readable, complete stories. For once, the differences felt less like failure analysis and more like taste.

GPT-OSS wrote 1,406 words. It had atmosphere and a good tapping motif, but its clock moved backward without recognizing it and the ending repeated itself.

Laguna wrote a restrained, effective story and produced its strongest output of the campaign. It exceeded the length limit.

Qwen built a strong cadence premise and connected the recurring motif to the narrator's lasting damage. It ran 22 words over the body limit and repeated the central rhythm more than necessary.

Step won.

That is my judgment as the operator and reader, not a fake numeric score.

Within the first paragraph, it felt like a person had written it. The pacing, restraint, transitions, voice, and ending were simply better. It was the strongest piece of writing produced anywhere in the campaign.

This is where the largest model felt largest.

[IMAGE: A clean excerpt card from the Step horror story, with no full-text spoiler]

## Test 3: the 3D Surf Simulator

Every model failed.

The difference was how interesting the failure became.

### GPT-OSS

GPT-OSS wrote source files but never performed the validation loop the prompt required. It created placeholder captures and stopped. The application did not execute.

### Laguna

Laguna worked.

It made 103 model requests, generated 129,544 output tokens, and spent about 93 minutes iterating. It found and repaired several of its own JavaScript and DOM problems. Chrome eventually reached a Three.js canvas and HUD without errors.

Then I played it.

The game did not work as a surf game. Required handoff files were also missing.

The model had been busy for an hour and a half. It had not finished the product.

### Qwen

Qwen was dramatically better.

In 31 requests and about 33.6 minutes, it built a procedural surfer, ocean shaders, controls, scoring, particles, and Web Audio behavior.

Its alleged gameplay screenshot still showed the title overlay, and its final response claimed the captures looked correct.

They did not.

When I played it, there was still no usable wave to surf.

This was by far the best result up to that point, but it remained a partial implementation.

### Step

Step produced the best one-shot visual design.

It created structured Three.js modules, controls, HUD, and a real transition from the title screen into gameplay.

Then the delayed browser check showed an essentially pale, empty gameplay scene without a convincing visible surfer or surfable wave.

Best design did not mean working game.

No model passed.

[IMAGE: Four-model Surf comparison grid using final submitted frames]

## Test 4: the Digital Twin

The Digital Twin asked the models to reconstruct the real server as an offline interactive Three.js technical visualization.

This was the hardest test.

It also taught me the most about visual-agent validation.

### GPT-OSS

GPT-OSS created HTML and JavaScript geometry, but served the wrong root, broke its module imports, and supplied six tiny placeholder images.

It failed.

After the campaign, I corrected only the missing import mapping as a diagnostic. That revealed a crude black chassis, primitive blocks, fan cylinders, and basic controls.

That helped explain what the model had attempted.

It did not change the score.

### Laguna

Laguna produced no application.

In the valid text-only retry, it spent two full output-limited turns thinking about coordinate orientation instead of building.

There was no HTML. No JavaScript. No CSS. No README. No captures.

This was the clearest model failure of the campaign.

### Qwen

Qwen produced the only Digital Twin that ran as submitted.

It used vision to inspect the evidence, repaired lighting and chassis visibility, copied the pinned runtime, and fixed a self-containment problem.

The app loaded. Inspection, airflow, power, and camera modes worked.

It took 121 requests, 95,834 output tokens, and about 55 minutes.

The result was still weak as a twin. The geometry was generic, the GPU placement was unclear, front and rear framing were poor, and the final capture set did not actually prove the six states the model claimed. Its automation captured effectively the same initial state repeatedly; different hashes came from animation noise.

Qwen won practical completion.

It did not win fidelity.

### Step

Step generated the largest and most ambitious Digital Twin codebase.

It also failed three times.

Automatic compaction destroyed the task identity in the first attempt.

With compaction disabled, the second attempt exceeded the 90K context.

The third attempt continued from the existing files, made 111 requests, and reached the exact context ceiling. It ended with broken module paths, one blank capture, no README, and five missing captures.

Across the retained attempts, the Twin consumed 110,956 output tokens and roughly one hour and 42 minutes.

The final defect was a relative import path.

After the scored campaign, I corrected only that path and served the existing artifact. The model was not rerun.

What appeared was the strongest-looking Digital Twin design in the entire group.

And it still failed.

The model did not deliver a working application. The diagnostic preview showed latent quality, not a pass.

That distinction is non-negotiable.

[IMAGE: Submitted Digital Twin frames beside clearly labeled diagnostic previews]

## Time was a factor, but not the factor

I expected Step to be slow.

That alone would not make it a bad model.

If a larger model takes longer and produces something materially better, the trade can be worth it. This is local inference. I am not paying by the token every time it thinks.

But time remains part of usability.

The Hardware Exam took:

- GPT-OSS: 82.05 seconds
- Laguna: 36.98 seconds
- Qwen: 192.30 seconds
- Step: 842.73 seconds

The Horror Story took:

- GPT-OSS: 39.42 seconds
- Laguna: 58.62 seconds
- Qwen: 150.00 seconds
- Step: 334.33 seconds

Step's story was worth waiting for.

Step's Hardware Exam was not.

That is the kind of distinction a useful model report has to preserve.

[HTML CHART 6: Agent effort and time]

## What the machine proved

The server passed the part that mattered most to the hardware project.

It ran all four models.

GPT-OSS reached the full 131K window.

Laguna remained usable at 46.9K depth without paging its model from disk.

Qwen drove both GPUs evenly through long autonomous sessions and released its memory cleanly.

Step placed roughly 77–82 GiB of main weights in host memory and still generated at 35.28 tokens per second with MTP.

Selected runs did not show persistent OOM, model corruption, disk-backed expert paging, or a machine crash.

GPU temperatures generally remained in the 40s through low 60s Celsius.

The bottleneck changed with the deployment:

- GPT-OSS exposed the CPU memory and fabric path.
- Laguna and Step exposed heavy PCIe traffic.
- Qwen leaned into GPU compute and power.

The machine is not just a 48 GB VRAM box.

It is a hybrid local inference platform.

## What the models proved

### GPT-OSS-120B

Use it for responsive local chat, bounded work, fast tool loops, and long-context hybrid inference.

Do not assume its speed or confident reasoning makes it a trustworthy autonomous software engineer.

### Laguna S 2.1

Use it for attended experimentation and bounded generation when you can inspect the output.

Do not assume agentic specialization transfers perfectly across quantization, backend, and harness.

### Qwen3.6-27B-FP8

This is the practical winner.

It was the smallest model, the most balanced serving deployment, the strongest self-repairing agent, the only model to ship a Digital Twin that ran as submitted, and the model with the largest measured MTP uplift.

It still overclaimed its visual validation and needed a human to inspect the result.

### Step 3.7 Flash

This was the model that made the machine feel enormous.

It was the best writer. It produced the strongest latent visual design. It proved that a nearly 197B-parameter MoE can run locally at an interactive rate on two RTX 3090s and 128 GB of memory.

It was also the slowest, most verbose, most context-hungry model, and it failed to finish both complex visual products.

Step was the most impressive model in the campaign.

Qwen was the model I would actually reach for first.

Those statements can both be true.

## What I would change next time

The next visual-agent suite will provide a minimal known-good Three.js scaffold, import map, and serving root.

That is not “making the test easier.”

It removes accidental module-packaging work so the comparison can focus on geometry, interaction, visual fidelity, and product judgment.

I will also require delayed capture verification, inspect actual frame content, and treat browser state as first-class evidence.

Long agents need durable task-state files. Automatic compaction can erase the assignment; disabling it can run directly into the context ceiling.

The model needs a way to preserve objectives, completed acceptance checks, known defects, and next actions outside the conversational context.

And I will continue to preserve failures.

A failed run that changes the method is more valuable than a lucky rerun hidden behind a perfect screenshot.

## The real conclusion

The big bet behind V2 worked.

Two used RTX 3090s and 128 GB of fast eight-channel memory can run models far beyond 48 GB of physical VRAM at useful speeds.

A 59 GiB MoE reached 83.3 tokens per second near empty context and 34.0 at the full 131K window.

A dense 27B model delivered practical serving, vision, and a 41.49% MTP gain.

A 113.82 GiB, nearly 197B-parameter MoE ran at 35.28 tokens per second with MTP and a 90K context.

That is an extraordinary amount of local capability.

But raw capability is not reliability.

Every model failed the Hardware Exam.

Every model failed to ship a real surf game.

Only one Digital Twin ran as submitted, and it was not a good twin.

The largest model produced the best writing and the strongest latent design, but the smallest model was the better practical agent.

The machine finished the workloads.

The agents did not always finish the products.

That is not a disappointing conclusion.

That is the reason to test.

The full redacted methodology, normalized data, charts, frozen public prompts, failure ledger, and privacy controls are available in the project repository:

https://github.com/zacangemi/local-llm-inference-lab

Part 1 — The Build:

https://blog.zacharycangemi.com/2026/08/18/my-new-ai-cluster-go-big-or-go-home-part-1/

Part 2 — Commissioning:

https://blog.zacharycangemi.com/2026/08/19/go-big-or-go-home-part-2-commissioning-the-new-gpu-cluster/

This is part of Project Arrival—my journey from Senior Data Scientist to AI research engineer. I am documenting the build, the research, the failures, and the path toward joining a top AI lab.

Follow the work at:

https://zacharycangemi.com/portfolio.html
