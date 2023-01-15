import ROOT as rt
import numpy as np
import argparse as arg

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

files_to_read_roc = ['Efficiency_info_'+year+'_'+lep+'.root']
print("Reading file ......", files_to_read_roc )
colors = [2,3,4,6,7,216]
makerstyle = [87,20,21,22,23,34]

legend_txt_eff = ["#epsilon_{Sig}","#epsilon_{Bkg}","Signal Purity"]
legend_txt = [year+" #it{#"+lep+"^{#pm} + jets}"]
roc_array = []
effi_array = []
rocInt_array = []
for i in range(len(files_to_read_roc)):
        inputfile = rt.TFile(filedir+files_to_read_roc[i],'read')

        rocInt_Grp = inputfile.Get("rocInt")
        rocInt_Grp.Print()
        rocInt_array.append(round(rocInt_Grp.GetY()[0],3))

        roc_temp = inputfile.Get("roc")
        roc_temp.SetLineColor(colors[i])
        roc_temp.SetMarkerStyle(makerstyle[i])
        roc_temp.SetMarkerColor(colors[i])
        roc_temp.SetMarkerSize(1)
        roc_array.append(roc_temp)
        del roc_temp
        
        sig_effi_temp = inputfile.Get("sig_effi")
        sig_effi_temp.SetTitle("")
        sig_effi_temp.SetLineColor(rt.kRed)
        sig_effi_temp.GetYaxis().SetTitleOffset(1.4)
        sig_effi_temp.SetMarkerStyle(makerstyle[i])
        sig_effi_temp.SetMarkerColor(rt.kRed)
        sig_effi_temp.SetMarkerSize(1)
        effi_array.append(sig_effi_temp)
        del sig_effi_temp
        
        bkg_effi_temp = inputfile.Get("bkg_effi")
        bkg_effi_temp.SetLineColor(rt.kGreen-2)
        bkg_effi_temp.SetMarkerStyle(makerstyle[i])
        bkg_effi_temp.SetMarkerColor(rt.kGreen-2)
        bkg_effi_temp.SetMarkerSize(1)
        effi_array.append(bkg_effi_temp)
        del bkg_effi_temp
        
        purity_temp = inputfile.Get("Purity")
        purity_temp.SetLineColor(rt.kBlue)
        purity_temp.SetMarkerStyle(makerstyle[i])
        purity_temp.SetMarkerColor(rt.kBlue)
        purity_temp.SetMarkerSize(1)
        effi_array.append(purity_temp)
        del purity_temp
	

print(rocInt_array)        
c1 = rt.TCanvas('c1', '', 800, 800, 800, 800)
c1.cd()

std.Draw()
roc_array[0].Draw("same")
for i in range(1,len(roc_array)):
     roc_array[i].Draw("P;same")
     

cntrl0 = rt.TPaveText(0.2, 0.93, 0.25, 208)
cntrl0.SetFillStyle(0)
cntrl0.SetBorderSize(0)
cntrl0.SetMargin(0)
cntrl0.SetTextFont(42)
cntrl0.SetTextSize(0.02)
cntrl0.SetTextAlign(13)
cntrl0.AddText("2J1T")
cntrl0.Draw("same")

legend = rt.TLegend(0.12193646, 0.818435, 0.3293552, 0.83026143)
legend.Clear()
#legend.SetNColumns(2)
legend.SetBorderSize(1)
legend.SetTextSize(0.04)
legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)

legend.AddEntry(roc_array[0], legend_txt[0]+" ("+str(rocInt_array[0])+")", "l")
#for i in range(1,len(roc_array)):
# legend.AddEntry(roc_array[i], legend_txt[i]+" ("+str(rocInt_array[i])+")", "p")

legend.Draw("same")
c1.Update()
c1.Print('Plots/'+year+'_'+lep+'_ROC.png')
c1.Print('Plots/'+year+'_'+lep+'_ROC.pdf') 


c2 = rt.TCanvas('c2', '', 800, 800, 800, 800)
c2.cd()

effi_array[0].Draw()
for i in range(1,len(effi_array)):
     effi_array[i].Draw("l;same")

cntrl0 = rt.TPaveText(0.2, 0.93, 0.25, 208)
cntrl0.SetFillStyle(0)
cntrl0.SetBorderSize(0)
cntrl0.SetMargin(0)
cntrl0.SetTextFont(42)
cntrl0.SetTextSize(0.02)
cntrl0.SetTextAlign(13)
cntrl0.AddText("2J1T")
cntrl0.Draw("same")

legend = rt.TLegend(0.50193646, 0.768435, 0.73293552, 0.8826143)
legend.Clear()
#legend.SetNColumns(2)
legend.SetBorderSize(1)
legend.SetTextSize(0.04)
legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)

legend.AddEntry(effi_array[0], legend_txt_eff[0], "l")
for i in range(1,len(effi_array)):
     legend.AddEntry(effi_array[i], legend_txt_eff[i], "l")

legend.Draw("same")
c2.Update()
c2.Print('Plots/'+year+'_'+lep+'_Effi.png')
c2.Print('Plots/'+year+'_'+lep+'_Effi.pdf')


