"""YMERA memory-ablation — a transparent view of the published effect sizes.

Loads the public summary results (from the Zenodo preprint, DOI 10.5281/zenodo.20256693)
and visualizes the reported values without recomputing statistical estimates.
Run from the repository root using the commands in README.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
if __package__:
    from .validate_summary import load_summary, significance_label
else:
    from validate_summary import load_summary, significance_label

CSV = Path(__file__).resolve().parents[1] / "data" / "ymera_memory_ablation_results.csv"


def load() -> pd.DataFrame:
    df = pd.DataFrame(load_summary(CSV))
    df["cohens_d"] = pd.to_numeric(df["cohens_d"], errors="raise")
    return df


def summarize(df: pd.DataFrame) -> None:
    print("YMERA memory-ablation — published effect sizes\n" + "=" * 50)
    for _, r in df.iterrows():
        sig = significance_label(r["p_value"])
        print(f"  {r['comparison']:24s} d={r['cohens_d']:>5}  p={r['p_value']:<10} ({sig})")
    print("\nSummary values only: statistics are not recalculated from raw runs. "
          "The aggregate mechanism comparison is not significant; this does not establish equivalence.")


def plot(df: pd.DataFrame, out: Path) -> None:
    import matplotlib.pyplot as plt  # lazy: the summary table works without it

    order = df.sort_values("cohens_d", ascending=True)
    colors = ["#c0392b" if c == "bio_vs_flat" else "#2e86de" for c in order["comparison"]]
    plt.figure(figsize=(9, 5))
    plt.barh(order["comparison"], order["cohens_d"], color=colors)
    plt.axvline(0.8, ls="--", color="gray", lw=1)
    plt.text(0.85, -0.4, "d=0.8 (large)", color="gray", fontsize=8)
    plt.xlabel("Cohen's d (effect size)")
    plt.title("YMERA: reported effect sizes across six study comparisons")
    plt.tight_layout()
    plt.savefig(out, dpi=130)
    plt.close()
    print(f"\nsaved chart -> {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("ymera_effect_sizes.png"))
    args = parser.parse_args()
    df = load()
    summarize(df)
    # Failure to generate the requested artifact must produce a nonzero exit.
    plot(df, args.output)


if __name__ == "__main__":
    main()
