from pathlib import Path
import hashlib,json,re,os
import numpy as np
import pandas as pd
from openpyxl import load_workbook

BASE=Path(__file__).resolve().parent
rows=[]; summaries=[]; audits=[]; windows=[]
conditions=[(50,1),(100,1),(100,5),(100,10),(200,1),(200,5)]
for cd,salt in conditions:
    filename=f'{cd}；{salt}.xlsx'
    matches=list(Path(os.environ.get('CD_NACL_INPUT_DIR','/workspace/attachments')).rglob(filename))
    assert len(matches)==1, matches
    path=matches[0]
    wb=load_workbook(path,read_only=True,data_only=True)
    assert len(wb.sheetnames)==1
    ws=wb[wb.sheetnames[0]]
    ws.reset_dimensions()  # Instrument XLSX incorrectly declares dimension A1.
    it=ws.iter_rows(values_only=True)
    headers=next(it)
    assert headers[0]=='x',headers
    cols=[i for i,h in enumerate(headers) if isinstance(h,str) and re.fullmatch(r'y\d+',h)]
    expected=3 if (cd,salt)==(100,1) else 5
    assert [headers[i] for i in cols]==[f'y{i}' for i in range(1,expected+1)],headers
    data=[]; excel_rows=[]
    for rowno,row in enumerate(it,2):
        if row[0] is None:
            assert all(i>=len(row) or row[i] is None for i in cols),f'Unmatched intensity row {rowno}'
            continue
        vals=[row[0]]+[row[i] if i<len(row) else None for i in cols]
        assert all(isinstance(v,(int,float)) and np.isfinite(v) for v in vals),(filename,rowno,vals)
        data.append(vals);excel_rows.append(rowno)
    a=np.array(data,dtype=float)
    assert (np.diff(a[:,0])>0).all()
    mask=(a[:,0]>=589.9)&(a[:,0]<=590.5)
    win=a[mask];source_rows=np.array(excel_rows)[mask]
    assert len(win)>0
    group=[]
    for j,c in enumerate(cols,1):
        heights=win[:,j]; peak=heights.max(); ties=np.flatnonzero(heights==peak)
        k=ties[0]
        rec=dict(condition=f'{cd}/{salt}',CD_uM=cd,NaCl_uM=salt,acquisition_index=j,column=headers[c],peak_mz=win[k,0],peak_intensity_au=peak,source_file=filename,sheet=ws.title,excel_row=int(source_rows[k]),excel_column=c+1,tie_count=len(ties),all_max_mz=';'.join(format(v,'.15g') for v in win[ties,0]))
        rows.append(rec);group.append(peak)
    sd=np.std(group,ddof=1);mean=np.mean(group)
    summaries.append(dict(condition=f'{cd}/{salt}',CD_uM=cd,NaCl_uM=salt,n=expected,mean_au=mean,SD_au=sd,CV_percent=100*sd/mean,mean_million=mean/1e6,SD_million=sd/1e6))
    display=(a[:,0]>=589.8)&(a[:,0]<=591.6)
    view=pd.DataFrame(a[display],columns=['mz']+[headers[c] for c in cols]);view['mean_raw_au']=a[display,1:].mean(axis=1);view.insert(0,'condition',f'{cd}/{salt}')
    windows.append(view)
    audits.append(dict(file=filename,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sheet=ws.title,rows=len(a),mz_min=a[0,0],mz_max=a[-1,0],n=expected,window_points=int(mask.sum()),plot_points=int(display.sum()),missing_values=0))
    wb.close()
peaks=pd.DataFrame(rows);summary=pd.DataFrame(summaries)
heat=summary.pivot(index='CD_uM',columns='NaCl_uM',values='mean_million').reindex(index=[50,100,200],columns=[1,5,10])
assert len(peaks)==28
checks={'highest_mean_is_200_1':summary.loc[summary.mean_au.idxmax(),'condition']=='200/1','100_5_exceeds_100_1_and_100_10':bool(summary.set_index('condition').loc['100/5','mean_au']>summary.set_index('condition').loc[['100/1','100/10'],'mean_au'].max()),'total_columns_28':len(peaks)==28,'unmeasured_cells_3':int(heat.isna().sum().sum())==3}
peaks.to_csv(BASE/'individual_peaks.csv',index=False);summary.to_csv(BASE/'summary.csv',index=False);heat.to_csv(BASE/'heatmap_million.csv',na_rep='NA')
with pd.ExcelWriter(BASE/'quantification.xlsx',engine='openpyxl') as writer:
    peaks.to_excel(writer,sheet_name='Individual_peaks',index=False)
    summary.to_excel(writer,sheet_name='Summary',index=False)
    heat.to_excel(writer,sheet_name='Heatmap_x1e6',na_rep='NA')
    pd.DataFrame(audits).to_excel(writer,sheet_name='Input_audit',index=False)
    for v in windows:v.to_excel(writer,sheet_name='Spectrum_'+v.condition.iloc[0].replace('/','_'),index=False)
pd.concat(windows,ignore_index=True).to_csv(BASE/'spectra_window.csv',index=False)
(BASE/'audit.json').write_text(json.dumps({'inputs':audits,'checks':checks,'method':'Inclusive 589.9–590.5; max per acquisition; sample SD ddof=1; all ties recorded, first used for source row; no preprocessing, normalization or exclusion; scaling 1e6 only for display; no inferential tests.'},indent=2),encoding='utf-8')
print(summary.to_string(index=False));print(checks)
