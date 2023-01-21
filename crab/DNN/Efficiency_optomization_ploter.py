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
files_to_read = ['Efficiency_Optimization_with_ttbar_DNNScore_info_'+year+'_'+lep+'_with_weights.root'] 
#files_to_read = ['Efficiency_Optimization_info_'+year+'_'+lep+'_with_weights.root']
print("Reading file ......", files_to_read )
colors = [2,3,4,6,7,216]
makerstyle = [87,20,21,22,23,34]

legend_txt_eff = ["#epsilon_{Sig}","#epsilon_{Bkg}","Signal Purity"]
legend_txt = [year+" #it{#"+lep+"^{#pm} + jets}"]
effi_array = []
plots = ["Sig_Efficiency","Bkg_Efficiency","Purity","Sig_by_Bkg_Ratio"]
for i in range(len(files_to_read)):
     inputfile = rt.TFile(filedir+files_to_read[i],'read')
     for plot in plots:
        print plot
        sig_effi_temp = inputfile.Get(plot)
        effi_array.append(sig_effi_temp)
        del sig_effi_temp
        

c2 = rt.TCanvas('c2', '', 800, 800, 800, 800)
c2.cd()
rt.gStyle.SetOptStat(0)

pad = rt.TPad("grid","",0,0,1,1)
pad.Draw()
#pad.cd()
#pad.SetGrid()
#pad.SetFillStyle(4000)

for i in range(0,len(effi_array)):
        print plots[i]
        effi_array[i].Draw("colz")
        #effi_array[i].Draw("box")
        effi_array[i].SetLineStyle(9)
        effi_array[i].SetLineWidth(3)
        effi_array[i].SetLineColorAlpha(rt.kRed,0.5)
        effi_array[i].Draw("CONT3 same")
        c2.Update()

        c2.Print('Plots/Optimization_ttbar_'+plots[i]+"_"+year+'_'+lep+'_Effi.png')
        c2.Print('Plots/Optimization_ttbar_'+plots[i]+"_"+year+'_'+lep+'_Effi.png')
