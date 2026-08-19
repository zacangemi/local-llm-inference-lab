# Public data dictionary

All tables are redacted transcriptions from retained internal reports. Blank cells mean the source did not provide a directly comparable value; they are not zero.

## models.csv

One row per tested model and selected showcase deployment. Artifact size is left blank for Qwen because the exact installed byte total is not asserted by the publication source.

## raw-headlines.csv

A compact index of the major raw inference anchors. The instrument column is mandatory because llama.cpp native timing, vLLM TPOT-derived generation, and vLLM aggregate output are different measurement layers.

## gptoss-context.csv

Five context-depth anchors for GPT-OSS. The 49K row came from the native server timing object; other rows came from native llama-bench runs.

## qwen-context.csv

Median of three fresh-server trials for each input, output, and KV-cache condition. Status remains measured campaign evidence pending the disclosed sentinel replication.

## qwen-concurrency.csv

Concurrency scaling at 2,048 input and 128 output tokens. Serving throughput is aggregate request throughput and is not batch-one generation.

## qwen-kv-capacity.csv

Backend-reported capacity under BF16 and FP8 E4M3 KV. Capacity is not a promise that the full number is practically available after every other allocation.

## speculative-decoding.csv

Matched parent-versus-MTP comparisons. Qwen concurrency eight is aggregate output; Step is native fixed-work generation.

## placement.csv

Main-model buffers only. Additional draft/projector artifacts are described separately. Values use MiB as reported by the backend.

## showcase-summary.csv

Selected showcase requests and latency. Step Digital Twin combines multiple retained attempts, so request-level medians are intentionally blank rather than manufactured.

## capability-outcomes.csv

A deliberately small categorical matrix:

- pass: requested product or response met the essential contract;
- partial: substantial or runnable work existed, but important acceptance requirements failed;
- fail: technically unreliable response, non-running submission, or no deliverable.

## agent-effort.csv

Request counts, generated output tokens, and known wall time for the two build-agent tasks. Blank wall times were not promoted from rough inference.
