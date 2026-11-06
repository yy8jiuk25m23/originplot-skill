from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/originplot-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image
BASE=Path(__file__).resolve().parent
s=pd.read_csv(BASE/'summary.csv');p=pd.read_csv(BASE/'individual_peaks.csv')
plt.rcParams.update({'font.family':'Liberation Sans','font.size':8,'axes.labelsize':8,'axes.titlesize':9,'axes.linewidth':.7,'pdf.fonttype':42,'svg.fonttype':'none','path.simplify':False,'savefig.facecolor':'white'})
fig,axs=plt.subplots(1,3,figsize=(230/25.4,95/25.4),sharey=True)
fig.subplots_adjust(left=.09,right=.985,bottom=.25,top=.70,wspace=.25)
fig.suptitle('Concentration effects on the target ion at m/z ≈ 590.2',fontsize=12,y=.97)
settings=[('A','CD concentration effect','NaCl = 1 μM','CD_uM',[50,100,200],s.NaCl_uM==1,'#0F4D92'),('B','NaCl concentration effect','CD = 100 μM','NaCl_uM',[1,5,10],s.CD_uM==100,'#42949E'),('C','NaCl concentration effect','CD = 200 μM','NaCl_uM',[1,5],s.CD_uM==200,'#9A4D8E')]
for ax,(letter,title,fixed,key,xvals,mask,color) in zip(axs,settings):
 q=s[mask].sort_values(key)
 assert q[key].tolist()==xvals
 ax.text(-.12,1.17,letter,transform=ax.transAxes,fontweight='bold',fontsize=12)
 ax.set_title(title+'\n'+fixed,pad=11,linespacing=1.5)
 ax.plot(q[key],q.mean_million,color=color,lw=1.2,zorder=2)
 span=max(xvals)-min(xvals)
 for row in q.itertuples():
  vals=p[p.condition==row.condition].peak_intensity_au.to_numpy()/1e6
  x=getattr(row,key)
  ax.scatter(x+np.linspace(-.025*span,.025*span,len(vals)),vals,s=19,facecolor='white',edgecolor=color,linewidth=.9,zorder=3)
  ax.errorbar(x,row.mean_million,yerr=row.SD_million,fmt='o',color=color,markeredgecolor='white',markeredgewidth=.6,ms=5.3,capsize=3,elinewidth=1,zorder=4)
  ax.text(x,max(vals.max(),row.mean_million+row.SD_million)+.75,f'n={row.n}',ha='center',fontsize=7,color='#4D4D4D')
 ax.set_xlim(min(xvals)-span*.14,max(xvals)+span*.14)
 ax.set_xticks(xvals);ax.set_ylim(0,13);ax.set_yticks([0,3,6,9,12]);ax.tick_params(direction='out',length=3)
 ax.set_xlabel(('CD' if key=='CD_uM' else 'NaCl')+' concentration (μM)',labelpad=7)
 ax.spines[['top','right']].set_visible(False)
axs[0].set_ylabel('Peak intensity at m/z ≈ 590.2\n(×10⁶ a.u.)',labelpad=8)
fig.legend(handles=[Line2D([],[],marker='o',mfc='white',mec='#4D4D4D',ls='none',ms=4,label='Individual acquisition'),Line2D([],[],marker='o',color='#4D4D4D',lw=1,ms=4,label='Mean ± sample SD')],loc='upper center',bbox_to_anchor=(.54,.89),ncol=2,frameon=False,fontsize=8)
fig.text(.09,.07,'Target window: m/z 590.1–590.3. Lines connect measured means only; no prediction or significance testing.',fontsize=7,color='#4D4D4D')
for ext in ['png','pdf','svg']:
 fig.savefig(BASE/f'Figure1_target_ion.{ext}',dpi=600)
fig.savefig(BASE/'Figure1_target_ion.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
fig.savefig(BASE/'Figure1_target_ion_preview.png',dpi=160)
plt.close(fig)
for ext in ['png','tiff']:
 with Image.open(BASE/f'Figure1_target_ion.{ext}') as im:
  assert all(abs(d-600)<1 for d in im.info['dpi'])
  print(ext,im.size,im.info['dpi'])
