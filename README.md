# VOG Data Analysis Pipeline

This project implements a pipeline to parse, analyze, and visualize Vestibulo-Ocular Gaze (VOG) data from CSV files. The primary goal is to assess eye-tracking performance by comparing eye movement against a moving target.

<div align="center">
    <img src="https://github.com/user-attachments/assets/b1fe42e7-5aaf-4612-9c48-7c8d88dec418">
</div>

---

## Navigating the Core Analysis Logic

To efficiently understand the data processing pipeline **before** diving into the main executor code (e.g., `src/app/main_app.py`), we recommend reviewing the key methods within the `src/` directory in the specified order. These three methods represent the foundational stages of the analysis.

---



## Data Tree

#### Data should be like this below

<details>
<summary>📂 Click to expand the Data Directory Tree</summary>

```text
data/
└── sample_csv
    ├── HC_csv_24_25
    │   ├── 20240329_084111_1324721_
    │   │   ├── PD VOG -_Horizontal Saccade A.csv
    │   │   ├── PD VOG -_Horizontal Saccade B (anti).csv
    │   │   ├── PD VOG -_Horizontal Saccade B.csv
    │   │   ├── PD VOG -_Horizontal Saccade R.csv
    │   │   ├── PD VOG -_Vertical Saccade A.csv
    │   │   ├── PD VOG -_Vertical Saccade B (anti).csv
    │   │   ├── PD VOG -_Vertical Saccade B.csv
    │   │   └── PD VOG -_Vertical Saccade R.csv
    │   ├── 20240329_094040_1073209_
    │   ...
    └── MCI_csv_25_26
        ├── 20250701_091148_644377_
        │   ├── PD VOG -_Horizontal Gaze Left30, 20sec.csv
        │   ├── PD VOG -_Horizontal Gaze Right30, 20sec.csv
        │   ├── PD VOG -_Horizontal Saccade A.csv
        │   ├── PD VOG -_Horizontal Saccade B (anti).csv
        │   ├── PD VOG -_Horizontal Saccade B.csv
        │   ├── PD VOG -_Horizontal Saccade R.csv
        │   ├── PD VOG -_Vertical Gaze  Down15, 20sec.csv
        │   ├── PD VOG -_Vertical Gaze  Up15, 20sec.csv
        │   ├── PD VOG -_Vertical Saccade A.csv
        │   ├── PD VOG -_Vertical Saccade B (anti).csv
        │   ├── PD VOG -_Vertical Saccade B.csv
        │   └── PD VOG -_Vertical Saccade R.csv
```
</details>

### 1. Data Parsing: `src/Parser/data_parser.py`

## Notebooks
*   **Key Method:** `VOGRobustParser.parse()`
*   **Purpose:** This method serves as the entry point for data ingestion. It reads raw CSV files, standardizes column names, and loads the data into a pandas DataFrame. From a statistical perspective, this is the crucial **Data Loading and Sanitization** step, ensuring data consistency and readiness for subsequent analytical operations.

---

## Updates

### VOG Visualization through Spectrograms

Means of spectrograms drawin with different window sizes

<img width="5180" height="2458" alt="Combined_32_Panels_Comprehensive_Dashboard" src="https://github.com/user-attachments/assets/8d7f91a6-7c84-4ca6-976f-847f6e6778f3" />

<img width="5180" height="2458" alt="Combined_32_Panels_Comprehensive_Dashboard" src="https://github.com/user-attachments/assets/89f26ce2-ac33-4ba4-a947-4bc94d3f1bdb" />

<p align="center">Upper one is drawn with 16 size window, Down one is drawn with 48 size window

---
### 2. Feature Engineering & Analysis: `src/Analyzer/vog_data_analyzer.py`

*   **Key Method:** `VOGDomainAnalyzer.analyze()`
*   **Purpose:** This is the central analysis engine. The `analyze` method processes the parsed DataFrame to derive key features:
    **Anti Saccade has the opposite handler modification(df -> -df)**
    1.  **Determines Primary Axis:** Identifies whether the target's movement is primarily Vertical or Horizontal.
    2.  **Calculates Tracking Error:** Computes the difference between the eye's position and the target's position for both left and right eyes (`Error_L`, `Error_R`). This represents the core performance metric.
    3.  **Identifies Cross-Axis Noise:** Extracts eye movement data from the axis *orthogonal* to the primary target movement. This "noise" is not statistically filtered or removed but is isolated for qualitative visual assessment of off-axis deviations, providing insight into potential artifacts or unintended eye movements.
    *   This method transforms raw time-series data into a structured format with engineered features, preparing it for visual interpretation.

---

### 3. Data Visualization: `src/Visualizer/visualizer.py`

---

<div align="center">
<img width="1589" height="1145" alt="output" src="https://github.com/user-attachments/assets/0b977560-0c6e-4580-8deb-298cd85c1701" />
</div>

<div align="center">
<img width="1589" height="1145" alt="reversed" src="https://github.com/user-attachments/assets/21b95a62-2130-4b47-9913-6aa7b73a9a24" />
</div>

---

*   **Key Method:** `VOGMatplotlibVisualizer.plot()`
*   **Purpose:** This method takes the analyzed `VOGData` object and generates a multi-panel plot using Matplotlib. It visually represents the analysis results, including:
    *   Raw waveforms of target and eye movements.
    *   The calculated eye-tracking error over time.
    *   The identified "cross-axis noise," allowing for visual inspection of movements perpendicular to the intended tracking direction.

---

#### <p align="center">The third one</p>

---

<div align="center">
<img width="861" height="662" alt="스크린샷 2026-03-27 오후 2 05 42" src="https://github.com/user-attachments/assets/2a8fb5d8-1cf1-4702-af8d-862f2617923c" />
</div>
