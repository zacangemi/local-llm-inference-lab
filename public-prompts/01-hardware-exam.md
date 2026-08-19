I run a local AI inference server and want your expert analysis on optimizing
it. Be specific and quantitative where possible, and prioritize your
recommendations by expected impact.

THE HARDWARE:
- CPU: AMD Threadripper PRO 9955WX — 16 cores / 32 threads, Zen 5, 2 CCDs,
  on an ASUS Pro WS WRX90E-SAGE SE (WRX90 chipset, sTR5)
- RAM: 128 GB (8× 16 GB) DDR5-6000 ECC RDIMM, all 8 channels populated,
  one DIMM per channel. The kit is factory-rated for 6400.
- GPUs: 2× NVIDIA RTX 3090 Founders Edition (24 GB GDDR6X each, 48 GB
  total), both at PCIe Gen4 x16, no NVLink bridge
- Storage: 2 TB PCIe NVMe SSD
- PSU: 1600 W. OS: Ubuntu 24.04.

THE WORKLOAD:
I serve large mixture-of-experts models with llama.cpp using hybrid GPU+CPU
inference. Current flagship: a 120B-parameter MoE (5.1B active parameters,
128 experts/layer, top-4 routing, 36 layers) quantized to ~59 GB. Since it
exceeds VRAM, I keep the expert tensors of the first 12 layers in system RAM
(--n-cpu-moe 12) and everything else on the GPUs with a 23/13 layer split.
Context is 50K with Q8_0 KV cache, flash attention on, single user.

MEASURED PERFORMANCE (my own benchmarks):
- Decode: ~83 tokens/s at empty context, ~64 t/s at 32K depth, ~55 t/s at
  49K depth
- Prefill: ~1,050 t/s sustained on a 49K prompt (TTFT ~46 s); pp512 ~665 t/s
- During decode, the CPU averages ~9.5 cores busy; during prefill it's nearly
  idle while the GPUs work
- Measured system RAM bandwidth (STREAM TRIAD, pinned): ~120 GB/s

MY QUESTIONS — answer each specifically:
1. What is the binding bottleneck for my decode speed, and why? Walk through
   the arithmetic.
2. My RAM kit is rated DDR5-6400 but runs at 6000. Would raising it to 6400
   improve my decode? Estimate the gain.
3. Would moving the KV cache to system RAM to free VRAM for more expert layers
   be a net win or loss? Show reasoning.
4. If I could change ONE component to improve hybrid MoE decode the most,
   what would it be and roughly how much would it help? Consider CPU options
   within the same socket.
5. What software-level optimizations should I try next, in priority order,
   and what would each realistically buy me? (Consider batching parameters,
   speculative decoding, thread counts, placement tuning.)
6. Is there anything in my current configuration that looks like a mistake or
   a leftover suboptimal choice?

Be honest about uncertainty — if something depends on information you don't
have, say what you'd need to measure.
