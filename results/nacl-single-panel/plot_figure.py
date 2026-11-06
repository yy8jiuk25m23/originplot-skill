from pathlib import Path
import os,json
os.environ.setdefault('MPLCONFIGDIR','/tmp/originplot-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import font_manager
import numpy as np
import pandas as pd
from PIL import Image
BASE=Path(__file__).resolve().parent
s=pd.read_csv(BASE/'summary.csv');p=pd.read_csv(BASE/'individual_peaks.csv');a=json.loads((BASE/'audit.json').read_text())
font='Arial' if any(f.name=='Arial' for f in font_manager.fontManager.ttflist) else 'Liberation Sans'
plt.rcParams.update({'font.family':font,'font.size':9,'axes.labelsize':10,'axes.linewidth':.8,'pdf.fonttype':42,'svg.fonttype':'none','path.simplify':False,'savefig.facecolor':'white'})
fig,ax=plt.subplots(figsize=(180/25.4,125/25.4));fig.subplots_adjust(left=.14,right=.96,bottom=.21,top=.76)
fig.suptitle('Effect of NaCl concentration on target-ion intensity\nand repeatability at m/z ≈ 590.2 (CD = 100 μM)',fontsize=12,y=.965,linespacing=1.45)
colors=['#0F4D92','#26805C','#B64342']
ax.plot(s.NaCl_uM,s.mean_million,color='#707070',lw=1,zorder=1)
for r,c in zip(s.itertuples(),colors):
 vals=p[p.NaCl_uM==r.NaCl_uM].peak_intensity_au.to_numpy()/1e6
 ax.scatter(r.NaCl_uM+np.linspace(-.17,.17,5),vals,s=34,facecolor='white',edgecolor=c,linewidth=1.2,zorder=3)
 ax.errorbar(r.NaCl_uM,r.mean_million,yerr=r.SD_million,fmt='o',color=c,ms=6,markeredgecolor='white',markeredgewidth=.7,capsize=4,elinewidth=1.3,zorder=4)
 if r.NaCl_uM!=10:
  ax.text(r.NaCl_uM,max(vals.max(),r.mean_million+r.SD_million)+.48,f'Mean = {r.mean_million:.2f}\nCV = {r.CV_percent:.1f}%',ha='center',va='bottom',fontsize=9,color=c,linespacing=1.5)
 else:
  ax.annotate(f'{a["decrease_10_vs_5_percent"]:.1f}% decrease vs 5 μM\nMean = {r.mean_million:.2f}\nCV = {r.CV_percent:.1f}%',xy=(10,max(vals.max(),r.mean_million+r.SD_million)+.12),xytext=(9.2,7.7),ha='center',va='center',fontsize=9.5,color=c,linespacing=1.6,arrowprops={'arrowstyle':'-','color':c,'lw':.8})
ax.set(xlim=(.2,11),ylim=(0,11),xlabel='NaCl concentration (μM)',ylabel='Peak intensity of m/z ≈ 590.2 (×10⁶ a.u.)');ax.set_xticks([1,5,10]);ax.set_yticks([0,2,4,6,8,10]);ax.spines[['top','right']].set_visible(False);ax.tick_params(direction='out',length=3.5)
ax.get_xticklabels()[-1].set_color(colors[-1]);ax.get_xticklabels()[-1].set_fontweight('bold')
handles=[Line2D([],[],marker='o',mfc='white',mec='#555555',ls='none',ms=5,label='Individual acquisition (n = 5/group)'),Line2D([],[],marker='o',color='#555555',lw=1,ms=5,label='Mean ± sample SD')]
fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.55,.855),ncol=2,frameon=False,fontsize=8,handlelength=1.6,columnspacing=1.6)
fig.text(.14,.10,'High NaCl (10 μM): marked signal attenuation and poor repeatability.',fontsize=8.5)
fig.text(.14,.055,'Peak window: m/z 590.10–590.32. No normalization or significance testing.',fontsize=7.5,color='#555555')
for ext in ['png','pdf','svg']:fig.savefig(BASE/f'Figure_NaCl_CD100.{ext}',dpi=600)
fig.savefig(BASE/'Figure_NaCl_CD100.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
plt.close(fig)
for ext in ['png','tiff']:
 with Image.open(BASE/f'Figure_NaCl_CD100.{ext}') as im:
  assert all(abs(v-600)<1 for v in im.info['dpi']);print(ext,im.size,im.info['dpi'])
print('Font:',font)
