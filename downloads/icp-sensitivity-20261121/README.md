# ICP 峰位异常候选与剔除敏感性分析

主推荐 D0/L0，保留全部70条。D有IQR候选Y17/Y27/Y33，修正Z候选Y17/Y27；L均无候选。D3/L0仅作敏感性对照，不能据此断言采集错误或仪器重复性改善。

请先读 `Analysis_report_ZH.md`，查看 `All_Figures_A_to_F_preview.png` 或六张独立图片；全部统计见 `ICP_Sensitivity_All_Results.xlsx`。各组11档嵌套方案、121组合及全部保留/删除编号均可追溯。

所有电压暂按 X×0.002 mV，未经仪器标定确认。峰参数取自原始未对齐信号，不平滑、不拟合。六图实际由 Matplotlib 渲染，TIFF600dpi、PNG、矢量PDF、可编辑SVG均已生成。

**未生成 .opju**：当前Linux没有Origin或Windows桥。`origin/` 的可选Windows导入器仅创建数据工作表，不重建六图，未在Origin执行。请勿将其他格式当作Origin工程。

完整包中的 `reproducibility/` 保留原始Excel与脚本。复现：先在该目录运行 `read_raw.py`、`analyze_sensitivity.py`，如系统无Arial则运行 `install_arial.py`，随后运行 `render_sensitivity.py` 和 `make_report.py`。`validate_outputs.py`验证科学统计与导出属性；`package_outputs.py`打包。Arial字体文件不随包分发，PDF已嵌入子集，SVG文字编辑需要本地字体。

## GitHub 直接下载

- [完整资料 ZIP](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/ICP_Sensitivity_Complete.zip)
- [全部 TIFF/PNG/PDF/SVG 图片](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/ICP_Sensitivity_Figures.zip)
- [仅 PNG 图片](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/ICP_Sensitivity_PNG.zip)
- [全部 Excel 统计表](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/ICP_Sensitivity_Excel_Tables.zip)
- [统计总表](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/ICP_Sensitivity_All_Results.xlsx)
- [六图 PDF](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-sensitivity-20261121/downloads/icp-sensitivity-20261121/All_Figures_A_to_F_vector.pdf)
