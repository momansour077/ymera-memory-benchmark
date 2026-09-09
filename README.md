# YMERA — public memory-ablation results

**Summary data, validation, and Python visualization for a published 21-agent study.**

Paper: Mohamed Fathy Mansour (2026), *Memory Presence Matters, Mechanism Does Not:
Evidence from a 21-Agent Organizational Simulation on a Historical Economic
Benchmark*. [Zenodo preprint / DOI](https://doi.org/10.5281/zenodo.20256693).

The repository makes six reported comparisons easy to inspect. It does **not**
contain the simulation engine or raw run observations. Running it reproduces the
summary presentation, not the original experiment or its statistics. Start with
the [data and reproduction contract](docs/DATA_AND_REPRODUCTION.md).

## The question and reported findings

Does giving agents memory help, and does a more complex mechanism improve on flat
retrieval? The paper reports an advantage for memory presence in its tested setup,
without a statistically significant aggregate advantage for bio-inspired over
flat retrieval. A non-significant difference is not proof of equivalence; these
findings do not generalize automatically to other models or tasks.

| Comparison | Reported n | Cohen's d | Reported p |
| --- | --- | --- | --- |
| Bio-memory vs no memory | 78/arm | 5.30 | <1e-58 |
| Flat retrieval vs no memory | 78/arm | 4.94 | <1e-58 |
| Bio-memory vs flat retrieval | 78/arm | 0.14 | 0.390 |
| Memory on vs off, crisis-continuation | 212/244 | 6.28 | 2.10e-195 |
| Full system on vs off | Not supplied in this summary | 3.16 | 2.52e-120 |
| Bio vs flat, CEO+CHRO crisis years, exploratory post hoc | Not supplied in this summary | 1.03 | 0.022 |

Values are transcribed from the paper, not recomputed here. Different protocols
are not interchangeable independent replications. The post-hoc result is exploratory.

![Reported effect sizes](ymera_effect_sizes.png)

## Run the checks

Python 3.11 or newer. The validator and tests use the standard library:

```bash
python3 notebook/validate_summary.py
python3 -m unittest discover -s tests -v
```

To generate the chart with pinned plotting dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
MPLBACKEND=Agg python notebook/ymera_results_analysis.py --output /tmp/ymera.png
```

Expected: six validated comparisons, ten passing tests, a printed summary, and
a PNG. No API key, model download, or paid inference is needed. Installation needs
network access. Validation, tests, and plotting passed locally on Python **3.11.15
and 3.13.13**, macOS arm64, September 5, 2026. Validation and all ten tests were
rerun successfully on both versions on September 9. The same ten tests ran twice;
this is not a claim of twenty distinct tests. [GitHub CI passed on September 7](https://github.com/momansour077/ymera-memory-benchmark/actions/runs/34097980560)
for commit `db17e9ec1a48455893f61e8854819373336bf272`, on Python 3.11 and 3.13.
That result belongs to that commit; later changes need their own CI run.

## What the code demonstrates

- Schema checks, complete cells, and exactly six unique known comparison IDs.
- Rejection of duplicate/missing comparisons, non-finite effects, invalid p-values,
  and wrong headers.
- Decimal parsing preserves very small p-values and distinguishes exact values
  from upper bounds. Display labels derive from the data.
- Output-path control and nonzero exit if chart generation fails.
- Separation of data validation from statistical replication claims.

`data/` contains the CSV; `notebook/` holds the validator and plotting script;
`tests/` holds failure-path tests. `requirements.lock` pins plotting dependencies
with Python-version markers where required.

## Attribution and scope

The underlying paper is a preprint, not a claim of peer-reviewed publication.
The public CSV is unchanged in this maintenance update. Existing citation and
license metadata are retained; no new software license is selected.
See [CITATION.cff](CITATION.cff).

The September maintenance changes were prepared with Codex assistance. They
improve the reporting tools and documentation; they are not new experiments.
