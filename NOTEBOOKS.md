# Notebook Guide

This document summarizes each notebook for fast onboarding by medical researchers and ML engineers.

## `visualization.ipynb`

Purpose: visualize one VOG CSV file with defensive parsing.

- Core function: `visualize_vog_data(file_path)`
- Workflow:
  - validate file path,
  - auto-detect encoding and header row,
  - parse/clean numeric data,
  - infer axis direction from target columns,
  - generate 3-panel figure (raw signal, tracking error, cross-axis noise).
- Best use: single-session inspection and debugging parser behavior.

Execution entry (last cell): points to one sample CSV path in `data/sample_csv/...`.

## `visualization_atoz.ipynb`

Purpose: end-to-end directory-level visualization with contextual metadata.

- Reuses robust single-file parser/plotter from the first notebook.
- Adds metadata extraction from file path:
  - group (for example `HC`, `MCI`),
  - session ID,
  - task name.
- Adds batch runner: `visualize_directory_recursively(base_dir_path)`
  - recursively scans `*.csv`,
  - runs visualization for each file,
  - prints progress and success count.
- Best use: dataset-wide exploratory review and quick QC sweep.

Execution entry (last cell): targets `data/sample_csv` for recursive processing.

## Interpreting the 3 Plots

- Raw waveform: confirms if both eyes follow target trajectory.
- Tracking error (`Error_L`, `Error_R`): highlights latency/overshoot/mismatch.
- Cross-axis noise: checks unwanted movement in non-target axis.

## Practical Notes

- `plt.show()` is used for notebook rendering.
- Batch notebook explicitly calls `plt.close(fig)` to reduce memory pressure in long runs.
- If required columns are missing, the notebook prints clear skip/error messages.
