import ROOT as rt
import numpy as np
import argparse as arg
from Hist_style import *

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
args = parser.parse_args()
lep = args.lepton[0]
year= args.year[0]

filedir = "ROC_TGraphs/"
     
files_to_read = ['Efficiency_2D_opt_'+year+'_'+lep+'_with_weights.root']
print("Reading file ......", files_to_read )

plots = ['Purity','Sig_Efficiency','Bkg_Efficiency','Sig_by_Bkg_Ratio']

inputfile = rt.TFile(filedir+files_to_read[0],'read')

c2 = rt.TCanvas('c2', '', 800, 800, 800, 800)
rt.gStyle.SetOptStat(0)
c2.cd()

for plot in plots: 
        temp = inputfile.Get(plot)
        temp.Draw("colz")
        c2.Print('Plots/Optimization_'+plot+'_'+year+'_'+lep+'.png')
        c2.Print('Plots/Optimization_'+plot+'_'+year+'_'+lep+'.pdf')
        c2.Update()
        del temp
