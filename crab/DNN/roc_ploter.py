import ROOT as rt
import numpy as np

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

files_to_read_roc = ['ROC_info_ULpreVFP2016_mu.root','ROC_info_ULpreVFP2016_el.root','ROC_info_ULpostVFP2016_mu.root','ROC_info_ULpostVFP2016_el.root','ROC_info_UL2017_mu.root','ROC_info_UL2017_el.root']
colors = [2,3,4,6,7,216]
makerstyle = [87,20,21,22,23,34]

legend_txt = ["UL2016preVFP #it{#mu^{#pm} + jets}","UL2016preVFP #it{e^{#pm} + jets}","UL2016postVFP #it{#mu^{#pm} + jets}","UL2016postVFP #it{e^{#pm} + jets}","UL2017 #it{#mu^{#pm} + jets}","UL2017 #it{e^{#pm} + jets}"]

roc_array = []
rocInt_array = []
for i in range(len(files_to_read_roc)):
        inputfile = rt.TFile(filedir+files_to_read_roc[i],'read')

        rocInt_Grp = inputfile.Get("rocInt")
        rocInt_Grp.Print()
        rocInt_array.append(round(rocInt_Grp.GetPointY(0),3))

        roc_temp = inputfile.Get("roc")
        roc_temp.SetLineColor(colors[i])
        roc_temp.SetMarkerStyle(makerstyle[i])
        roc_temp.SetMarkerColor(colors[i])
        roc_temp.SetMarkerSize(1)
        roc_array.append(roc_temp)
	

print(rocInt_array)        
c1 = rt.TCanvas('c1', '', 800, 800, 800, 800)
c1.cd()

std.Draw()
roc_array[0].Draw("same")
for i in range(1,len(files_to_read_roc)):
     roc_array[i].Draw("P;same")
     x =np

cntrl0 = rt.TPaveText(0.2, 0.93, 0.25, 208)
cntrl0.SetFillStyle(0)
cntrl0.SetBorderSize(0)
cntrl0.SetMargin(0)
cntrl0.SetTextFont(42)
cntrl0.SetTextSize(0.02)
cntrl0.SetTextAlign(13)
cntrl0.AddText("2J1T")
cntrl0.Draw("same")

legend = rt.TLegend(0.10193646, 0.518435, 0.3293552, 0.83026143)
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
for i in range(1,len(files_to_read_roc)):
     legend.AddEntry(roc_array[i], legend_txt[i]+" ("+str(rocInt_array[i])+")", "p")

legend.Draw("same")
c1.Update()
#c1.Print('Plots/ROC.png')
#c1.Print('Plots/ROC.pdf') 
