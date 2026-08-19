# Metric definitions

The campaign separates latency, throughput, capacity, and product quality. They describe different parts of the experience.

| Metric | Meaning | Common misuse |
|---|---|---|
| TTFT | Time from request dispatch to the first streamed model token | Treating it as time to a visible answer when reasoning is separate |
| TTFAT | Time to the first answer-channel token after reasoning | Ignoring the reasoning wait and reporting only TTFT |
| Prefill | Rate at which fresh prompt tokens are evaluated | Comparing short synthetic prefill directly with long server prefill |
| Decode | Generated-token rate after prompt processing | Mixing native engine timing with client-observed streaming rate |
| TPOT | Average time per output token; raw Qwen decode uses 1000 / TPOT | Reading speculative chunks as ordinary one-token intervals |
| ITL | Inter-token latency observed in the stream | Treating a multi-token speculative chunk as one token |
| E2E | Request dispatch through terminal completion | Confusing one request with a multi-request agent's wall time |
| Serving throughput | Output delivered per second including request and prefill overhead | Calling concurrent aggregate throughput batch-one decode |
| Context depth | Tokens already active when generation is measured | Treating configured context as demonstrated used context |
| KV capacity | Backend-reported cache capacity under a configuration | Assuming it equals practical context after all allocations |
| Draft acceptance | Accepted speculative tokens divided by proposed draft tokens | Assuming acceptance predicts application quality |

## Instrument boundary

llama.cpp exposed native prompt and decode timing objects. Qwen's raw vLLM campaign derived decode from TPOT, while its showcase used gateway-observed streaming latency and server-reported token counts. The publication therefore uses separate panels and explicit labels rather than one false speed leaderboard.

## Reasoning latency

Reasoning models can emit a first reasoning token quickly and still withhold the answer for a long time:

- Qwen thinking pilot: median TTFT 61.2 ms; median TTFAT 28.801 s.
- Step natural-stop coherence check: warm-prefix TTFT 0.206 s; TTFAT 33.164 s.

That gap is real user wait time even when token-level decode is healthy.

## Claim labels

- **Measured:** produced by this campaign and retained in its evidence.
- **Reported:** copied from an upstream model card, runtime, or manufacturer source.
- **Inferred:** a reasoned interpretation rather than direct instrument output.
- **Operator reviewed:** a disclosed human qualitative judgment.
