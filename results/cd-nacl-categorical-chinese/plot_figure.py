from pathlib import Path
import os,json,warnings
os.environ.setdefault('MPLCONFIGDIR','/tmp/originplot-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image
BASE=Path(__file__).resolve().parent
font=Path(os.environ.get('CD_NACL_FONT','/workspace/cd-nacl-six-chinese/fonts/SourceHanSansSC-Regular.otf'))
assert font.is_file(),'Provide official SourceHanSansSC-Regular.otf via CD_NACL_FONT'
font_manager.fontManager.addfont(str(font));font_name=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.family':[font_name,'DejaVu Sans'],'font.size':10,'axes.labelsize':11,'axes.linewidth':.8,'axes.unicode_minus':False,'path.simplify':False,'savefig.facecolor':'white'})
p=pd.read_csv(BASE/'individual_peaks.csv');s=pd.read_csv(BASE/'summary.csv');audit=json.loads((BASE/'audit.json').read_text())
order=[(50,1),(100,1),(100,5),(100,10),(200,1),(200,5)]
s=s.set_index(['CD_uM','NaCl_uM']).loc[order].reset_index()
assert len(s)==6 and len(p)==s.n.sum()
colors=['#3775BA','#0F4D92','#26805C','#B43F3F','#588BB9','#50A47A']
fig,ax=plt.subplots(figsize=(230/25.4,155/25.4))
fig.subplots_adjust(left=.095,right=.97,bottom=.18,top=.80)
fig.suptitle('不同环糊精与 NaCl 浓度组合对 m/z=590.2 目标离子峰强度的梯度影响',fontsize=13.2,y=.965)
# Equal spacing denotes named experimental categories, not a continuous concentration axis.
xs=np.arange(1,7,dtype=float)
line=ax.plot(xs,s.mean_million,color='#777777',lw=1.05,zorder=1)[0]
all_drawn=[]
for i,(row,color) in enumerate(zip(s.itertuples(),colors),1):
    group=p[(p.CD_uM==row.CD_uM)&(p.NaCl_uM==row.NaCl_uM)].sort_values('acquisition')
    vals=group.peak_intensity_au.to_numpy()/1e6
    assert len(vals)==row.n
    # Keep the mean/error-bar centre free of raw markers; Y is never changed.
    if len(vals)==5:offset=np.array([-.22,-.13,.12,.21,.30])
    elif len(vals)==1:offset=np.array([.17])
    else:
        nleft=len(vals)//2
        offset=np.r_[np.linspace(-.26,-.13,nleft),np.linspace(.13,.30,len(vals)-nleft)]
    raw=ax.scatter(i+offset,vals,s=29,facecolors='white',edgecolors=color,linewidths=1.1,zorder=3)
    all_drawn.extend(raw.get_offsets()[:,1].tolist())
    ax.errorbar(i,row.mean_million,yerr=row.SD_million,fmt='o',color=color,ms=6.5,mec='white',mew=.65,elinewidth=1.35,capsize=4,capthick=1.1,zorder=5)
labels=[f'CD {cd} μM\nNaCl {salt} μM' for cd,salt in order]
ax.set_xticks(xs,labels,fontsize=9.5);ax.tick_params(axis='x',pad=9,length=4)
ax.get_xticklabels()[3].set_color(colors[3]);ax.get_xticklabels()[3].set_fontweight('bold')
ax.set(xlim=(.48,6.52),ylim=(0,15.5),xlabel='',ylabel='目标离子峰强度（×10⁶）')
ax.set_yticks([0,3,6,9,12,15]);ax.tick_params(axis='y',length=4,pad=5)
ax.spines[['top','right']].set_visible(False)
legend=[Line2D([],[],color='#777777',marker='o',mfc='white',mec='#555555',ls='none',ms=5,label='单次采集'),Line2D([],[],color='#555555',marker='o',lw=1,ms=5,label='均值 ± 样本标准差')]
fig.legend(handles=legend,loc='upper center',bbox_to_anchor=(.535,.89),ncol=2,frameon=False,fontsize=9.5,columnspacing=3,handlelength=2)
assert len(all_drawn)==len(p) and np.allclose(sorted(all_drawn),sorted(p.peak_intensity_au.to_numpy()/1e6))
assert p.peak_intensity_au.max()/1e6<15.5 and (s.mean_million-s.SD_million).min()>0 and (s.mean_million+s.SD_million).max()<15.5
assert len(fig.axes)==1 and np.allclose(line.get_ydata(),s.mean_million)
assert not ax.texts and ax.get_xlabel()==''
with warnings.catch_warnings():
    warnings.filterwarnings('error',message='Glyph .* missing from font')
    fig.savefig(BASE/'六组试剂浓度组合_中文梯度散点图.png',dpi=600)
plt.close(fig)
with Image.open(BASE/'六组试剂浓度组合_中文梯度散点图.png') as im:
    assert all(abs(v-600)<1 for v in im.info['dpi'])
    print('PNG:',im.size,im.info['dpi'])
print('PASS: single panel, six ordered categories, all original points, one mean-connection line; font:',font_name)
