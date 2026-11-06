from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import hashlib,json,os
import numpy as np
import pandas as pd
BASE=Path(__file__).resolve().parent
inputs=json.loads((BASE/'inputs.json').read_text())
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
peaks=[];audits=[];windows=[]
for inp in inputs:
    path=Path(os.environ.get('CD_NACL_INPUT_DIR',inp['directory']))/inp['filename']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==inp['sha256'],f'Input hash mismatch: {path.name}'
    with ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(s.itertext()) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        book=ET.fromstring(z.read('xl/workbook.xml'))
        sheets=book.findall('s:sheets/s:sheet',ns)
        assert len(sheets)==1
        sheet=sheets[0].attrib['name']
        root=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        data=[];source_rows=[];headers={}
        for row in root.findall('s:sheetData/s:row',ns):
            cells={}
            for cell in row.findall('s:c',ns):
                col=cell.attrib['r'].rstrip('0123456789');v=cell.find('s:v',ns)
                if v is not None:
                    cells[col]=strings[int(v.text)] if cell.attrib.get('t')=='s' else float(v.text)
                elif cell.attrib.get('t')=='inlineStr':
                    cells[col]=''.join(cell.find('s:is',ns).itertext())
            if row.attrib['r']=='1':headers=cells;continue
            if cells.get('A') is None:
                assert not any(isinstance(cells.get(c),(float,int)) for c in 'BCDEF'),'Intensity without m/z'
                continue
            assert isinstance(cells['A'],(float,int))
            values=[cells.get(c) for c in 'ABCDEF']
            assert all(isinstance(v,(float,int)) and np.isfinite(v) for v in values),(path.name,row.attrib['r'],values)
            data.append(values);source_rows.append(int(row.attrib['r']))
        assert [headers.get(c) for c in 'ABCDEF']==['x','y1','y2','y3','y4','y5'],headers
        assert not any(isinstance(v,str) and v.startswith('y') and k not in 'BCDEF' for k,v in headers.items()),headers
        a=np.array(data);assert (np.diff(a[:,0])>0).all()
        mask=(a[:,0]>=590.10)&(a[:,0]<=590.32);win=a[mask];rs=np.array(source_rows)[mask]
        assert len(win)>2
        for j in range(1,6):
            v=win[:,j];k=int(np.argmax(v));local=np.flatnonzero((v[1:-1]>v[:-2])&(v[1:-1]>=v[2:]))+1
            assert len(local)==1 and k==local[0] and 0<k<len(v)-1,(path.name,j,'ambiguous/edge peak')
            peaks.append(dict(CD_uM=inp['CD_uM'],NaCl_uM=inp['NaCl_uM'],acquisition=j,column=f'y{j}',peak_mz=win[k,0],peak_intensity_au=v[k],source_file=path.name,sheet=sheet,excel_row=int(rs[k]),excel_column=j+1,local_maxima_in_window=len(local)))
        view=pd.DataFrame(win,columns=['mz','y1','y2','y3','y4','y5']);view.insert(0,'NaCl_uM',inp['NaCl_uM']);view.insert(0,'CD_uM',inp['CD_uM']);windows.append(view)
        audits.append(dict(CD_uM=inp['CD_uM'],NaCl_uM=inp['NaCl_uM'],file=path.name,sha256=inp['sha256'],n=5,rows=len(a),window_points=len(win)))
p=pd.DataFrame(peaks)
s=p.groupby(['CD_uM','NaCl_uM']).peak_intensity_au.agg(n='count',mean_au='mean',SD_au='std').reset_index()
s['CV_percent']=s.SD_au/s.mean_au*100;s['mean_million']=s.mean_au/1e6;s['SD_million']=s.SD_au/1e6
assert len(p)==30 and len(s)==6 and (s.n==5).all()
s100=s[s.CD_uM==100].set_index('NaCl_uM')
decrease=100*(1-s100.loc[10,'mean_au']/s100.loc[5,'mean_au'])
p.to_csv(BASE/'individual_peaks.csv',index=False);s.to_csv(BASE/'summary.csv',index=False);pd.concat(windows).to_csv(BASE/'target_window.csv',index=False)
with pd.ExcelWriter(BASE/'quantification.xlsx',engine='openpyxl') as w:
    p.to_excel(w,sheet_name='逐次采集峰高',index=False);s.to_excel(w,sheet_name='六组统计',index=False);pd.DataFrame(audits).to_excel(w,sheet_name='输入文件核查',index=False)
    for v in windows:v.to_excel(w,sheet_name=f'CD{int(v.CD_uM.iloc[0])}_NaCl{int(v.NaCl_uM.iloc[0])}',index=False)
(BASE/'audit.json').write_text(json.dumps(dict(inputs=audits,inclusive_window_mz=[590.10,590.32],all_30_peaks_single_interior_local_maximum=True,CD100_decrease_10_vs_5_percent=decrease,CD100_NaCl10_CV_percent=s100.loc[10,'CV_percent'],peak_mz_range=[p.peak_mz.min(),p.peak_mz.max()],preprocessing='none',SD='sample ddof=1',inferential_tests='none'),indent=2))
print(s.to_string(index=False));print('CD100 NaCl10 vs5 decrease (%)',decrease)
