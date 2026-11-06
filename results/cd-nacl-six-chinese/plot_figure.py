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
font_path=Path(os.environ.get('CD_NACL_FONT',str(BASE/'fonts/SourceHanSansSC-Regular.otf')))
assert font_path.is_file(),'Supply the official SourceHanSansSC-Regular.otf via CD_NACL_FONT'
font_manager.fontManager.addfont(str(font_path));font_name=font_manager.FontProperties(fname=str(font_path)).get_name()
plt.rcParams.update({'font.family':[font_name,'DejaVu Sans'],'font.size':10,'axes.labelsize':11,'axes.linewidth':.8,'axes.unicode_minus':False,'path.simplify':False,'savefig.facecolor':'white'})
p=pd.read_csv(BASE/'individual_peaks.csv');s=pd.read_csv(BASE/'summary.csv');a=json.loads((BASE/'audit.json').read_text())
assert len(p)==30 and len(s)==6 and (s.n==5).all()
fig,ax=plt.subplots(figsize=(220/25.4,155/25.4))
fig.subplots_adjust(left=.11,right=.97,bottom=.24,top=.73)
fig.suptitle('不同环糊精与 NaCl 浓度对目标离子峰强度及重复性的影响',fontsize=14,y=.965)
fig.text(.54,.906,'目标离子：m/z ≈ 590.2',ha='center',fontsize=10,color='#444444')
colors={50:'#328C95',100:'#0F4D92',200:'#95508C'}
markers={50:'o',100:'s',200:'D'};offsets={50:-.50,100:0,200:.50}
raw_offsets=np.array([-.32,-.19,.16,.29,.42])
mean_positions=[];actual_points=[]
for cd in [50,100,200]:
    sub=s[s.CD_uM==cd].sort_values('NaCl_uM');x=sub.NaCl_uM.to_numpy()+offsets[cd]
    if len(sub)>1:ax.plot(x,sub.mean_million,color=colors[cd],lw=1.15,alpha=.85,zorder=1)
    for row in sub.itertuples():
        xx=row.NaCl_uM+offsets[cd];vals=p[(p.CD_uM==cd)&(p.NaCl_uM==row.NaCl_uM)].sort_values('acquisition').peak_intensity_au.to_numpy()/1e6
        assert len(vals)==5
        artist=ax.scatter(xx+raw_offsets,vals,s=28,facecolors='white',edgecolors=colors[cd],marker=markers[cd],linewidths=1.05,zorder=3)
        actual_points.extend(artist.get_offsets()[:,1].tolist())
        ax.errorbar(xx,row.mean_million,yerr=row.SD_million,fmt=markers[cd],color=colors[cd],ms=6.5,mec='white',mew=.65,elinewidth=1.3,capsize=3.6,capthick=1.1,zorder=5)
        mean_positions.append((row.CD_uM,row.NaCl_uM,xx,row.mean_million))
# Labels are placed outside each group's raw points and SD interval.
label_positions={(50,1):(1.00,4.45),(100,1):(1.30,.65),(100,5):(4.95,9.65),(200,1):(1.60,12.6),(200,5):(5.50,14.45)}
for row in s.itertuples():
    key=(row.CD_uM,row.NaCl_uM)
    if key in label_positions:
        xx,yy=label_positions[key]
        ax.text(xx,yy,f'均值 {row.mean_million:.2f}',ha='center',va='center',fontsize=9,color=colors[row.CD_uM])
red='#B43F3F';drop=a['CD100_decrease_10_vs_5_percent'];cv=a['CD100_NaCl10_CV_percent']
row=s[(s.CD_uM==100)&(s.NaCl_uM==10)].iloc[0]
max10=p[(p.CD_uM==100)&(p.NaCl_uM==10)].peak_intensity_au.max()/1e6
note=f'与 5 μM NaCl 相比\n峰强度下降约 {drop:.1f}%\n变异系数 CV ≈ {cv:.1f}%'
ax.annotate(note,xy=(10,max10+.16),xytext=(8.95,10.80),ha='center',va='center',fontsize=11,color=red,linespacing=1.6,arrowprops={'arrowstyle':'->','lw':1.1,'color':red,'shrinkA':10,'shrinkB':4},zorder=6)
ax.text(8.90,1.15,f'均值 {row.mean_million:.2f}',ha='center',va='center',fontsize=9,color=colors[100])
ax.set(xlim=(-.05,11.35),ylim=(0,16),xlabel='NaCl 浓度（μM）',ylabel='目标离子峰强度（×10⁶）')
ax.set_xticks([1,5,10]);ax.set_yticks([0,3,6,9,12,15]);ax.tick_params(direction='out',length=4,pad=5)
ax.spines[['top','right']].set_visible(False)
handles=[Line2D([],[],marker=markers[cd],color=colors[cd],lw=1.1,mfc=colors[cd],mec='white',ms=6,label=f'{cd} μM') for cd in [50,100,200]]
fig.legend(handles=handles,title='环糊精浓度',loc='upper center',bbox_to_anchor=(.54,.865),ncol=3,frameon=False,fontsize=10,title_fontsize=10,columnspacing=2.5,handlelength=2)
fig.text(.11,.135,'空心点：单次采集；实心点与误差棒：均值 ± 标准差；每组 5 次采集。',fontsize=9,color='#444444')
fig.text(.11,.092,'仅连接实测均值；未测组合不补零、不插值；横向错位仅用于避免遮挡。',fontsize=8.5,color='#555555')
fig.text(.11,.049,'高盐下的信号衰减与重复性下降可提示潜在离子抑制，但不能据此确认其机制。',fontsize=8.5,color='#555555')
assert len(actual_points)==30 and np.allclose(sorted(actual_points),sorted(p.peak_intensity_au.to_numpy()/1e6))
assert (s.mean_million-s.SD_million).min()>0 and (s.mean_million+s.SD_million).max()<16 and p.peak_intensity_au.max()/1e6<16
# Missing Chinese glyphs must fail the build instead of silently yielding boxes.
with warnings.catch_warnings():
    warnings.filterwarnings('error',message='Glyph .* missing from font')
    fig.savefig(BASE/'六组浓度_目标离子中文对比图.png',dpi=600)
plt.close(fig)
with Image.open(BASE/'六组浓度_目标离子中文对比图.png') as im:
    assert all(abs(v-600)<1 for v in im.info['dpi']);assert im.size==(5196,3661)
    print('PNG:',im.size,im.info['dpi'])
print('Font:',font_name,'; all 30 raw points verified, no clipping; single axes only')
