# Target-ion analysis: CD–NaCl effects at m/z ≈ 590.2

## Revised scope

Figure 1 is a horizontal three-panel controlled-variable comparison of the **target ion only**. The complete nearby mass spectrum, heatmap and acquisition-index curves are excluded. The user previously delegated design and renderer choice; this revision follows the explicitly requested A/B/C comparisons.

Original six XLSX inputs were reread without modification. Only x and explicitly named y1–yN columns were analyzed; UI Settings were excluded. Instrument files incorrectly declare sheet dimensions as A1; the reader resets dimensions before processing. Each acquisition's intensity is its measured maximum in the **inclusive m/z 590.1–590.3** window, not a sum of peaks. Every column has exactly one interior local maximum within that window. Recorded apex positions span 590.1982–590.2682. No window expansion was necessary. All 28 maxima equal the previous broader-window results: narrowing the window changes the analytical scope but not the values for these data. This confirms that previous quantitative values did not combine neighboring peaks.

There is no smoothing, baseline correction, normalization, peak fitting, outlier removal, imputation or significance testing. SD uses n−1; CV=100×SD/mean. Original peak intensities and source cell references are retained. Division by 10^6 is only a display-unit conversion. The 100/1 condition has n=3, all others n=5. Columns are not assumed independent biological replicates or known time intervals.

## Results

| CD/NaCl (μM) | n | Mean ± SD (×10^6 a.u.) | CV (%) |
|---|---:|---:|---:|
| 50/1 | 5 | 3.387994 ± 0.287572 | 8.487979 |
| 100/1 | 3 | 5.794225 ± 0.631000 | 10.890156 |
| 100/5 | 5 | 8.366888 ± 0.557101 | 6.658407 |
| 100/10 | 5 | 3.288496 ± 0.290610 | 8.837165 |
| 200/1 | 5 | 11.193279 ± 0.245994 | 2.197695 |
| 200/5 | 5 | 7.031410 ± 0.416506 | 5.923510 |

- A: At NaCl=1 μM, the mean target-ion response increases over measured CD levels 50, 100, 200 μM.
- B: At CD=100 μM, increasing NaCl from 1 to 5 μM increases mean response by 44.4%; increasing from 5 to 10 μM decreases it by 60.7%.
- C: At CD=200 μM, increasing NaCl from 1 to 5 μM decreases mean response by 37.2%.

The observed effect of increasing NaCl from 1 to 5 μM therefore differs between CD=100 and CD=200 μM. This is a descriptive pattern, not a statistically established interaction or mechanistic conclusion. 200/1 μM gives the highest mean among tested combinations; it is not a demonstrated global optimum. No chemical formula is assigned from m/z alone.

## Figure caption

**Figure 1. Effects of CD and NaCl concentrations on the target-ion signal at m/z ≈ 590.2.** (A) Effect of CD concentration at fixed NaCl=1 μM. (B) Effect of NaCl concentration at fixed CD=100 μM. (C) Effect of NaCl concentration at fixed CD=200 μM. Open circles show individual acquisition-column peak heights within m/z 590.1–590.3; filled circles and error bars show arithmetic mean ± sample SD. All panels share the intensity range 0–13×10^6 a.u. Sample sizes refer to acquisition columns: n=3 for 100/1 μM and n=5 otherwise. Horizontal scatter offsets separate observations without altering intensities. Lines connect measured means as visual guides only; they do not predict unmeasured concentrations. Shared conditions appearing in more than one panel reuse the same observations, not additional replicates. No significance tests were performed.

## Files and reproducibility

- Figure1_target_ion.png / .tiff: 600 dpi, 5433×2244 pixels, nominal 230×95 mm.
- Figure1_target_ion.pdf / .svg: vector files; SVG labels remain editable text.
- quantification.xlsx: all 28 original target peak heights, peak locations, source Excel cells, six-group statistics, input audit and target-window data.
- Origin_import_tables.xlsx and A/B/C CSVs: panel-specific measured X, mean, SD, CV and individual intensities in ×10^6 units. Blank missing acquisition entries remain blank. X positions are actual numeric concentrations.
- individual_peaks.csv / summary.csv: raw-unit quantification and summary.
- spectra_window.csv: numerical target window only for audit; no full-spectrum plot is drawn.
- audit.json: original-file SHA256 hashes and validation.
- analyze.py / plot_figure.py / prepare_origin_tables.py / requirements.txt: scripts and software versions.

Install requirements, set CD_NACL_INPUT_DIR to the directory containing the six original XLSX files (default /workspace/attachments), and run analyze.py, prepare_origin_tables.py, then plot_figure.py. Scripts write beside themselves.

## Origin limitation

The supplied images were rendered by Python/Matplotlib. This Linux environment has no installed Windows Origin/OriginPro or COM bridge. **A genuine editable OPJU project has not been produced.** No placeholder OPJU is supplied. Origin_import_tables.xlsx and the FigureSpec provide data and design for rebuilding in licensed Windows Origin: use numeric X, individual scatter series, connected mean series with SD designated as Y-error, a horizontal 1×3 layout, and shared 0–13 Y limits. The Excel workbook is not an OPJU substitute.
