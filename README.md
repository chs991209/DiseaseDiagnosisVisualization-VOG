# VOG Visualization

Lightweight notebook-based visualization workflow for VOG (video-oculography) CSV data.
The project is designed for quick signal quality checks and exploratory analysis of saccade tasks.

## Who This Is For

- Medical researchers: verify eye-tracking behavior and data quality by patient/task/session.
- ML engineers: inspect preprocessing assumptions, target alignment, and error signals before feature modeling.

## What It Does

- Reads VOG CSV files with robust encoding fallback (`utf-16`, `utf-16le`, `utf-8-sig`, `cp949`).
- Detects the true header row using required keywords (`LH`, `RH`, `Target`).
- Cleans null-byte artifacts and irregular row lengths.
- Converts numeric columns safely (`errors='coerce'`), drops fully empty rows.
- Plots 3 synchronized views:
  - target vs left/right eye trajectories,
  - left/right tracking error (`Eye - Target`),
  - non-target-axis movement for noise/outlier monitoring.

<img width="1589" height="1145" alt="output" src="https://github.com/user-attachments/assets/0b977560-0c6e-4580-8deb-298cd85c1701" />

## Notebooks

- `visualization.ipynb`: single-file visualization pipeline and plotting.
- `visualization_atoz.ipynb`: extended version with metadata-aware titles and recursive batch processing.

See `NOTEBOOKS.md` for notebook-level details.

## Quick Start

1. Prepare CSVs under a data folder (example: `data/sample_csv/...`).
2. Open one of the notebooks.
3. Update input path(s) in the final execution cell.
4. Run all cells and review generated plots.

## Input Expectations

- CSV should include time-like column and target columns (`TargetH`/`TargetV` variants).
- Eye channels should include horizontal/vertical pairs (`LH`,`RH`,`LV`,`RV` variants).
- Column names are matched defensively and case-insensitively.

## Current Scope

- Visualization and exploratory quality control only.
- No model training, inference, or automated report export yet.
