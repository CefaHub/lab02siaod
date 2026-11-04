#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерация точных наборов операций ЛР 2 для варианта 14 (seed=44).

Алгоритм и параметры соответствуют generate_ops из исходного репозитория курса.
Сгенерированные данные сохраняются локально в data/generated и не коммитятся.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

VARIANT = 14
SEED = 30 + VARIANT
OPS_LENGTH = 100_000
OPS_MAX_SIZE = 5_000
APPEND_SIZE_RANGE = (1_000, 200_000)


def _ops_walk(rng: random.Random, n_ops: int, max_size: int,
              pushes: tuple[str, ...], pops: tuple[str, ...],
              peek: str | None) -> list[str]:
    lines: list[str] = []
    size = 0

    def step(grow: bool) -> None:
        nonlocal size
        if peek is not None and rng.random() < 0.1:
            lines.append(peek)
        elif rng.random() < (0.7 if grow else 0.3):
            lines.append(f"{rng.choice(pushes)} {rng.randrange(1_000_000)}")
            size += 1
        else:
            lines.append(rng.choice(pops))
            size = max(0, size - 1)

    while len(lines) < n_ops:
        target = int(max_size ** rng.random())
        while size < target and len(lines) < n_ops:
            step(grow=True)
        while size > 0 and len(lines) < n_ops:
            step(grow=False)
        if rng.random() < 0.5:
            lines.append(rng.choice(pops if peek is None else (*pops, peek)))
    return lines[:n_ops]


def main() -> None:
    out = Path("data/generated")
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    files = {
        "ops_stack.txt": _ops_walk(rng, OPS_LENGTH, OPS_MAX_SIZE,
                                   ("push",), ("pop",), "peek"),
        "ops_deque.txt": _ops_walk(rng, OPS_LENGTH, OPS_MAX_SIZE,
                                   ("push_front", "push_back"),
                                   ("pop_front", "pop_back"), None),
    }
    lo, hi = APPEND_SIZE_RANGE
    sizes = {int(lo * (hi / lo) ** ((i + rng.random()) / 8)) for i in range(8)}
    k = rng.randint(lo.bit_length(), hi.bit_length() - 2)
    sizes |= {2 ** k, 2 ** k + 1}
    files["ops_append_sizes.txt"] = [str(n) for n in sorted(sizes)]

    for filename, lines in files.items():
        (out / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest = {
        "variant": VARIANT,
        "seed": SEED,
        "generated": ["ops"],
        "files": sorted(files),
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Данные варианта {VARIANT} (seed={SEED}) записаны в {out.resolve()}")
    for filename, lines in files.items():
        print(f"  {filename}: {len(lines)} строк")


if __name__ == "__main__":
    main()
