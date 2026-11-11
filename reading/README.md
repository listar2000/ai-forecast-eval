# Forecasting evaluation reading collection

Collected November 9, 2026. Scope: priorities 1–4 from the meeting-history reading list. These are source materials for subsequent reading, not a completed literature review.

## 1. ForecastBench

- **Read first:** [ForecastBench: Updated Ranking Methodology](01_forecastbench/updated_ranking_methodology.pdf). Separate supplemental technical report by Simas Kucinskas, Houtan Bastani, and Ezra Karger. [Original PDF](https://www.forecastbench.org/assets/pdfs/forecastbench_updated_methodology.pdf).
- [ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities](01_forecastbench/forecastbench_paper.pdf). Main paper and appendices. [arXiv record](https://arxiv.org/abs/2409.19839).
- Reading focus: difficulty-adjusted Brier score, fixed-effect identification, use of market forecasts, and simulation assumptions.

## 2. Metaculus FutureEval

- **Read first:** [The FutureEval model leaderboard](02_futureeval/model_leaderboard.md). Sylvain, February 10, 2026; edited February 23, 2026. [Original post](https://www.metaculus.com/notebooks/42076/the-futureeval-model-leaderboard/). This matches the meeting's discussion of pairwise score differences, ridge regression, staggered participation, and spot-score weighting.
- [Methodology overview](02_futureeval/methodology_overview.md). [Original page](https://www.metaculus.com/futureeval/methodology/).
- Reading focus: overlap graph, regularization, weighting, bootstrap confidence intervals, and question discrimination.

## 3. Metaculus Peer Score

- [Scores FAQ, including expandable mathematics](03_peer_score/scores_faq.md). [Original page](https://www.metaculus.com/help/scores-faq/).
- Reading focus: log score, Peer Score, time averaging, spot scoring, and the distinction between scoring an individual forecast and estimating leaderboard skill.
- **Meeting-note correction to track:** the official Metaculus definition uses differences in **log scores**, not Brier scores. Keep any Brier-based peer-score variant used elsewhere distinct.

## 4. Item Response Theory for model evaluation

The meetings did not name exact public IRT papers. These two are suggested starting points, not verified matches to papers discussed:

- [tinyBenchmarks: evaluating LLMs with fewer examples](04_irt/tinybenchmarks.pdf), Maia Polo et al. [arXiv record](https://arxiv.org/abs/2402.14992); [authors' code](https://github.com/felipemaiapolo/tinyBenchmarks). Useful for IRT-based estimation from a limited evaluation subset.
- [Lost in Benchmarks? Rethinking Large Language Model Benchmarking with Item Response Theory](04_irt/lost_in_benchmarks.pdf), Zhou et al. [arXiv record](https://arxiv.org/abs/2505.15055). Useful for item properties and separating model capabilities.

Still to obtain from the team:

- Anrui's IRT implementation and any accompanying write-up.
- The exact title or copy of Haifeng and Mary's “3D/cancer IRT” paper.
- Any preferred foundational IRT reference or forecasting-specific IRT variant.

Do not assume the meeting notes' claims that IRT necessarily requires MCMC or discretization apply to every IRT variant; verify assumptions for each candidate method.

## Formats and provenance

- Four original PDF downloads were validated with a PDF parser. Adjacent `.txt` files provide searchable text; equations, figures, tables, and some complex PDF objects may be omitted or imperfect. Use PDFs as authoritative.
- The FutureEval Markdown files are web text extractions. Original image URLs in the detailed post remain remote; the overview omits interactive content and some link targets.
- Direct Metaculus HTML downloads returned a site challenge. The Scores FAQ Markdown was therefore converted from the official public website repository, retaining 105 mathematical expressions and the expandable math sections. Original TSX files are under `03_peer_score/source/`. The repository snapshot may differ from the live deployment.
- `02_futureeval/source/` retains the introductory methodology component as additional source material; it is not the complete methodology page.
- The Metaculus source revision is in [metaculus_source_revision.txt](metaculus_source_revision.txt). [sources.json](sources.json) records source URLs and local file hashes.
- These are snapshots retrieved on the date above, not archived versions from the meeting dates. Original authors retain their respective rights.
