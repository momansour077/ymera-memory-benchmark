# Data and reproduction contract

The CSV contains six summary comparisons transcribed from the author's Zenodo
preprint, DOI [10.5281/zenodo.20256693](https://doi.org/10.5281/zenodo.20256693).
The values were checked against the preprint on September 5, 2026. Rounded values
in this CSV correspond to the paper's abstract and result tables.

## What the commands establish

| Command | Establishes | Does not establish |
| --- | --- | --- |
| `python3 notebook/validate_summary.py` | Required columns, six unique comparison IDs, complete cells, finite effect sizes, valid p-value syntax/range | Correctness of the underlying experiment or freedom from statistical bias |
| `python3 -m unittest discover -s tests -v` | Valid data loads and defined malformed inputs fail | That a new simulation reproduces the research |
| `MPLBACKEND=Agg python notebook/ymera_results_analysis.py --output /tmp/ymera.png` | Six reported comparisons can be loaded, printed, and plotted | Independent recomputation of effect sizes or p-values |

## Fields

- `comparison`: stable identifier for one of the six published comparisons.
- `condition_a`, `condition_b`: labels from the study.
- `n`: reported sample description; `n/a` means this summary does not supply a count.
- `cohens_d`: reported, rounded standardized effect size; finite numeric value.
- `p_value`: reported exact value or upper bound such as `<1e-58`.
- `protocol`: experiment or analysis family. Results from different protocols are
  not interchangeable independent replicates.
- `interpretation`: an author-provided summary, not a computed label.

## Limits to interpretation

The public repository does not contain raw observations, model execution traces,
or the simulation engine. Significance and effect-size estimates cannot be
independently recalculated here. A non-significant difference does not prove two
systems equivalent. The exploratory post-hoc result is not confirmatory evidence.
Repeated observations and protocol differences must be considered when reading
the paper; the small p-values should not be treated as proof of universal effects.

## Changes in the September 2026 maintenance update

Added input validation and failure-path tests; corrected claims about source code
and statistical reproduction; derived display labels from p-values instead of
hard-coding them by comparison name; made chart-output failure visible through a
nonzero exit; added an explicit output path. No data values were changed.

The maintenance changes were prepared with Codex assistance. They improve the
public reporting tools and do not constitute new experiments or new findings.
