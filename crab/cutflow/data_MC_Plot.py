#!/usr/bin/env python
import os,sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='el', help="lepton flavor [ el , mu ]")
parser.add_argument('-y', '--year', dest='year', type=str, default='UL2018', help=" UL2017 UL2016preVFP UL2016postVFP UL2018 ")

args = parser.parse_args()
print('--------------------')
print(args)


Lep = args.lepton
year = args.year

import csv
import ROOT
data = {}  # A dictionary to store the data

with open('cut_flow_Run2_'+year+'_'+Lep+'.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')  # Use tab as the delimiter
    for row in reader:
        channel = row[0]
        print(channel)
        if(channel in ["Cuts"]):
            cuts = [value.strip() for value in row[1:]]
        else:
            cuts = [int(float(value.strip())) for value in row[1:]]  # Convert values to integers
        data[channel] = cuts

print(type(data['Tchannel'][0]),data['Tchannel'])

channel_colors = {
    "Tchannel": ROOT.kRed,
    "Tbarchannel": ROOT.kRed,
    "Total": ROOT.kBlack,
    "TWChannel": ROOT.kCyan+1,
    "TbarWChannel": ROOT.kCyan+1,
    "SChannel": ROOT.kCyan+1,
    "TTbar Semi": ROOT.kOrange-1,
    "TTbar Fully": ROOT.kOrange-1,
    "Wp0Jets": ROOT.kGreen+2,
    "Wp1Jets": ROOT.kGreen+2,
    "Wp2Jets": ROOT.kGreen+2,
    "DYJets": ROOT.kBlue,
    "WWTo2L2NU": ROOT.kMagenta,
    "WZTo2L2Q": ROOT.kMagenta,
    "ZZTo2L2Q": ROOT.kMagenta,
}

# Create a ROOT TCanvas
canvas = ROOT.TCanvas("stack_plot", "Stack Plot", 800, 700)

# Create a TLegend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

# Create THStack for the stack plot
stack = ROOT.THStack("stack", "Stack Plot")

# Convert the data dictionary into TH1 histograms and add them to the stack
for channel, cuts in data.items():
    if(channel in ["Cuts"]): continue
    hist = ROOT.TH1F(channel, channel, len(cuts), 0, len(cuts))
    for i, cut_value in enumerate(cuts):
        hist.SetBinContent(i + 1, cut_value)
    hist.SetFillColor(channel_colors.get(channel, ROOT.kBlack))
    if(channel in ['Tchannel','Tbarchannel']):#,"TWChannel","TbarWChannel","SChannel"]):#,"TTbar Semi","TTbar Fully","Wp0Jets","Wp1Jets","Wp2Jets"]): 
        stack.Add(hist)
        legend.AddEntry(hist, channel, "f")

pad1 = ROOT.TPad("pad1", "pad1", 0.0,0.2831916,1.0,0.97)
pad1.SetBottomMargin(0.015)
pad1.SetTopMargin(0.12)
pad1.SetLeftMargin(0.11)
pad1.SetTicky()
pad1.SetTickx()
pad1.SetLogy()
pad1.Draw()
pad1.cd()

# Draw the stack plot
stack.SetMinimum(100000)
stack.SetMaximum(1e10)
stack.Draw("hist")
stack.GetXaxis().SetTitle("Cuts")
stack.GetYaxis().SetTitle("Y-Axis Title")

# Draw the legend
legend.Draw()

# Compare with the "data" channel (assuming you have "data" as one of the channels)
data_hist = ROOT.TH1F("data", "data", len(data["data"]), 0, len(data["data"]))
for i, cut_value in enumerate(data["data"]):
    data_hist.SetBinContent(i + 1, cut_value)
#data_hist.Draw("same")

# Save or display the plot
canvas.SaveAs("Plots/stack_plot_cutflow_"+year+"_"+Lep+".png")
