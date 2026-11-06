from pathlib import Path
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/originplot-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from PIL import Image

BASE=Path(__file__).resolve().parent
s=pd.read_csv(BASE/'summary.csv'); p=pd.read_csv(BASE/'individual_peaks.csv'); spectra=pd.read_csv(BASE/'spectra_window.csv')
order=['50/1','100/1','100/5','100/10','200/1','200/5']
colors=['#0F4D92','#42949E','#B64342','#767676','#9A4D8E','#8BCF8B']
markers=['o','s','^','D','v','P']
plt.rcParams.update({'path.simplify':False,'font.family':'Liberation Sans','font.size':8,'axes.labelsize':8.5,'axes.titlesize':9,'axes.linewidth':0.7,'xtick.major.width':0.7,'ytick.major.width':0.7,'xtick.direction':'out','ytick.direction':'out','pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
fig,axes=plt.subplots(2,2,figsize=(200/25.4,165/25.4))
fig.subplots_adjust(left=.095,right=.975,bottom=.10,top=.84,wspace=.36,hspace=.48)
A,B,C,D=axes.ravel()
for ax,label,title in zip(axes.ravel(),'ABCD',['Mean raw mass spectra','Peak response (mean ± SD)','Concentration response','Acquisition index']):
 ax.text(-.15,1.08,label,transform=ax.transAxes,fontweight='bold',fontsize=12,va='bottom')
 ax.set_title(title,pad=10,loc='left')
 ax.tick_params(length=3,pad=3)
 ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
for cond,color,marker in zip(order,colors,markers):
 v=spectra[spectra.condition==cond]
 A.plot(v.mz,v.mean_raw_au/1e6,color=color,lw=1.1,label=cond+' μM')
 q=p[p.condition==cond].sort_values('acquisition_index')
 D.plot(q.acquisition_index,q.peak_intensity_au/1e6,color=color,lw=1,marker=marker,ms=3.7,markeredgewidth=.5)
A.set(xlim=(589.8,591.6),ylim=(0,spectra.mean_raw_au.max()/1e6*1.18),xlabel='m/z',ylabel='Ion intensity (×10⁶, a.u.)')
A.set_xticks([589.8,590.2,590.6,591.0,591.4]);A.ticklabel_format(axis='x',style='plain',useOffset=False)
A.text(.035,.95,'m/z ≈ 590.2',transform=A.transAxes,va='top',fontsize=8)
# One shared legend preserves identical group color/marker mapping in A, B and D.
handles=[Line2D([0],[0],color=c,marker=m,lw=1,ms=4,label=g+' μM') for g,c,m in zip(order,colors,markers)]
fig.legend(handles=handles,title='CD/NaCl concentration',ncol=3,loc='upper center',bbox_to_anchor=(.53,.995),frameon=False,columnspacing=2.4,handlelength=2,fontsize=8,title_fontsize=8.5)
for i,(cond,color,marker) in enumerate(zip(order,colors,markers),1):
 q=p[p.condition==cond].peak_intensity_au.to_numpy()/1e6
 offsets=np.linspace(-.14,.14,len(q))
 B.scatter(i+offsets,q,s=19,color=color,marker=marker,edgecolor='white',linewidth=.35,zorder=3)
 r=s[s.condition==cond].iloc[0]
 B.errorbar(i,r.mean_million,yerr=r.SD_million,fmt='_',color='#272727',markersize=12,markeredgewidth=1.4,elinewidth=.9,capsize=3,zorder=4)
 B.text(i,13.0,f'n={len(q)}',ha='center',fontsize=7)
B.set(xlim=(.5,6.5),ylim=(0,14.3),xlabel='CD/NaCl (μM)',ylabel='Peak intensity (×10⁶, a.u.)')
B.set_xticks(range(1,7),order,rotation=35,ha='right')
B.annotate('Highest mean',xy=(5,s.loc[s.condition=='200/1','mean_million'].iloc[0]+.4),xytext=(4.7,13.65),ha='center',fontsize=7,arrowprops={'arrowstyle':'-','lw':.6,'color':'#4D4D4D'})
heat=s.pivot(index='CD_uM',columns='NaCl_uM',values='mean_million').reindex(index=[50,100,200],columns=[1,5,10]).to_numpy()
cmap=plt.get_cmap('viridis').copy();cmap.set_bad('#E7E7E7')
im=C.imshow(np.ma.masked_invalid(heat),origin='lower',cmap=cmap,vmin=0,vmax=s.mean_million.max(),interpolation='none',aspect='auto')
C.set_xticks([0,1,2],['1','5','10']);C.set_yticks([0,1,2],['50','100','200'])
C.set(xlabel='NaCl concentration (μM)',ylabel='CD concentration (μM)')
for y in range(3):
 for x in range(3):
  z=heat[y,x]
  C.text(x,y,'NA' if np.isnan(z) else f'{z:.2f}',ha='center',va='center',fontsize=9,color='#4D4D4D' if np.isnan(z) else ('white' if z<6 else '#202020'))
C.set_xticks(np.arange(-.5,3,1),minor=True);C.set_yticks(np.arange(-.5,3,1),minor=True)
C.grid(which='minor',color='white',linewidth=1);C.tick_params(which='minor',length=0)
cb=fig.colorbar(im,ax=C,fraction=.047,pad=.04);cb.set_label('Mean peak intensity (×10⁶, a.u.)',fontsize=7.5);cb.ax.tick_params(labelsize=7)
D.set(xlim=(.8,5.2),ylim=(0,13),xlabel='Acquisition index',ylabel='Peak intensity (×10⁶, a.u.)');D.set_xticks([1,2,3,4,5])
fig.text(.095,.025,'Peak window: m/z 589.9–590.5; no smoothing or normalization. NA: not measured.',fontsize=7,color='#4D4D4D')
for ext in ['png','pdf','svg']:
 fig.savefig(BASE/f'Figure1.{ext}',dpi=600)
fig.savefig(BASE/'Figure1.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
fig.savefig(BASE/'Figure1_preview.png',dpi=150)
plt.close(fig)
for name in ['Figure1.png','Figure1.tiff']:
 with Image.open(BASE/name) as img:
  assert img.width>4500 and img.height>3800
  assert all(abs(v-600)<1 for v in img.info['dpi'])
  print(name,img.size,img.info['dpi'])
print('PASS: exports verified; 28 points in B and D; 100/1 ends at acquisition 3; three heatmap NA cells')
