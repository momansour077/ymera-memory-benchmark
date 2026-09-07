"""Validate the public summary CSV; do not recompute research statistics."""

from __future__ import annotations

import csv
import math
from decimal import Decimal, InvalidOperation
from pathlib import Path

CSV = Path(__file__).resolve().parents[1] / "data" / "ymera_memory_ablation_results.csv"
FIELDS = ["comparison", "condition_a", "condition_b", "n", "cohens_d", "p_value", "protocol", "interpretation"]
COMPARISONS = {"bio_vs_none", "flat_vs_none", "bio_vs_flat", "memoryon_vs_memoryoff", "fullsystem_on_vs_off", "posthoc_bio_gt_flat"}


def parse_p_value(value: str) -> tuple[str, Decimal]:
    operator = "<" if value.startswith("<") else "="
    try:
        number = Decimal(value[1:] if operator == "<" else value)
    except InvalidOperation as exc:
        raise ValueError("Invalid p-value") from exc
    if not number.is_finite() or not Decimal(0) < number <= Decimal(1):
        raise ValueError("p-value must be finite and in (0, 1]")
    return operator, number


def significance_label(value: str) -> str:
    operator, number = parse_p_value(value)
    if operator == "<":
        return ("reported p < 0.05" if number <= Decimal("0.05")
                else "reported bound does not establish whether p < 0.05")
    return "reported p < 0.05" if number < Decimal("0.05") else "reported p >= 0.05"


def load_summary(path: Path = CSV) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError("Unexpected CSV schema")
        rows = list(reader)
    seen: set[str] = set()
    for row in rows:
        if set(row) != set(FIELDS) or any(not isinstance(v, str) or not v.strip() for v in row.values()):
            raise ValueError("Every row must contain all fields with nonempty values")
        comparison = row["comparison"]
        if comparison in seen or comparison not in COMPARISONS:
            raise ValueError("Unknown or duplicate comparison")
        seen.add(comparison)
        try:
            effect = float(row["cohens_d"])
        except ValueError as exc:
            raise ValueError("Invalid effect size") from exc
        if not math.isfinite(effect):
            raise ValueError("Effect size must be finite")
        parse_p_value(row["p_value"])
    if seen != COMPARISONS:
        raise ValueError("Expected all six published comparisons")
    return rows


if __name__ == "__main__":
    print(f"Validated {len(load_summary())} published summary rows; raw-run statistics were not recomputed.")
