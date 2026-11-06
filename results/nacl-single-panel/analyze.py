from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import hashlib,json,os
import numpy as np
import pandas as pd
BASE=Path(__file__).resolve().parent
inputs=json.loads((BASE/'inputs.json').read_text())
peaks=[];audit=[];windows=[]
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for item in inputs:
 path=Path(os.environ.get('NACL_INPUT_DIR',item['directory']))/item['filename']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'Input changed'
 with ZipFile(path) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   strings=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
  sheet=ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets/s:sheet',ns).attrib['name']
  records=[];headers={};rowids=[]
  for row in root.findall('s:sheetData/s:row',ns):
   cells={}
   for c in row.findall('s:c',ns):
    col=c.attrib['r'].rstrip('0123456789');v=c.find('s:v',ns)
    if v is not None:cells[col]=strings[int(v.text)] if c.attrib.get('t')=='s' else float(v.text)
    elif c.attrib.get('t')=='inlineStr':cells[col]=''.join(c.find('s:is',ns).itertext())
   if row.attrib['r']=='1':headers=cells;continue
   if isinstance(cells.get('A'),(float,int)):
    vals=[cells.get(c) for c in 'ABCDEF']
    assert all(isinstance(v,(float,int)) and np.isfinite(v) for v in vals),(item['filename'],row.attrib['r'],vals)
    records.append(vals);rowids.append(int(row.attrib['r']))
  assert [headers.get(c) for c in 'ABCDEF']==['x','y1','y2','y3','y4','y5'],headers
  a=np.array(records);assert (np.diff(a[:,0])>0).all()
  mask=(a[:,0]>=590.10)&(a[:,0]<=590.32);w=a[mask];rs=np.array(rowids)[mask]
  assert len(w)>2
  for j in range(1,6):
   v=w[:,j];k=int(np.argmax(v));local=np.flatnonzero((v[1:-1]>v[:-2])&(v[1:-1]>=v[2:]))+1
   assert 0<k<len(w)-1 and k in local,(item['filename'],j,'no interior apex')
   assert len(local)==1,(item['filename'],j,'ambiguous local maxima',local)
   peaks.append(dict(NaCl_uM=item['NaCl_uM'],CD_uM=100,acquisition=j,column=f'y{j}',peak_mz=w[k,0],peak_intensity_au=v[k],source_file=path.name,sheet=sheet,excel_row=int(rs[k]),excel_column=j+1,local_maxima_in_window=len(local)))
  df=pd.DataFrame(w,columns=['mz','y1','y2','y3','y4','y5']);df.insert(0,'NaCl_uM',item['NaCl_uM']);windows.append(df)
  audit.append(dict(file=path.name,sha256=item['sha256'],rows=len(a),n=5,window_points=len(w)))
p=pd.DataFrame(peaks);stats=p.groupby('NaCl_uM').peak_intensity_au.agg(n='count',mean_au='mean',SD_au='std').reset_index();stats['CV_percent']=stats.SD_au/stats.mean_au*100;stats['mean_million']=stats.mean_au/1e6;stats['SD_million']=stats.SD_au/1e6
assert len(p)==15 and stats.n.tolist()==[5,5,5]
decrease=(1-stats.set_index('NaCl_uM').loc[10,'mean_au']/stats.set_index('NaCl_uM').loc[5,'mean_au'])*100
p.to_csv(BASE/'individual_peaks.csv',index=False);stats.to_csv(BASE/'summary.csv',index=False);pd.concat(windows).to_csv(BASE/'target_window.csv',index=False)
with pd.ExcelWriter(BASE/'quantification.xlsx',engine='openpyxl') as writer:
 p.to_excel(writer,sheet_name='Individual_peaks',index=False);stats.to_excel(writer,sheet_name='Summary',index=False);pd.DataFrame(audit).to_excel(writer,sheet_name='Input_audit',index=False)
 for df in windows:df.to_excel(writer,sheet_name=f'NaCl_{int(df.NaCl_uM.iloc[0])}_window',index=False)
(BASE/'audit.json').write_text(json.dumps(dict(inputs=audit,window_mz=[590.10,590.32],decrease_10_vs_5_percent=decrease,peak_mz_range=[p.peak_mz.min(),p.peak_mz.max()],all_15_peaks_single_interior_local_maximum=True,preprocessing='none',SD='sample ddof=1',inferential_tests='none'),indent=2))
print(stats.to_string(index=False));print('Decrease 10 vs 5 (%)',decrease)
