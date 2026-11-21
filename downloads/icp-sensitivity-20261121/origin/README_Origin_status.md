# Origin 原生工程状态

本任务计算环境为 Linux，没有 Windows Origin 安装、Automation/COM 运行时或可用的 Windows 桥。Origin Skill 明确要求：“External mode must run in Windows Python.” 因此本环境没有生成或验证任何 `.opju`；不得将其他格式改名为 `.opju`。

六张最终图的实际渲染软件由主分析记录注明。所有 CSV 与 Excel 可导入 Origin，SVG 可逐对象编辑，但这些文件不是 Origin 原生工程。

附带 `build_origin_data_project.py` 是可选的 **Windows 数据工程导入器**，仅完成语法检查，未在 Origin 运行。其 `new_sheet`、`from_df`、`new`、`save`、`set_show` API 已与公开发布的 originpro 1.1.15 源码核对。它将给定目录中的所有 CSV 原样导入可编辑 Origin 工作表，再由真正的 Origin 保存为新 `.opju`。它不重新筛选数据，也不重建六张图页，不能当作已交付的完整图形工程。

运行前需要 Windows、已安装且有许可的 Origin，以及 originpro、pandas。具体命令见脚本开头。运行器拒绝覆盖已有工程，Origin 保持打开。原始 Excel 文件不由该导入器修改。
