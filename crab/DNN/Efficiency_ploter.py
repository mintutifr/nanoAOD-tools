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

x2 = np.linspace(0, 1, 40)
y2 = x2

std = rt.TGraph(len(x2), x2, y2)
std.SetLineWidth(4)
std.SetLineStyle(2)
std.SetLineColorAlpha(rt.kBlack, 0.5)
std.SetMaximum(100.0)
std.SetMinimum(0.0)
std.GetXaxis().SetLimits(0.0, 100.0)
std.GetXaxis().SetTitle('#varepsilon_{Sig} (%)')
std.GetYaxis().SetTitle('#varepsilon_{Bkg} (%)')
std.GetYaxis().SetTitleOffset(1.3)
std.SetTitle("")
filedir = "ROC_TGraphs/"
 
files_to_read = ['Efficiency_info_'+year+'_'+lep+'_with_weights.root']
print("Reading file ......", files_to_read )
colors = [2,3,4,6,7,216]
makerstyle = [87,20,21,22,23,34]

legend_txt_eff = ["#epsilon_{Sig}","#epsilon_{Bkg}","Signal Purity"]
legend_txt = [year+" #it{#"+lep+"^{#pm} + jets}"]
effi_array = []
for i in range(len(files_to_read)):
        inputfile = rt.TFile(filedir+files_to_read[i],'read')

        sig_effi_temp = inputfile.Get("sig_effi")
        sig_effi_temp.SetTitle("")
        sig_effi_temp.SetLineColor(rt.kRed)
        sig_effi_temp.SetLineWidth(3)
        sig_effi_temp.GetYaxis().SetTitleOffset(1.4)
        sig_effi_temp.SetMarkerStyle(20)#makerstyle[i])
        sig_effi_temp.SetMarkerColor(rt.kRed)
        sig_effi_temp.SetMarkerSize(1)
        effi_array.append(sig_effi_temp)
        del sig_effi_temp
        
        bkg_effi_temp = inputfile.Get("bkg_effi")
        bkg_effi_temp.SetLineColor(rt.kGreen-2)
        bkg_effi_temp.SetLineWidth(3)
        bkg_effi_temp.SetMarkerStyle(20)#makerstyle[i])
        bkg_effi_temp.SetMarkerColor(rt.kGreen-2)
        bkg_effi_temp.SetMarkerSize(1)
        effi_array.append(bkg_effi_temp)
        del bkg_effi_temp
        
        purity_temp = inputfile.Get("Purity")
        purity_temp.SetLineColor(rt.kBlue)
        purity_temp.SetLineWidth(3)
        purity_temp.SetMarkerStyle(20)#makerstyle[i])
        purity_temp.SetMarkerColor(rt.kBlue)
        purity_temp.SetMarkerSize(1)
        effi_array.append(purity_temp)
        del purity_temp
	

c2 = rt.TCanvas('c2', '', 800, 700)
c2.cd()

pad = rt.TPad("grid","",0,0,1,1)
pad.Draw()
pad.cd()
pad.SetGrid()
pad.SetFillStyle(4000)

effi_array[0].SetMaximum(118.0)
effi_array[0].Draw("ACP")
for i in range(1,len(effi_array)):
     effi_array[i].SetMaximum(118.0)
     effi_array[i].Draw("CP;same")


legend = rt.TLegend(0.50193646, 0.738435, 0.78293552, 0.89026143)
legend.Clear()
#legend.SetNColumns(2)
legend.SetBorderSize(1)
legend.SetTextSize(0.04)
legend.SetTextSize(0.04)
#legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)

legend.AddEntry(effi_array[0], legend_txt_eff[0], "l")
for i in range(1,len(effi_array)):
     legend.AddEntry(effi_array[i], legend_txt_eff[i], "l")

legend.Draw("same")
c2.Update()

region_tag = getregion_tag("2J1T", 2, 0.91, 3, 205)
region_tag.Draw("same")
#CMSpreliminary = getCMSpre_tag()
#CMSpreliminary.Draw("same")
getCMSIntrenal_tag = getCMSIntrenal_tag(0.30, 0.86, 0.40, 0.88)
getCMSIntrenal_tag.Draw("same")
lepjet_tag = leptonjet_tag(lep,0.29, 0.82, 0.32, 0.84)
lepjet_tag.Draw("same")
yearNlumitag = year_tag(year,0.948, 118, 0.99,128)
yearNlumitag.Draw("same")
c2.Update()

c2.Print('Plots/'+year+'_'+lep+'_Effi.png')
c2.Print('Plots/'+year+'_'+lep+'_Effi.pdf')


