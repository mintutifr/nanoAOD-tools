import ROOT as rt
import numpy as np
import argparse as arg
from Hist_style import *

# Argument parser
parser = arg.ArgumentParser(description="Plot efficiency curves for given years and lepton type.")
parser.add_argument('-l', '--lepton', dest='lepton', type=str, required=True, help="Lepton type: [el, mu]")
parser.add_argument('-y', '--year', dest='year', type=str, nargs='*', help="Specific Year(s): [UL2016preVFP, UL2016postVFP, UL2017, UL2018]")
args = parser.parse_args()

lep = args.lepton  # Lepton type
years = args.year if args.year else ["UL2016preVFP", "UL2017", "UL2016postVFP",  "UL2018"]  # Default to all years

x2 = np.linspace(0, 1, 40)
y2 = x2

# Standard line for reference
# std = rt.TGraph(len(x2), x2, y2)
# std.SetLineWidth(4)
# std.SetLineStyle(2)
# std.SetLineColorAlpha(rt.kBlack, 0.5)
# std.SetMaximum(120.0)
# std.SetMinimum(0.0)
# std.GetXaxis().SetLimits(0.0, 100.0)
# std.GetXaxis().SetTitle('#varepsilon_{Sig} (%)')
# std.GetYaxis().SetTitle('#varepsilon_{Bkg} (%)')
# std.GetYaxis().SetTitleOffset(1.3)
# std.SetTitle("")

filedir = "ROC_TGraphs/"
marker_styles = [20, 21, 22, 29]  # Marker styles for years

# Define colors for sig_effi, bkg_effi, and purity
sig_color = rt.kRed
bkg_color = rt.kGreen - 2
purity_color = rt.kBlue

effi_arrays = {year: [] for year in years}  # Store efficiency graphs by year

# Loop over years and read files
for idx, year in enumerate(years):
    files_to_read = f'Efficiency_info_{year}_{lep}_with_weights_new_withoutmtwMassCut.root'
    print(f"Reading file for {year} ...... {files_to_read}")
    print(marker_styles[idx])

    inputfile = rt.TFile(filedir + files_to_read, 'read')

    # Signal Efficiency
    sig_effi_temp = inputfile.Get("sig_effi")
    sig_effi_temp.SetLineColor(sig_color)
    sig_effi_temp.SetLineWidth(3)
    sig_effi_temp.SetMarkerStyle(marker_styles[idx])
    sig_effi_temp.SetMarkerColor(sig_color)
    sig_effi_temp.SetMarkerSize(1)
    sig_effi_temp.SetName("")
    effi_arrays[year].append(sig_effi_temp.Clone())
    del sig_effi_temp

    # Background Efficiency
    bkg_effi_temp = inputfile.Get("bkg_effi")
    bkg_effi_temp.SetLineColor(bkg_color)
    bkg_effi_temp.SetLineWidth(3)
    bkg_effi_temp.SetMarkerStyle(marker_styles[idx])
    bkg_effi_temp.SetMarkerColor(bkg_color)
    bkg_effi_temp.SetMarkerSize(1)
    bkg_effi_temp.SetName("")
    effi_arrays[year].append(bkg_effi_temp.Clone())
    del bkg_effi_temp

    # Purity
    purity_temp = inputfile.Get("Purity")
    purity_temp.SetLineColor(purity_color)
    purity_temp.SetLineWidth(3)
    purity_temp.SetMarkerStyle(marker_styles[idx])
    purity_temp.SetMarkerColor(purity_color)
    purity_temp.SetMarkerSize(1)
    purity_temp.SetName("")
    effi_arrays[year].append(purity_temp.Clone())
    del purity_temp

# Create Canvas
c2 = rt.TCanvas('c2', '', 800, 700)
c2.SetTitle("")
c2.cd()

pad = rt.TPad("grid", "", 0, 0, 1, 1)
pad.Draw()
pad.cd()
pad.SetGrid()
pad.SetFillStyle(4000)
pad.SetLogy()

# Draw graphs
first_year = list(effi_arrays.keys())[0]
effi_arrays[first_year][0].SetMaximum(100.0)
effi_arrays[first_year][0].Draw("ACP")

for year, effi_list in effi_arrays.items():
    for graph in effi_list:
        graph.SetMinimum(-10)
        graph.SetMaximum(500.0)
        graph.Draw("CP;same")

# Add legend for efficiencies (fixed colors)
legend_eff = rt.TLegend(0.15, 0.15, 0.3, 0.3)
legend_eff.Clear()
legend_eff.SetBorderSize(0)
legend_eff.SetTextSize(0.04)
legend_eff.SetLineStyle(1)
legend_eff.SetLineWidth(1)
legend_eff.SetFillStyle(1001)

legend_eff.AddEntry(effi_arrays[first_year][0], "#varepsilon_{Sig}", "l")
legend_eff.AddEntry(effi_arrays[first_year][1], "#varepsilon_{Bkg}", "l")
legend_eff.AddEntry(effi_arrays[first_year][2], "Purity", "l")
legend_eff.Draw("same")

# Add legend for years (marker styles) or CMS Internal Tag
if args.year:
    getCMSIntrenal_tag = getCMSIntrenal_tag(0.30, 0.86, 0.45, 0.88)
    getCMSIntrenal_tag.Draw("same")
else:
    legend_years = rt.TLegend(0.45, 0.77, 0.89, 0.86)
    legend_years.SetNColumns(2)  # Two-column legend
    legend_years.Clear()
    legend_years.SetBorderSize(0)
    legend_years.SetTextSize(0.04)
    legend_years.SetLineStyle(1)
    legend_years.SetLineWidth(1)
    legend_years.SetFillStyle(1001)

    for year, effi_list in effi_arrays.items():
        legend_years.AddEntry(effi_list[2], f"{year}", "p")

    legend_years.Draw("same")

# Add region tag and other labels
region_tag = getregion_tag("2J1T", 2, 0.91, 3, 205)
region_tag.Draw("same")
lepjet_tag = leptonjet_tag(lep, 0.3, 0.80, 0.4, 0.84)
lepjet_tag.Draw("same")
#getCMSIntrenal_tag = getCMSIntrenal_tag(0.28, 0.86, 0.48, 0.88)
#getCMSIntrenal_tag.Draw("same")
getCMSpre_tag = getCMSpre_tag(x1=0.185, y1=0.86, x2=0.455, y2=0.88)
getCMSpre_tag.Draw("same")

# Save plot
c2.Update()
if(len(years)==4):
    years = ['Run2']
output_name = f'Plots/{lep}_Effi_{"_".join(years)}.png'
c2.Print(output_name)
c2.Print(output_name.replace('.png', '.pdf'))
