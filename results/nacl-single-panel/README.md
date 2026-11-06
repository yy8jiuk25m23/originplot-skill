> **历史版本：**本目录未包含用户后续确认的最新50/1与100/1数据归属互换更正。请使用[最新更正后的单图与统计](../cd-nacl-categorical-chinese/README.md)。

# One-figure analysis: NaCl effect at CD = 100 μM

This result supersedes earlier 100/1 and 100/10 analyses, using only the three latest uploads specified by the user. The other three CD conditions are excluded. The 1 and 10 μM input filenames use a full-width colon (：); the 5 μM file uses a full-width semicolon (；). inputs.json records exact filenames and SHA256 hashes to prevent accidental selection of older same-named files.

## Quantification

Each of the three files contains five acquisition columns y1–y5. For each column, select the raw target peak apex in inclusive m/z 590.10–590.32. Every selected apex is an interior local maximum and each window has only one local maximum. No adjacent-peak integration, column addition, normalization, smoothing, baseline correction, outlier removal or imputation is used. All 15 source peak values, positions and original cell coordinates are retained. Standard deviation is the sample SD (n−1); CV=100×SD/mean. Scaling by 10^6 is a display-unit conversion only.

| NaCl (μM) | n | Mean (×10^6 a.u.) | Sample SD (×10^6 a.u.) | CV (%) |
|---|---:|---:|---:|---:|
| 1 | 5 | 1.976907 | 0.118546 | 5.996542 |
| 5 | 5 | 8.366888 | 0.557101 | 6.658407 |
| 10 | 5 | 1.711636 | 1.246347 | 72.816150 |

The observed mean peak intensity decreases by **79.5427%** from 5 to 10 μM NaCl. The 10 μM condition has the largest sample SD and CV of the three conditions. The 5 μM condition has the highest mean response; both 1 and 5 μM have relatively low observed CVs. No hypothesis tests, P values or significance marks are used. Acquisition columns are not assumed to be independent biological replicates, and variability across columns is not equated with a validated temporal drift measurement. Potential salt-related suppression is a hypothesis, not an established mechanism. These data do not establish a global optimum.

## Figure caption

**Effect of NaCl concentration on the intensity and repeatability of the m/z ≈ 590.2 target ion at CD = 100 μM.** Peak intensities were extracted separately from five acquisition columns per condition within m/z 590.10–590.32. Open circles show all individual acquisition values (n=5 per group), filled circles show means, and error bars indicate sample SD. Small horizontal offsets separate observations without changing intensities. Thin lines connect measured means as visual guides and do not predict unmeasured concentrations. At 10 μM NaCl, mean signal was 79.5% lower than at 5 μM, and CV increased to 72.8%, indicating marked signal attenuation and poor within-condition repeatability in these measurements. This pattern is compatible with a potential salt-related signal suppression effect, but does not demonstrate its mechanism. No inferential statistics were performed.

## Deliverables

- Figure_NaCl_CD100.png and .tiff: the same single-panel figure, 600 dpi, 4251×2952 pixels (nominal 180×125 mm).
- Figure_NaCl_CD100.pdf and .svg: vector versions of the same figure.
- quantification.xlsx, individual_peaks.csv, summary.csv, target_window.csv and audit.json: auditable data.
- FigureSpec.yaml: final figure design.
- analyze.py and plot_figure.py: reproducible analysis/plotting; requirements.txt records package versions.

Reproduce with the six software requirements installed: set NACL_INPUT_DIR to a directory containing these three exact input filenames, run analyze.py, then plot_figure.py. Inputs must match the recorded hashes. Without NACL_INPUT_DIR, inputs.json points to the uploaded files in the current cloud workspace. Raw uploads are not duplicated here.

Arial is unavailable on this cloud host; the figure uses the Arial-compatible Liberation Sans font. PDF embeds fonts; SVG keeps labels as editable text. The figure was rendered by Python/Matplotlib. No real OPJU is generated because Windows Origin/OriginPro is unavailable on this Linux host.
