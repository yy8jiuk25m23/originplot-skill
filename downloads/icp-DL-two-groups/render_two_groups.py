"""Standalone D/L plot: remove duplicate display groups, keep all 70 scans."""
from pathlib import Path
import os,json
B=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']=str(B/'mplconfig')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt,font_manager
from PIL import Image

O=B/'two_groups_only';O.mkdir(exist_ok=True)
font=Path('/workspace/icp_chiral_20261121/font_setup/Arial.ttf')
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({'font.family':'Arial','font.size':11,'axes.labelsize':12,
    'xtick.labelsize':11,'ytick.labelsize':10,'axes.linewidth':.8,
    'axes.edgecolor':'#333333','text.color':'#222222','axes.labelcolor':'#222222',
    'axes.unicode_minus':False,'savefig.facecolor':'white','figure.facecolor':'white'})
s=pd.read_csv(B/'output/data/all70_original_peak_parameters.csv')
assert len(s)==70 and not s.duplicated(['group','scan']).any()
fig,ax=plt.subplots(figsize=(7.2,6.1))
fig.subplots_adjust(left=.15,right=.97,bottom=.13,top=.97)
colors={'D':'#2166AC','L':'#D73027'}
record=[]
for group,x in [('D',1),('L',2)]:
    data=s[s.group==group].sort_values('scan_number')
    v=data.peak_voltage_mV.to_numpy();assert len(v)==35
    q1,q3=np.quantile(v,[.25,.75],method='linear');median=np.median(v)
    ax.boxplot([v],positions=[x],widths=.48,patch_artist=True,showfliers=False,manage_ticks=False,
        boxprops=dict(facecolor='white',edgecolor=colors[group],lw=1.7),
        whiskerprops=dict(color=colors[group],lw=1.5),capprops=dict(color=colors[group],lw=1.5),
        medianprops=dict(color='#222222',lw=1.7),zorder=1)
    jitter=.15*np.sin(data.scan_number.to_numpy()*2.3999632297)
    normal=~data.candidate_either_threshold.to_numpy()
    ax.scatter(x+jitter[normal],v[normal],s=23,color=colors[group],alpha=.83,zorder=3)
    ax.scatter(x+jitter[~normal],v[~normal],s=41,facecolors='white',edgecolors=colors[group],lw=1.3,zorder=4)
    ax.text(x,151.7,f'n = 35\nMedian = {median:.3f}\nIQR = {q3-q1:.3f}',
        ha='center',va='top',fontsize=10,color=colors[group])
    record.append(dict(group=group,n=35,median_mV=float(median),IQR_mV=float(q3-q1),
        measured_scans_deleted=0,displayed_once=True))
ax.set(xticks=[1,2],xticklabels=['D-Arginine','L-Arginine'],ylabel='Peak Voltage (mV)',
    xlim=(.5,2.5),ylim=(127.5,153.5))
ax.tick_params(axis='x',length=0,pad=9)
ax.tick_params(axis='y',direction='out',length=4,width=.8)
assert sum(len(c.get_offsets()) for c in ax.collections)==70
fig.savefig(O/'ICP_D_L_Peak_Distribution_600dpi.png',dpi=600)
fig.savefig(O/'ICP_D_L_Peak_Distribution_600dpi.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
fig.savefig(O/'ICP_D_L_Peak_Distribution_preview.png',dpi=240)
plt.close(fig)
for suffix in ['png','tiff']:
    with Image.open(O/f'ICP_D_L_Peak_Distribution_600dpi.{suffix}') as im:
        assert im.size==(4320,3660) and all(abs(float(d)-600)<.1 for d in im.info['dpi'])
(O/'plot_record.json').write_text(json.dumps(dict(groups=record,display_groups=2,actual_scan_points=70,
    voltage_conversion='Provisional V=X*0.002 mV; unverified calibration',renderer='Matplotlib',
    hollow_points='Statistical candidates, retained in data',raster_dpi=600),indent=2))
print('Done: two display groups, all 70 original peak-voltage points; PNG/TIFF 4320x3660 at 600dpi.')
