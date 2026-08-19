#!/usr/bin/env python3
"""Generate deterministic, dependency-free SVG charts from public CSV data."""

from __future__ import annotations

import csv
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "charts"

BG = "#08111f"
PANEL = "#111d30"
GRID = "#26364e"
TEXT = "#f8fafc"
MUTED = "#aab8cc"
BLUE = "#38bdf8"
PURPLE = "#a78bfa"
GOLD = "#fbbf24"
GREEN = "#34d399"
RED = "#fb7185"


def rows(name: str):
    with (DATA / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def svg_open(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f"<title id=\"title\">{escape(title)}</title>",
        f"<desc id=\"desc\">{escape(description)}</desc>",
        f'<rect width="{width}" height="{height}" rx="24" fill="{BG}"/>',
    ]


def text(x, y, value, size=16, color=TEXT, weight=500, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="Inter,system-ui,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'
    )


def write(name: str, parts: list[str]):
    OUT.mkdir(exist_ok=True)
    parts.append("</svg>")
    (OUT / name).write_text("\n".join(parts) + "\n", encoding="utf-8")


def line_panel(parts, x, y, w, h, title_value, values, x_max, y_max, color, x_label):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{PANEL}"/>')
    parts.append(text(x + 24, y + 34, title_value, 18, TEXT, 750))
    left, top, right, bottom = x + 64, y + 58, x + w - 24, y + h - 54
    for tick in range(0, int(y_max) + 1, 20):
        py = bottom - (tick / y_max) * (bottom - top)
        parts.append(f'<line x1="{left}" y1="{py:.1f}" x2="{right}" y2="{py:.1f}" stroke="{GRID}"/>')
        parts.append(text(left - 10, py + 5, tick, 12, MUTED, 500, "end"))
    points = []
    for point_index, (xv, yv, label) in enumerate(values):
        px = left + (xv / x_max) * (right - left)
        py = bottom - (yv / y_max) * (bottom - top)
        value_label_y = py - 13 - (18 if point_index % 2 else 0)
        horizontal_offset = -6 if point_index == 0 else (6 if point_index == 1 else 0)
        label_anchor = "end" if point_index == 0 else ("start" if point_index == 1 else "middle")
        tick_offset = -4 if point_index == 0 else (4 if point_index == 1 else 0)
        points.append(f"{px:.1f},{py:.1f}")
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{color}"/>')
        parts.append(text(px + horizontal_offset, value_label_y, f"{yv:.1f}", 12, TEXT, 700, label_anchor))
        parts.append(text(px + tick_offset, bottom + 22, label, 11, MUTED, 500, label_anchor))
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>')
    parts.append(text((left + right) / 2, y + h - 13, x_label, 12, MUTED, 600, "middle"))
    parts.append(text(x + 17, (top + bottom) / 2, "tokens/s", 12, MUTED, 600, "middle"))


def context_chart():
    gpt = [(float(r["context_tokens"]), float(r["decode_tokens_s"]), label) for r, label in zip(rows("gptoss-context.csv"), ["0", "8K", "32K", "49K", "131K"])]
    qwen_rows = [r for r in rows("qwen-context.csv") if r["kv"] == "BF16"]
    qwen = [(float(r["input_tokens"]), float(r["decode_tokens_s"]), label) for r, label in zip(qwen_rows, ["512", "2K", "8K", "32K"])]
    p = svg_open(1200, 650, "Context depth and decode", "Separate panels show GPT-OSS llama.cpp native decode and Qwen vLLM TPOT-derived decode.")
    p.append(text(50, 55, "Decode as context grows", 30, TEXT, 850))
    p.append(text(50, 84, "Different backends and timing instruments are intentionally separated.", 15, MUTED))
    line_panel(p, 40, 115, 545, 455, "GPT-OSS-120B · llama.cpp native", gpt, 131000, 100, BLUE, "active context depth")
    line_panel(p, 615, 115, 545, 455, "Qwen3.6-27B-FP8 · vLLM TPOT", qwen, 33000, 100, PURPLE, "input tokens")
    p.append(text(600, 615, "Measured on the same dual-RTX 3090 server; not a cross-backend speed leaderboard.", 13, GOLD, 650, "middle"))
    write("context-and-decode.svg", p)


def speculative_chart():
    data = rows("speculative-decoding.csv")
    p = svg_open(1200, 650, "Speculative decoding uplift", "Qwen and Step parent versus MTP throughput in separately scaled panels.")
    p.append(text(50, 55, "MTP changed local usability", 30, TEXT, 850))
    p.append(text(50, 84, "Matched comparisons within each model and instrument.", 15, MUTED))
    panels = [
        (40, 125, 350, 400, data[0], 85, "Qwen · C1"),
        (425, 125, 350, 400, data[1], 500, "Qwen · C8 aggregate"),
        (810, 125, 350, 400, data[2], 45, "Step · fixed-work decode"),
    ]
    for x, y, w, h, row, ymax, label in panels:
        p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{PANEL}"/>')
        p.append(text(x + 20, y + 34, label, 18, TEXT, 750))
        base = y + h - 70
        barw = 82
        for idx, (name, key, color) in enumerate([("Parent", "parent_tokens_s", MUTED), ("MTP", "mtp_tokens_s", GREEN)]):
            value = float(row[key])
            bh = value / ymax * 260
            bx = x + 72 + idx * 125
            p.append(f'<rect x="{bx}" y="{base-bh:.1f}" width="{barw}" height="{bh:.1f}" rx="8" fill="{color}"/>')
            p.append(text(bx + barw/2, base - bh - 12, f"{value:.2f}", 14, TEXT, 750, "middle"))
            p.append(text(bx + barw/2, base + 27, name, 13, MUTED, 650, "middle"))
        p.append(text(x + w/2, y + h - 20, f"+{float(row['uplift_percent']):.2f}% · {float(row['acceptance_percent']):.1f}% accepted", 14, GOLD, 750, "middle"))
    p.append(text(600, 595, "C8 is aggregate throughput; it must not be compared to batch-one decode.", 13, MUTED, 600, "middle"))
    write("speculative-decoding.svg", p)


def placement_chart():
    data = rows("placement.csv")
    selected = [data[0], data[1], data[2], data[3]]
    p = svg_open(1200, 680, "Hybrid model placement", "Stacked model-buffer placement across GPU zero, GPU one, and host memory.")
    p.append(text(50, 55, "Where the large models actually lived", 30, TEXT, 850))
    p.append(text(50, 84, "Main model buffers only; sidecars and KV are annotated separately in the data.", 15, MUTED))
    x0, x1, max_mib = 300, 1040, 125000
    colors = [BLUE, PURPLE, GOLD]
    labels = ["GPU 0", "GPU 1", "Host memory"]
    for i, row in enumerate(selected):
        y = 145 + i * 112
        name = row["model"] if i == 0 else f"{row['model']} · {row['mode']}"
        p.append(text(45, y + 27, name, 15, TEXT, 700))
        cursor = x0
        vals = [float(row["gpu0_main_mib"]), float(row["gpu1_main_mib"]), float(row["host_main_mib"])]
        for value, color, label in zip(vals, colors, labels):
            bw = value / max_mib * (x1 - x0)
            p.append(f'<rect x="{cursor:.1f}" y="{y}" width="{bw:.1f}" height="38" fill="{color}"/>')
            if bw > 78:
                p.append(text(cursor + bw/2, y + 25, f"{value/1024:.1f}", 12, BG, 800, "middle"))
            cursor += bw
        p.append(text(1120, y + 27, f"{sum(vals)/1024:.1f} GiB", 13, MUTED, 650, "end"))
    for i, (label, color) in enumerate(zip(labels, colors)):
        lx = 360 + i * 190
        p.append(f'<rect x="{lx}" y="610" width="16" height="16" rx="3" fill="{color}"/>')
        p.append(text(lx + 24, 623, label, 13, MUTED, 650))
    write("placement.svg", p)


def capability_chart():
    data = rows("capability-outcomes.csv")
    models = ["GPT-OSS-120B", "Laguna S 2.1", "Qwen3.6-27B-FP8", "Step 3.7 Flash"]
    colors = {"pass": GREEN, "partial": GOLD, "fail": RED}
    labels = {"pass": "PASS", "partial": "PARTIAL", "fail": "FAIL"}
    p = svg_open(1200, 650, "Shared capability outcomes", "Outcome matrix for four models and four shared tests.")
    p.append(text(50, 55, "Healthy inference did not guarantee a finished product", 30, TEXT, 850))
    p.append(text(50, 84, "Artifact outcomes include runtime and operator inspection.", 15, MUTED))
    left, top, cellw, cellh = 285, 135, 215, 92
    for j, model in enumerate(models):
        p.append(text(left + j*cellw + cellw/2, 115, model, 13, TEXT, 750, "middle"))
    for i, row in enumerate(data):
        y = top + i*cellh
        p.append(text(45, y + 55, row["test"], 16, TEXT, 700))
        for j, model in enumerate(models):
            status = row[model]
            x = left + j*cellw
            p.append(f'<rect x="{x+7}" y="{y+8}" width="{cellw-14}" height="{cellh-16}" rx="13" fill="{colors[status]}" fill-opacity="0.18" stroke="{colors[status]}"/>')
            p.append(text(x + cellw/2, y + 56, labels[status], 14, colors[status], 850, "middle"))
    p.append(text(600, 555, "Step's story was the operator favorite. Qwen shipped the only Twin that ran as submitted.", 14, MUTED, 650, "middle"))
    p.append(text(600, 582, "No Surf Simulator fully passed. No faithful finished Digital Twin was produced.", 14, GOLD, 750, "middle"))
    write("capability-outcomes.svg", p)


def effort_chart():
    data = rows("agent-effort.csv")
    p = svg_open(1200, 690, "Agent output-token effort", "Log-scaled Surf and Digital Twin output-token effort by model.")
    p.append(text(50, 55, "The cost of trying to finish", 30, TEXT, 850))
    p.append(text(50, 84, "Output tokens across multi-request build-agent sessions · logarithmic scale.", 15, MUTED))
    max_log = math.log10(140000)
    for i, row in enumerate(data):
        y = 135 + i * 120
        p.append(text(45, y + 40, row["model"], 16, TEXT, 750))
        for offset, key, label, color in [(0, "surf_output_tokens", "Surf", BLUE), (46, "twin_output_tokens", "Twin", PURPLE)]:
            value = float(row[key])
            width = math.log10(max(value, 1)) / max_log * 760
            p.append(f'<rect x="300" y="{y+offset}" width="{width:.1f}" height="30" rx="7" fill="{color}"/>')
            p.append(text(310 + width, y + offset + 21, f"{int(value):,}", 13, TEXT, 700))
            p.append(text(280, y + offset + 21, label, 12, MUTED, 650, "end"))
    p.append(text(600, 635, "More output was not automatically better: Laguna and Step spent heavily without shipping the requested products.", 13, GOLD, 650, "middle"))
    write("agent-effort.svg", p)


def main():
    context_chart()
    speculative_chart()
    placement_chart()
    capability_chart()
    effort_chart()
    print("Generated 5 SVG charts")


if __name__ == "__main__":
    main()
