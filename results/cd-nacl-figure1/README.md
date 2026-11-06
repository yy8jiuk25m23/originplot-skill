> **历史版本：**本目录未包含用户后续确认的最新50/1与100/1数据归属互换更正。请使用[最新更正后的单图与统计](../cd-nacl-categorical-chinese/README.md)。

> **Superseded input:** the user replaced the 200/5 μM file. This historical result uses the old file and must not be used for the corrected experiment. See [corrected target-ion results](../cd-nacl-target-ion/README.md).

# CD–NaCl mass-spectrometry quantification — Figure 1 preparation

Status: quantitative analysis and Python-rendered 2×2 Figure 1 completed. The user accepted the proposed design and delegated renderer choice. PNG/TIFF are 600 dpi (4724×3897 pixels, 200×165 mm nominal); PDF and SVG are vector exports. A real OPJU remains unavailable because this host has no Windows Origin runtime.

## Method

Original six XLSX files remain unchanged in the uploaded attachments. Input filenames and SHA256 hashes are recorded in audit.json and the Input_audit Excel worksheet. Only x and explicitly named y1–yN columns were read; UI Settings and other auxiliary cells were excluded. Instrument files declare worksheet dimensions as A1, so the reader resets dimensions to read actual stored rows. No original data points were removed or altered. Source data were required to be numeric, finite, and ordered by increasing m/z; failure would stop processing.

For each original intensity column, peak height is the largest recorded intensity within the inclusive m/z window 589.9–590.5. No peak fitting or sub-grid peak estimation was performed. All maximum locations are recorded if tied, with the first occurrence used for the source-cell reference. Mean is the arithmetic mean of these per-column maxima; SD is sample SD (n−1 denominator); CV is 100×SD/mean. These are distinct from the maximum of the pointwise mean spectrum used in panel A.

There are 28 acquisition columns: 100/1 μM has three, and each other condition has five. Their independence and temporal ordering are unconfirmed. No inferential statistics, ion formula assignment, smoothing, baseline correction, normalization, interpolation, or outlier exclusion was applied. Dividing by 10^6 is only an axis-unit conversion. Unmeasured concentration pairs remain NA.

## Results

| CD/NaCl (μM) | n | Mean (×10^6 a.u.) | Sample SD (×10^6 a.u.) | CV (%) |
|---|---:|---:|---:|---:|
| 50/1 | 5 | 3.387994 | 0.287572 | 8.487979 |
| 100/1 | 3 | 5.794225 | 0.631000 | 10.890156 |
| 100/5 | 5 | 8.366888 | 0.557101 | 6.658407 |
| 100/10 | 5 | 3.288496 | 0.290610 | 8.837165 |
| 200/1 | 5 | 11.193279 | 0.245994 | 2.197695 |
| 200/5 | 5 | 7.031410 | 0.416506 | 5.923510 |

200/1 μM has the highest mean response and lowest observed CV among the tested conditions. At 100 μM CD, the 5 μM NaCl condition has higher mean response than 1 and 10 μM NaCl. These descriptive results do not establish a global optimum or statistical significance. Untested concentration combinations must not be inferred as measured results.

## Deliverables

- quantification.xlsx: individual peaks with original sheet/row/column, summary, heatmap, input audit, and six unmodified spectral windows plus pointwise means.
- individual_peaks.csv: all 28 peak heights and locations in original units.
- summary.csv: six groups, means, sample SDs, CVs and n.
- spectra_window.csv: measured 589.8–591.6 m/z window and pointwise raw mean per condition; acquisition columns not present in a group remain empty.
- heatmap_million.csv: 3×3 categorical concentration response grid; three NA cells.
- FigureSpec.yaml: accepted 2×2 figure plan, with actual rendering recorded.
- Figure1.png / Figure1.tiff: full 600 dpi figure.
- Figure1.pdf / Figure1.svg: vector figure.
- Figure1_preview.png: lightweight preview.
- plot_figure.py: Python renderer; all plotted line vertices are measured points, with path simplification disabled. Shared group legend applies to A/B/D.
- requirements.txt: versions used for analysis and plotting.
- analyze.py: reproducible analysis using Python, pandas, NumPy and openpyxl; currently locates original uploaded attachments under /workspace/attachments.

## Rendering limitation

This cloud host is Linux. OriginPlot uses external Windows Python plus installed/licensed Origin/OriginPro and COM automation. No Windows bridge is configured. A real editable OPJU cannot be produced here. The user accepted the proposed design and delegated the rendering decision; the supplied Python-rendered figures do not claim to be Origin exports. No dummy or renamed OPJU file is supplied. To obtain an editable OPJU, import the workbook into an installed/licensed Windows Origin and reproduce the accepted FigureSpec. This remaining deliverable has not been completed.

## Reproduce

Install requirements.txt, then run `python analyze.py` with originals available under /workspace/attachments (or set CD_NACL_INPUT_DIR to a directory containing the six unchanged files). Run `python plot_figure.py` from any directory; outputs are written alongside the scripts. All 28 peak heights and positions were independently cross-checked against the XML stored in the XLSX archives; six group means and sample SDs were also rechecked. Original uploads are not duplicated in this results directory; verify them using the recorded SHA256 hashes.

## Proposed figure caption

**Figure 1. CD–NaCl concentration combinations and mass-spectrometric response.** (A) Pointwise mean raw ion intensity spectra for six measured concentration combinations. (B) Individual acquisition-column maxima within m/z 589.9–590.5, with mean ± sample SD. Horizontal offsets separate individual observations and do not alter intensity values. (C) Mean peak intensity across the tested concentration grid; NA indicates unmeasured combinations. (D) Peak intensity by acquisition-column index. The 100/1 μM condition contains three columns; all other conditions contain five. Acquisition order is not interpreted as elapsed time, and independence of columns is unconfirmed. No smoothing, baseline correction, normalization, outlier removal or inferential tests were applied.
