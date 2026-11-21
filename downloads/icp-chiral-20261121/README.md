# ICP D/L-Arginine 3D Waterfall

## 直接下载

- [600 dpi TIFF](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_D_L_waterfall_600dpi.tiff)
- [600 dpi PNG](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_D_L_waterfall_600dpi.png)
- [矢量PDF](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_D_L_waterfall_vector.pdf)
- [统计与处理Excel](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_peak_statistics_and_processing.xlsx)
- [图形文件ZIP](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_D_L_figure_files.zip)
- [完整原始数据、处理记录与图形ZIP](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-chiral-20261121/downloads/icp-chiral-20261121/ICP_D_L_complete_data_and_figures.zip)

## 文件

- ICP_D_L_waterfall_600dpi.tiff：600 dpi、7680×4320、LZW压缩TIFF。
- ICP_D_L_waterfall_600dpi.png：相同分辨率PNG。
- ICP_D_L_waterfall_vector.pdf：真正矢量曲线、内嵌Arial字体，无栅格化图像。
- ICP_peak_statistics_and_processing.xlsx：全部70条扫描、FWHM、组统计、代表选择、平移、电压假设、校验和和Origin绘图数据。
- all_70_scan_peak_statistics.csv / group_summary_statistics.csv：未舍入精度统计。
- D/L_Origin_XYZ_plot.csv：X=V_aligned_mV_assumed，Y=sample_depth，Z=I_normalized；样品深度D=0、L=1.8。
- D/L_all_scans_normalized.npz：完整原始X、150000×35的原始强度与归一化强度、扫描名称，无损保存。
- D/L_representative_full.csv.gz：代表扫描的完整范围数据及平移前后电压坐标。
- Figure_caption_EN/ZH.txt：包含归一化、代表选择、对齐及暂定电压假设的中英文图注，论文使用时请保留这些说明。
- processing_record.json / rendering_record.json / validation_results.json：完整处理与验证记录。
- FigureSpec.yaml：Origin Skill层级配置及数据映射，明确实际渲染软件。

## 关键结果（mV为暂定换算）

| Sample | n | Mean peak (mV) | Sample SD (mV) | Median (mV) | Representative | Representative FWHM (mV) |
| --- | --- | --- | --- | --- | --- | --- |
| D-Arginine | 35 | 132.712286 | 2.560159 | 131.958000 | Y16 | 0.399992 |
| L-Arginine | 35 | 144.895771 | 1.843448 | 144.576000 | Y20 | 0.397719 |

由未舍入均值计算 ΔV=12.183485714 mV。两个峰的图内标注按要求保留3位小数；ΔV没有用舍入后的标注相减。

## 必须保留的解释

电压采用用户指定暂定假设 V_AC(mV)=X×300/150000=X×0.002；这不是文件中已验证的仪器电压标定。
35+35条扫描均完整有效且全部参与统计；D中3条Tukey峰位标记仍保留，没有删去。没有平滑、拟合、重构、补信号或平均峰形。
代表曲线先各自按最大值归一化，再仅整体水平平移至组平均峰位，FWHM不变。主图不是未经处理的原始同时实测双峰谱图。

已调用仓库Origin Skill。当前环境没有Origin本体，用户要求直接解决并给出结果，因此实际渲染为Matplotlib mplot3d。未生成或冒称原生OPJU项目。附Origin可导入CSV及FigureSpec，原始Excel完整保留在完整版的reproducibility/raw目录。

## 复现

进入完整版reproducibility目录，在Python 3.12环境安装requirements.txt，然后依次运行：

```bash
python read_raw.py
python analyze_icp.py
python install_arial.py
python render_waterfall.py
python make_report.py
```

Arial字体文件不随本包再分发。install_arial.py从固定版本的字体包恢复字体，并验证已记录的SHA512完整性；PDF内嵌的字体用于图形内容。原始文件SHA256可在raw_file_metadata.json和统计表中核对。
