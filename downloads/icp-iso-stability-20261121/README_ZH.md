# D/L 精氨酸与维拉帕米 ISO 强度稳定性

仅输出两张科学图，均为箱线图叠加全部真实散点：

1. `01_Arginine_Target_Stability`：精氨酸目标离子，D/L 同图。
2. `02_Verapamil_Relative_Intensity`：维拉帕米介质离子（约 m/z455），D/L 同图。

每组35次测量，70条扫描均保留，逐扫描分别提取两离子的峰高，共140条真实峰记录。没有额外平滑、拟合、峰形重建、峰位对齐、基线扣除或扫描剔除。旧的空白 L 上传没有参与本次分析。

## 结果

| 离子 | D组峰高均值 ± 样本SD | D组RSD | L组峰高均值 ± 样本SD | L组RSD |
|---|---:|---:|---:|---:|
| 精氨酸 | 10,701,988.914 ± 288,199.043 | 2.692948% | 12,607,428.829 ± 1,169,172.567 | 9.273680% |
| 维拉帕米 | 4,157,539.943 ± 320,162.659 | 7.700772% | 2,871,225.086 ± 231,417.571 | 8.059890% |

本次导出数据中，精氨酸目标信号 D 组的相对波动小于 L 组；维拉帕米两组的波动接近。这里只作描述性比较，没有进行显著性检验，也不将RSD较小解释为仪器本身或对映体本征稳定性提高。

## 相对强度定义

两图统一使用：**相对强度(%) = 每次该离子峰高 / 本组该离子35次峰高的均值 × 100**。

100%灰虚线表示各组自身均值。每次测量的峰高仍可高于或低于100%；这不是逐条谱把目标峰强制设为100%。该正比例缩放不改变RSD。RSD=100×样本SD/均值，SD采用ddof=1。

这一归一化用于比较各组自身的强度波动，不能从图上的100%判断D/L绝对信号相同。原始导出峰高及其均值/SD均保留在Excel和CSV中。

`Supplement_Ver_to_Arg_Ratio.csv` 和Excel另附每次 `I_Ver/I_Arg×100`，仅作相对丰度补充；它同时受分母精氨酸波动影响，不代替维拉帕米独立信号稳定性的主图。

## 图形说明

横轴D/L样品；纵轴相对于该组该离子平均峰高的百分比。两图纵轴统一80%–145%，便于比较波动大小。箱体为Q1–Q3，中线为中位数，须为1.5IQR范围内最远观测值。35个测量点全部单独绘出，超出须的点仍保留。散点只做水平方向避让，实际强度纵坐标未改变。上方为完整35次数据的RSD。

Arial字体，D=#2166AC，L=#D73027，白底。PNG/TIFF为600dpi、4560×3480像素；另附矢量PDF/SVG。实际使用Matplotlib渲染，没有原生Origin工程。

## 离子提取与坐标依据

用户确认低质荷比强峰为精氨酸，高质荷比强峰为约455的维拉帕米。

- D文件保留Raw=True，第一列为0–94999的原始采样索引，使用固定原始X窗：精氨酸12000–13000、维拉帕米40000–41000。没有把索引直接当作m/z，也没有套用L的标定。
- 新L文件Raw=False，第一列已经是导出的m/z网格50–999.989996，使用170–180与450–460固定窗口。
- 各窗取每条扫描的实际最大峰高。所有扫描在均值谱主峰附近±45行的较窄窗口重提取均得到完全相同峰高，主峰不存在强邻峰竞争；最强竞争邻峰低于主峰0.66%。
- L实测精氨酸主峰约174.863–174.893，维拉帕米约455.160–455.180，按实测位置取峰，不人为移动到理论位置。

**采集/导出设置限制：D与L的Raw开关不同，Relative均为False。该开关背后的仪器预处理影响尚未核实；这里的结论严格限于当前导出信号。若要归因于样品或添加剂本身，应统一并核实采集、信号处理与导出设置。**扫描序号来自Y1–Y35，没有额外时间戳或扫描独立性证明。

## 文件与可追溯性

`ISO_D_L_Stability_Data.xlsx` 含四组汇总、140条逐次峰记录、两离子各70条记录、70个Ver/Arg比值、方法及原始文件SHA256。四份原始局部窗口CSV.GZ可直接导入分析软件。完整包保存有效原始D/L Excel、读取/处理脚本、输入元数据、独立复核及处理记录。原始文件未覆盖。

独立复核91项全部通过：原始逐次峰高、SD/RSD、均值归一、比值、原始局部信号与Excel行数均一致。单独的格式检查还核对600dpi、PDF字体嵌入和矢量属性。

## GitHub 下载

- [精氨酸PNG](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/01_Arginine_Target_Stability_600dpi.png)
- [维拉帕米PNG](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/02_Verapamil_Relative_Intensity_600dpi.png)
- [两张图全部图片格式](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/ISO_D_L_Two_Figures.zip)
- [仅两张PNG](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/ISO_D_L_Two_PNG.zip)
- [完整数据与处理记录](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/ISO_D_L_Complete.zip)
- [统计Excel](https://github.com/yy8jiuk25m23/originplot-skill/raw/refs/heads/icp-iso-stability-20261121/downloads/icp-iso-stability-20261121/ISO_D_L_Stability_Data.xlsx)
