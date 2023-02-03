import sys
import ROOT as rt
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")

args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['ULpreVFP2016', 'ULpostVFP2016','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.lepton[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

print(args)


def propagate_rate_uncertainity(hist, uncert):
    for i in range(hist.GetXaxis().GetNbins()):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

from Hist_style import *


def stack_plot_from_histfile(lep='mu',dataYear='2016'):
	Filename = rt.TFile("/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_histograms_"+year+"_"+lep+".root","Read")

	#Filename = rt.TFile("Histogram_input_2016_Run2_controlRegionF0p2T0p82_stat_full.root","Read")
	Dir = Filename.GetDirectory(lep+'jets')

	top_sig = Dir.Get("top_sig_1725")
	top_sig.SetFillColor(rt.kRed)
	top_sig.SetLineColor(rt.kRed)

	top_bkg = Dir.Get("top_bkg_1725")
	top_bkg.SetFillColor(rt.kOrange-1)
	top_bkg.SetLineColor(rt.kOrange-1)

	EWK_bkg = Dir.Get("EWK_bkg")
	EWK_bkg.SetFillColor(rt.kGreen-2)
	EWK_bkg.SetLineColor(rt.kGreen-2)

	QCD_bkg = Dir.Get("QCD_DD")
	QCD_bkg.SetFillColor(rt.kGray)
	QCD_bkg.SetLineColor(rt.kGray)

	#propagate_rate_uncertainity(top_sig, 15.0)
	#propagate_rate_uncertainity(top_bkg, 6.0)
	#propagate_rate_uncertainity(EWK_bkg, 10.0)
	#propagate_rate_uncertainity(QCD_bkg, 50.0)


	hMC = top_sig.Clone()
	hMC.Add(top_bkg)
	hMC.Add(EWK_bkg)
	hMC.Add(QCD_bkg)

	Data = Dir.Get("data_obs")
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	Data.SetLineColor(rt.kBlack)


	legend = rt.TLegend(0.60193646, 0.5548435, 0.8093552, 0.79026143)
	legend.SetBorderSize(1)
	legend.SetTextSize(0.045)
	legend.SetLineColor(0)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(1001)
	#legend.SetHeader("beNDC", "C")
	legend.AddEntry(Data, "Data", "ple1")
	legend.AddEntry(top_sig, "#it{t}-ch.", "f")
	legend.AddEntry(top_bkg, "t#bar{t}", "f")
	legend.AddEntry(EWK_bkg, "V+Jets, VV", "f")
	legend.AddEntry(QCD_bkg, "QCD", "f")
	#legend.AddEntry(hMC,"Total Unc.","f")



	myComingCanvases = rt.TCanvas("c1","", 600,600,600,600)
	myComingCanvases.cd()
	rt.TGaxis.SetMaxDigits(3)

	top_sig.GetXaxis().SetTitle("M_{top}") 
     	hs = rt.THStack("hs",";"";Events")
	hs.Add(QCD_bkg)
	hs.Add(EWK_bkg)
	hs.Add(top_bkg)
	hs.Add(top_sig)
	hs.SetMaximum(Data.GetMaximum() * 1.2)

	pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
	pad1.SetBottomMargin(0.089)
	pad1.SetTicky()
	pad1.SetTickx()
	#pad1.SetRightMargin(0.143)
	pad1.Draw()
	pad1.cd()

	hs.Draw("hist")
	legend.Draw()

        CMSpreliminary = getCMSpre_tag(0.35, 0.84, 0.43, 0.88)
        CMSpreliminary.Draw("same")
        lepjet_tag = leptonjet_tag(lep,0.29, 0.82, 0.32, 0.84)
        lepjet_tag.Draw("same")
        region_tag = getregion_tag("2J1T", 0.17, 0.92, 0.22, 0.96)
        region_tag.Draw("same")
        yearNlumitag = year_tag(year,0.82, 0.92, 0.9, 0.96)
        yearNlumitag.Draw("same")

	myComingCanvases.Update()

######################################## if it tis top mass comment out below this #######
	Data.Draw("Same;E1")
	myComingCanvases.Update()

 	myComingCanvases.cd()
	pad2 = rt.TPad("pad2", "pad2", 0.0, 0.0, 1.0, 0.2621035)
	pad2.SetTopMargin(0.0)
	pad2.SetBottomMargin(0.3)
	pad2.SetGridy()
	pad2.SetTicky()
	pad2.SetTickx()
	pad2.Draw()
	pad2.cd()

	print Data.GetBinContent(6)
        print hMC.GetBinContent(6)
	h_ratio = rt.TGraphAsymmErrors(Data, hMC, 'pois')
	axis = h_ratio.GetXaxis()
	axis.SetLimits(Data.GetXaxis().GetXmin(), Data.GetXaxis().GetXmax())
	h_ratio.SetMarkerColor(1)
	h_ratio.SetMarkerStyle(20)
	h_ratio.SetMarkerSize(0.89)
	h_ratio.SetLineColor(rt.kBlack)


	h2_ratio = Data.Clone()
	h2_ratio.Divide(hMC)
	nbin = h2_ratio.GetXaxis().GetNbins()
	ledge = h2_ratio.GetXaxis().GetXmin()
	uedge = h2_ratio.GetXaxis().GetXmax()
	band = rt.TH1D('Band', '', nbin, ledge, uedge)
	rt.gStyle.SetOptStat(0)
	for i in range(nbin+1):
		band.SetBinContent(i+1, 1.0)
		if (hMC.GetBinContent(i+1)!=0 and Data.GetBinContent(i+1)!=0):
			err = (hMC.GetBinError(i+1) * h2_ratio.GetBinContent(i+1)) / hMC.GetBinContent(i+1)
		elif (hMC.GetBinContent(i+1)!=0 and Data.GetBinContent(i+1)==0):
			err = 1#hMC.GetBinError(i+1) / hMC.GetBinContent(i+1)
		else:
			err = 0
		band.SetBinError(i+1, err)

	band.SetFillColor(rt.kGray+3)
	band.SetFillStyle(3001) 
	band.GetYaxis().SetTitle("Data/MC")
        band.GetXaxis().SetTitle("m_{T} GeV") 
	#band.GetXaxis().SetTitle(Data.GetXaxis().GetTitle())
	band.GetYaxis().CenterTitle(1) 
	band.GetYaxis().SetTitleOffset(0.35)              
	band.GetYaxis().SetTitleSize(0.12)
	band.GetXaxis().SetTitleSize(0.12)
	band.GetYaxis().SetLabelSize(0.07)
	band.GetXaxis().SetLabelSize(0.1)
	band.SetMaximum(1.545665)
	band.SetMinimum(0.464544)
	c = band.GetYaxis()
	c.SetNdivisions(10)
	c.SetTickSize(0.01)
	d = band.GetXaxis()
	d.SetNdivisions(10)
	d.SetTickSize(0.03)

	band.Draw('E2')
	h_ratio.Draw('PE1, SAME')

######################################## if it tis top mass comment out above this #######

	myComingCanvases.cd()
	myComingCanvases.Update()

	raw_input()
	myComingCanvases.Print("Plots/mtwMass_validation_"+lep+"_"+dataYear+".png")	

if __name__ == "__main__":

        lep = args.lepton[0]
        year= args.year[0]
        stack_plot_from_histfile(lep,year)

