from pathlib import Path
import pandas as pd
b=Path(__file__).resolve().parent
s=pd.read_csv(b/'summary.csv');p=pd.read_csv(b/'individual_peaks.csv')
with pd.ExcelWriter(b/'Origin_import_tables.xlsx',engine='openpyxl') as w:
 for panel,key,mask in [('A_CD_at_NaCl1','CD_uM',s.NaCl_uM==1),('B_NaCl_at_CD100','NaCl_uM',s.CD_uM==100),('C_NaCl_at_CD200','NaCl_uM',s.CD_uM==200)]:
  q=s[mask].sort_values(key)[[key,'condition','n','mean_million','SD_million','CV_percent']].copy()
  for i in range(1,6):
   lookup=p[p.acquisition_index==i].set_index('condition').peak_intensity_au/1e6
   q[f'acquisition_{i}_million']=q.condition.map(lookup)
  q.to_excel(w,sheet_name=panel,index=False)
  q.to_csv(b/(panel+'.csv'),index=False)
