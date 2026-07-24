# Local LLM Inference Lab — Multi-Model Benchmarking with vLLM, llama.cpp & Agentic Workloads

> How far can 48 GB of VRAM go?

**Series:** Part 2 of 2 — Inference research and model evaluation

**Status:** 🧪 Research in Progress — Test design and data collection underway

## What this is

The research companion to [Local LLM Infrastructure V2](https://github.com/zacangemi/local-llm-infrastructure-v2). Part 1 builds and commissions the dual RTX 3090 Threadripper Pro AI server; Part 2 measures what it can actually do.

This project has two goals:

1. Validate the new machine under real local-AI workloads and characterize its limits.
2. Produce reproducible evidence about model, backend, and workload behavior instead of relying on one-off demos.

## What this project measures

- Prefill throughput, decode throughput, time to first token, and inter-token latency
- Context scaling, memory consumption, and KV-cache behavior
- GPU-only inference with vLLM
- Hybrid VRAM and system-RAM inference with llama.cpp
- Dense and mixture-of-experts model behavior
- Multimodal and vision workloads where supported
- Repeatable prompt suites and agentic workflows
- Stability, thermals, power, and failure behavior under sustained load

## Methodology commitments

- Pin model artifacts, checksums, backend versions, and launch configurations.
- Preserve raw evidence separately from derived tables and conclusions.
- Distinguish **measured**, **reported**, and **inferred** claims.
- Benchmark inference backends directly; UI traffic is not benchmark evidence.
- Use controlled prompts and workloads when comparing models.
- Publish unsuccessful experiments and limitations alongside successful results.

No performance claim is final until its run configuration and raw evidence are recorded.

## Planned repository structure

| Path | Purpose |
|---|---|
| methodology/ | Test protocol, workload definitions, and controls |
| configs/ | Reproducible vLLM and llama.cpp launch configurations |
| prompts/ | Shared prompt and agentic-workload suite |
| results/ | Raw and normalized measurements |
| analysis/ | Comparison tables, charts, and interpretation |
| docs/ | Decisions, limitations, and publication notes |

These directories will be added as the corresponding research phases begin.

## Part 1 — The machine

- 🖥️ **Build and infrastructure:** [zacangemi/local-llm-infrastructure-v2](https://github.com/zacangemi/local-llm-infrastructure-v2)
- 🌐 **Portfolio:** [zacharycangemi.com/portfolio.html](https://zacharycangemi.com/portfolio.html)
- 📚 **Writing:** [blog.zacharycangemi.com](https://blog.zacharycangemi.com)

---

*Part of [Project Arrival](https://zacharycangemi.com), my journey from Senior Data Scientist to AI Researcher.*
