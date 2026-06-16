# How to publish this — and the honest truth about income

**Read this first (no false promises):** publishing data on Kaggle/HuggingFace does
**NOT** pay you directly. Neither platform has a royalty/sales mechanism for datasets.
The value of this package is as a **credential** — a clean, citable, public artifact
that strengthens the applications you are *already* winning (RWS, micro1, Scale, Cohere,
and similar evaluation/AI-data work). The income comes from getting selected for paid
work, not from the upload itself. Treat it as portfolio leverage, not a paycheck.

What's in this folder is 100% safe to publish: it's built only from the **already-public
Zenodo preprint** (CC-BY-4.0). The simulation **codebase is intentionally excluded** (it
holds operational credentials). Do not add anything from the YMERA backup or the
recovered vault.

---

## Option A — GitHub repo (do this first; it's the anchor link)

The single most useful artifact: a public GitHub repo recruiters can open in 10 seconds.

```bash
cd ~/project/ymera-public
git init && git add . && git commit -m "YMERA: public writeup + memory-ablation results"
gh repo create ymera-memory-benchmark --public --source=. --push   # needs gh auth
```

Then put the repo link on your CV, LinkedIn, and in the "Online CV / Portfolio" field
of vendor profiles (RWS Workzone, etc.).

## Option B — Kaggle dataset + notebook (visibility in the AI-data community)

1. Kaggle → **Datasets → New Dataset** → upload `data/ymera_memory_ablation_results.csv`.
   - Title: *YMERA — LLM Agent Memory Ablation Results*
   - Description: paste the README's "What the study found" + "Headline results" + the DOI.
   - License: **CC-BY-4.0** (matches the paper).
2. Kaggle → **Code → New Notebook** → attach the dataset → paste
   `notebook/ymera_results_analysis.py`. Run it; the effect-size chart renders inline.
3. Make both **public**. Link them from the GitHub repo and your profile.

## Option C — HuggingFace dataset (optional, for ML reach)

`huggingface.co` → **New Dataset** → upload the CSV + README. Same content, ML audience.

---

## Where this actually converts to income

- **Vendor profiles** (RWS, micro1, Mercor, Scale, Cohere): paste the GitHub/Kaggle
  link in the portfolio/online-CV field. A published, rigorous eval benchmark is
  exactly the signal these AI-data employers select on — it raises your project-invite
  odds. *That* is the revenue path.
- **CV / LinkedIn**: "Author, peer-reviewable LLM-agent evaluation benchmark (Zenodo
  DOI; CC-BY-4.0)" — concrete, verifiable, differentiating.

## Do NOT

- Upload the simulation source code, the YMERA backup zip, or anything from
  `~/ymera_recovered_vault/` — they contain live secrets.
- Restate the speculative business-plan claims (TAM/valuation) — keep the public
  artifact to the verifiable science only.
