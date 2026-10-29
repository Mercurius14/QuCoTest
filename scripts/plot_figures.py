"""Regenerate numerical paper plots from the packaged full-precision data."""
from pathlib import Path
import argparse,json
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--font-file',type=Path);args=ap.parse_args()
    if args.font_file:font_manager.fontManager.addfont(str(args.font_file))
    installed={f.name for f in font_manager.fontManager.ttflist}
    font='Times New Roman' if 'Times New Roman' in installed else 'Liberation Serif' if 'Liberation Serif' in installed else 'DejaVu Serif'
    plt.rcParams.update({'font.family':font,'font.size':9,'pdf.fonttype':42})
    out=ROOT/'outputs/figures';out.mkdir(parents=True,exist_ok=True)
    def finish(fig,name):
        fig.tight_layout()
        fig.savefig(out/f'{name}.pdf',bbox_inches='tight')
        fig.savefig(out/f'{name}.png',dpi=180,bbox_inches='tight');plt.close(fig)
    methods=['condition_coherence','brick_circuit','quratest_iqft','quratest_ucnot','random_circuit','qucat_pairwise']
    labels=['QuCoTest','BWC','QuraTest-IQFT','QuraTest-UCNOT','RQC','QuCAT-PW']
    colors=['#0072B2','#D55E00','#009E73','#CC79A7','#666666','#8C6D31']
    main=pd.read_csv(ROOT/'data/analysis/main_summary.csv').set_index('method')
    fig,ax=plt.subplots(figsize=(3.5,2.7))
    for m,label,c in zip(methods,labels,colors):
        ax.plot(range(1,31),main.loc[m,[f'ms{k}' for k in range(1,31)]].to_numpy(float)*100,label=label,color=c,linewidth=1.3 if m==methods[0] else 1,linestyle=['-','--','-.',':',':',':'][methods.index(m)])
    ax.set(xlabel='Test budget',ylabel='Mutation score (%)',xlim=(1,30),ylim=(0,102));ax.legend(fontsize=6,ncol=2,loc='lower right',frameon=False);ax.grid(axis='y',alpha=.2)
    finish(fig,'detection_budget')
    order=pd.read_csv(ROOT/'data/analysis/ordering_summary.csv').set_index('method')
    stats=pd.read_csv(ROOT/'data/analysis/external_ordering_statistics.csv')
    fig,axes=plt.subplots(1,2,figsize=(7.16,2.65))
    for m,label,c,style in [('qcbc','Semantic','#0000b3','-'),('random','Random','#555555','--'),('novelty','Novelty','#d96c00','-.')]:
        k=[1,3,5,10,30];axes[0].plot(range(5),[order.loc[m,f'ms{i}']*100 for i in k],label=label,color=c,linestyle=style,marker='o',markersize=3)
    axes[0].set(xticks=range(5),xticklabels=k,xlabel='Test budget',ylabel='Mutation score (%)',ylim=(40,100));axes[0].legend(fontsize=7,frameon=False)
    entries=[]
    for m,label in [('brick_circuit','BWC'),('quratest_iqft','QuraTest-IQFT'),('quratest_ucnot','QuraTest-UCNOT')]:
        for alternative in ['original','random','novelty']:
            r=stats[(stats.target==m+'_qcbc')&(stats.alternative==m+'_'+alternative)&(stats.metric=='auc1_10')].iloc[0]
            entries.append((label+' / '+alternative,r))
    for i,(label,r) in enumerate(entries):axes[1].errorbar(r.mean_delta_pp,i,xerr=[[r.mean_delta_pp-r.ci_low_pp],[r.ci_high_pp-r.mean_delta_pp]],fmt='o',color='#0000b3',markersize=3)
    axes[1].set(yticks=range(len(entries)),yticklabels=[x[0] for x in entries],xlabel='Paired AUC gain (pp)');axes[1].invert_yaxis();axes[1].axvline(0,color='0.6',linewidth=.7);axes[1].tick_params(axis='y',labelsize=6)
    finish(fig,'ordering_evidence')
    threshold=order.loc[[f'tau_{v:g}' for v in [.6,.7,.8,.9,1.]]]
    fig,ax=plt.subplots(figsize=(3.5,2.6));tau=[.6,.7,.8,.9,1.]
    for col,label,color,marker in [('ms1','MS@1','#0000b3','o'),('ms5','MS@5','#d96c00','s'),('auc1_10','AUC@1–10','#008c00','^')]:
        values=threshold[col].to_numpy()*100;ax.plot(tau,values,label=label,color=color,marker=marker,markersize=4)
        for x,y in zip(tau,values):ax.annotate(f'{y:.2f}',(x,y),xytext=(0,-11 if col=='auc1_10' else 6),textcoords='offset points',ha='center',fontsize=8,color=color)
    ax.set(ylim=(60,92),xlim=(.57,1.03),xticks=tau,xlabel='Saturation threshold τ',ylabel='Detection score (%)');ax.axvline(.8,color='0.65',linestyle=':',linewidth=.8);ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.02),fontsize=8);ax.grid(axis='y',alpha=.18)
    finish(fig,'threshold_sensitivity')
    finite=pd.read_csv(ROOT/'data/finite_shots/reference/overall_equal_program_summary.csv')
    curve=pd.read_csv(ROOT/'data/time_model/reference_curve.csv')
    styles=[('condition_coherence','QuCoTest','#0000b3','-','o'),('brick_circuit','BWC','#d96c00','--','s'),('quratest_iqft','QuraTest-IQFT','#008c00','-.','^')]
    def finite_panel(ax):
        for m,label,c,style,mark in styles:
            b=finite[finite.method==m].set_index('shots')
            ax.plot(range(4),b.loc[[0,1024,4096,16384],'AUC1_10']*100,label=label,color=c,linestyle=style,marker=mark,markersize=4)
        ax.set(xticks=range(4),xticklabels=['Exact','1k','4k','16k'],xlabel='Shots per basis',ylabel='AUC@1–10 (%)',ylim=(45,100));ax.grid(axis='y',alpha=.2)
    def time_panel(ax):
        for m,label,c,style,mark in styles:
            b=curve[curve.method==m];ax.plot(b.seconds,b.time_AUC*100,label=label,color=c,linestyle=style)
        ax.set(xlabel='Estimated testing time (s)',ylabel='Time-normalized AUC (%)',xlim=(0,15),ylim=(0,35),xticks=[0,3,6,9,12,15]);ax.grid(axis='y',alpha=.2)
    fig,axes=plt.subplots(1,2,figsize=(7.16,2.6));finite_panel(axes[0]);time_panel(axes[1]);axes[0].legend(fontsize=7,frameon=False)
    finish(fig,'practical_limits')
    for name,fn in [('finite_shots',finite_panel),('estimated_time',time_panel)]:
        fig,ax=plt.subplots(figsize=(3.5,2.6));fn(ax);ax.legend(fontsize=7,frameon=False);finish(fig,name)
    print(json.dumps(dict(output=str(out),font=font,data='Frozen paper inputs and measurements; maxiter40 main configuration'),indent=2))

if __name__=='__main__':main()
