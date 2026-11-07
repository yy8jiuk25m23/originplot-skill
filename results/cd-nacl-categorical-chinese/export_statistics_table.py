from pathlib import Path
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
BASE=Path(__file__).resolve().parent
order=[(50,1),(100,1),(100,5),(100,10),(200,1),(200,5)]
s=pd.read_csv(BASE/'summary.csv').set_index(['CD_uM','NaCl_uM']).loc[order].reset_index()
table=pd.DataFrame({'试剂浓度组合':[f'CD {r.CD_uM} μM + NaCl {r.NaCl_uM} μM' for r in s.itertuples()], '均值（×10⁶）':s.mean_million, 'CV（%）':s.CV_percent})
# Keep full precision in the cells; display as in the original annotations.
with pd.ExcelWriter(BASE/'均值与CV汇总表.xlsx',engine='openpyxl') as writer:
 table.to_excel(writer,sheet_name='均值与CV',index=False)
 ws=writer.sheets['均值与CV'];ws.freeze_panes='A2';ws.auto_filter.ref='A1:C7'
 ws.column_dimensions['A'].width=37;ws.column_dimensions['B'].width=20;ws.column_dimensions['C'].width=17
 for row in ws:
  for cell in row:
   cell.font=Font(name='微软雅黑',size=11)
   cell.alignment=Alignment(horizontal='left' if cell.column==1 else 'center',vertical='center')
   cell.border=Border(bottom=Side(style='hair',color='DDDDDD'))
 for cell in ws[1]:
  cell.font=Font(name='微软雅黑',size=11,bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='345A7C')
 ws.row_dimensions[1].height=26
 for i in range(2,8):
  ws.row_dimensions[i].height=25;ws.cell(i,2).number_format='0.000';ws.cell(i,3).number_format='0.0'
  if i%2==0:
   for cell in ws[i]:cell.fill=PatternFill('solid',fgColor='F4F7FA')
 ws.print_options.horizontalCentered=True;ws.sheet_properties.pageSetUpPr.fitToPage=True
 ws.page_setup.orientation='landscape';ws.page_setup.paperSize=ws.PAPERSIZE_A4;ws.page_setup.fitToWidth=1;ws.page_setup.fitToHeight=1
 ws.print_area='A1:C7'
table.to_csv(BASE/'均值与CV汇总表.csv',index=False,encoding='utf-8-sig')
roundtrip=pd.read_excel(BASE/'均值与CV汇总表.xlsx')
pd.testing.assert_frame_equal(roundtrip,table,check_exact=False,rtol=1e-13)
print(table.to_string(index=False));print('PASS: full-precision mean/CV workbook verified')
