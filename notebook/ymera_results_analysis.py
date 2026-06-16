"""YMERA memory-ablation — a transparent view of the published effect sizes.

Loads the public summary results (from the Zenodo preprint, DOI 10.5281/zenodo.20256693)
and visualizes them. The story in one chart: memory PRESENCE produces enormous effect
sizes (d ~5-6), while the memory MECHANISM (bio vs. flat) does not separate (d ~0.14).

Run:  pip install pandas matplotlib  &&  python ymera_results_analysis.py
On Kaggle: paste this into a notebook cell after adding the results CSV as a dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CSV = Path(__file__).resolve().parents[1] / "data" / "ymera_memory_ablation_results.csv"


def load() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    df["cohens_d"] = pd.to_numeric(df["cohens_d"], errors="coerce")
    return df


def summarize(df: pd.DataFrame) -> None:
    print("YMERA memory-ablation — published effect sizes\n" + "=" * 50)
    for _, r in df.iterrows():
        sig = "n.s." if r["comparison"] == "bio_vs_flat" else "significant"
        print(f"  {r['comparison']:24s} d={r['cohens_d']:>5}  p={r['p_value']:<10} ({sig})")
    print("\nTakeaway: memory PRESENCE -> d 5.30/4.94/6.28 (huge); "
          "memory MECHANISM (bio vs flat) -> d 0.14 (no separation).")


def plot(df: pd.DataFrame, out: Path) -> None:
    import matplotlib.pyplot as plt  # lazy: the summary table works without it

    order = df.sort_values("cohens_d", ascending=True)
    colors = ["#c0392b" if c == "bio_vs_flat" else "#2e86de" for c in order["comparison"]]
    plt.figure(figsize=(9, 5))
    plt.barh(order["comparison"], order["cohens_d"], color=colors)
    plt.axvline(0.8, ls="--", color="gray", lw=1)
    plt.text(0.85, -0.4, "d=0.8 (large)", color="gray", fontsize=8)
    plt.xlabel("Cohen's d (effect size)")
    plt.title("YMERA: memory presence dominates; mechanism (red) does not separate")
    plt.tight_layout()
    plt.savefig(out, dpi=130)
    print(f"\nsaved chart -> {out}")


def main() -> None:
    df = load()
    summarize(df)
    try:
        plot(df, CSV.parent.parent / "ymera_effect_sizes.png")
    except Exception as exc:  # headless / no display is fine — the table is the point
        print(f"(plot skipped: {exc.__class__.__name__})")


if __name__ == "__main__":
    main()
