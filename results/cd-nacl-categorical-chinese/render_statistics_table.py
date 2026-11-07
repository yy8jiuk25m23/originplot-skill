from pathlib import Path
import os,warnings
os.environ.setdefault('MPLCONFIGDIR','/tmp/originplot-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
from PIL import Image
BASE=Path(__file__).resolve().parent
font=Path(os.environ.get('CD_NACL_FONT','/workspace/cd-nacl-six-chinese/fonts/SourceHanSansSC-Regular.otf'))
font_manager.fontManager.addfont(str(font));family=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'savefig.facecolor':'white'})
order=[(50,1),(100,1),(100,5),(100,10),(200,1),(200,5)]
s=pd.read_csv(BASE/'summary.csv').set_index(['CD_uM','NaCl_uM']).loc[order].reset_index()
t=pd.DataFrame({'试剂浓度组合':[f'CD {r.CD_uM} μM + NaCl {r.NaCl_uM} μM' for r in s.itertuples()], '均值（×10⁶）':s.mean_million, 'CV（%）':s.CV_percent})
assert len(t)==6
rows=[[str(r.iloc[0]),f'{float(r.iloc[1]):.3f}',f'{float(r.iloc[2]):.1f}'] for _,r in t.iterrows()]
fig,ax=plt.subplots(figsize=(200/25.4,95/25.4));fig.subplots_adjust(left=.04,right=.96,bottom=.05,top=.85);ax.axis('off')
fig.suptitle('六组试剂浓度组合的均值与变异系数',fontsize=14,y=.955)
table=ax.table(cellText=rows,colLabels=['试剂浓度组合','均值（×10⁶）','CV（%）'],colWidths=[.56,.25,.19],cellLoc='center',loc='center',bbox=[0,.01,1,.98])
table.auto_set_font_size(False);table.set_fontsize(11)
for (row,col),cell in table.get_celld().items():
    cell.set_edgecolor('#D6DDE4');cell.set_linewidth(.6)
    cell.PAD=.08
    if row==0:
        cell.set_facecolor('#E8EEF4');cell.get_text().set_weight('bold');cell.get_text().set_color('#243B53')
    else:
        cell.set_facecolor('#FFFFFF' if row%2 else '#F8FAFC');cell.get_text().set_color('#242424')
        if col==0:cell.get_text().set_ha('left')
for row_idx,values in enumerate(rows,1):
    for col,value in enumerate(values):assert table[row_idx,col].get_text().get_text()==value
with warnings.catch_warnings():
    warnings.filterwarnings('error',message='Glyph .* missing from font')
    fig.savefig(BASE/'均值与CV汇总表.png',dpi=600)
plt.close(fig)
with Image.open(BASE/'均值与CV汇总表.png') as im:
    assert all(abs(v-600)<1 for v in im.info['dpi']);print(im.size,im.info['dpi'])
print('PASS: all six corrected conditions, exact formatted mean/CV, Chinese font, 600 dpi')
