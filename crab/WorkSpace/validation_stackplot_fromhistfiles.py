import sys
import ROOT as rt
import argparse as arg
from mlfitNormsToText import *

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-DS', '--DNNscale ', dest='DNNscale', type=str, nargs=1, help="if need to apply DNN renomalization and the unct. propagation [ 0 , 1 ]")
parser.add_argument('-f1', '--combine_InFile ', dest='combine_InFile', type=str, nargs=1, help="combine Input file which has histogram files i.e /home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_t_ch_CAsi_histograms_UL2017_mu.root")
parser.add_argument('-f2', '--fitdignostic_outFile ', dest='fitdignostic_outFile', type=str, nargs=1, help="Fit dignostic output file which has histogram files i.e /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2017.root")
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

print("\n",args)

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

from Hist_style import *

def reset_stack_range(stack, xmin, xmax):
    histograms = stack.GetHists()
    for hist in histograms:
        hist.GetXaxis().SetRangeUser(xmin, xmax)

def stack_plot_from_histfile(lep='mu',dataYear='2016',DNN_recale="0",Combine_InFile="Hist_for_workspace/Combine_Input_t_ch_CAsi_histograms_UL2017_mu.root",Fitdignostic_outFile="fitDiagnostics_M1725_DNNfit_UL2017.root"):
        Combine_year_tag={
                'ULpreVFP2016' :  "_ULpre16",
                'ULpostVFP2016' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"} 	
<<<<<<< Updated upstream
        tag = Combine_year_tag[year] 
=======
        tag = ""#Combine_year_tag[year] 
>>>>>>> Stashed changes

        #Filename = "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/WorkSpace/Hist_for_workspace/Combine_Input_histograms_"+year+"_"+lep+".root" 
        fitdignostic_outrootfile = Fitdignostic_outFile 
	File = rt.TFile(Combine_InFile,"Read")

        if(DNN_recale=="1"):
                print"\n ####################################           ############     ##################"
                print("Please make sure the DNN rescaling is not applied while creating "+Combine_InFile+" Other vise rescaling will be twice which will distort the Data Vs Mc plots")
                print("Reading the Normalization form the "+fitdignostic_outrootfile)
                print"####################################            ###########     ##################\n"
        del Combine_InFile

	#File = rt.TFile("Histogram_input_2016_Run2_controlRegionF0p2T0p82_stat_full.root","Read")
	Dir = File.GetDirectory(lep+'jets')

	top_sig = Dir.Get("top_sig_1725"+tag);
<<<<<<< Updated upstream
               
=======
>>>>>>> Stashed changes
	top_sig.SetFillColor(rt.kRed)
	top_sig.SetLineColor(rt.kRed)
             

	top_bkg = Dir.Get("top_bkg_1725"+tag)
	top_bkg.SetFillColor(rt.kOrange-1)
        top_bkg.SetLineColor(rt.kOrange-1)
        

	EWK_bkg = Dir.Get("EWK_bkg"+tag)
	EWK_bkg.SetFillColor(rt.kGreen-2)
	EWK_bkg.SetLineColor(rt.kGreen-2)
        

	QCD_bkg = Dir.Get("QCD_DD"+tag)
	QCD_bkg.SetFillColor(rt.kGray)
	QCD_bkg.SetLineColor(rt.kGray)
    
        tag = Combine_year_tag[year]
        #for i in range(1,top_sig.GetNbinsX()+1):
        #        print "--------------------"
        #        print "top sig : ",top_sig.GetBinContent(i), top_sig.GetBinError(i)
        #        print "top BKG : ",top_bkg.GetBinContent(i), top_bkg.GetBinError(i)
        #        print "EWK BKG : ",EWK_bkg.GetBinContent(i), EWK_bkg.GetBinError(i)
        #        print "QCD DDD : ",QCD_bkg.GetBinContent(i), QCD_bkg.GetBinError(i)
 
        print(top_sig.Integral()," ",top_bkg.Integral()," ",EWK_bkg.Integral()," ",QCD_bkg.Integral())
        if(DNN_recale=="1"):
            Norm_and_error_from_fit = Get_Norm_N_error(errors=True,InFile = fitdignostic_outrootfile,year=year)
            del fitdignostic_outrootfile
           
            top_sig_norm_postfit = Norm_and_error_from_fit[lep+'jets'+tag]['top_sig_1725'+tag]['S+B-Fit']['Norm']
            top_bkg_norm_postfit = Norm_and_error_from_fit[lep+'jets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Norm']
            EWK_bkg_norm_postfit = Norm_and_error_from_fit[lep+'jets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Norm']
            QCD_bkg_norm_postfit = Norm_and_error_from_fit[lep+'jets'+tag]['QCD_DD'+tag]['S+B-Fit']['Norm']
            print("\n new postfit Norms: \n top_sig_1725 : %s, top_bkg_1725 : %s, EWK_bkg : %s, QCD_DD : %s" % (top_sig_norm_postfit,top_bkg_norm_postfit,EWK_bkg_norm_postfit,QCD_bkg_norm_postfit))
             

            top_sig_norm_prefit = Norm_and_error_from_fit[lep+'jets'+tag]['top_sig_1725'+tag]['Pre-Fit']['Norm']
            top_bkg_norm_prefit = Norm_and_error_from_fit[lep+'jets'+tag]['top_bkg_1725'+tag]['Pre-Fit']['Norm']
            EWK_bkg_norm_prefit = Norm_and_error_from_fit[lep+'jets'+tag]['EWK_bkg'+tag]['Pre-Fit']['Norm']
            QCD_bkg_norm_prefit = Norm_and_error_from_fit[lep+'jets'+tag]['QCD_DD'+tag]['Pre-Fit']['Norm']
            print("\n new prefit Norms: \n top_sig_1725 : %s, top_bkg_1725 : %s, EWK_bkg : %s, QCD_DD : %s" % (top_sig_norm_prefit,top_bkg_norm_prefit,EWK_bkg_norm_prefit,QCD_bkg_norm_prefit))
            
            top_sig_cons_el = (Norm_and_error_from_fit['eljets'+tag]['top_sig_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['top_sig_1725'+tag]['S+B-Fit']['Norm'])*100
            top_sig_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['top_sig_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['top_sig_1725'+tag]['S+B-Fit']['Norm'])*100
            top_sig_cons = top_sig_cons_el if(top_sig_cons_el > top_sig_cons_mu) else top_sig_cons_mu

            top_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Norm'])*100
            top_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Norm'])*100
            top_bkg_cons = top_bkg_cons_el if(top_bkg_cons_el > top_bkg_cons_mu) else top_bkg_cons_mu

            EWK_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Norm'])*100
            EWK_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Norm'])*100
            EWK_bkg_cons = EWK_bkg_cons_el if(EWK_bkg_cons_el > EWK_bkg_cons_mu) else EWK_bkg_cons_mu

            QCD_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['QCD_DD'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['QCD_DD'+tag]['S+B-Fit']['Norm'])*100
            QCD_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['QCD_DD'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['QCD_DD'+tag]['S+B-Fit']['Norm'])*100
            QCD_bkg_cons = QCD_bkg_cons_el if(QCD_bkg_cons_el > QCD_bkg_cons_mu) else QCD_bkg_cons_mu

            print("\n new constraints : \n top_sig_1725 : %s , top_bkg_1725 : %s , EWK_bkg : %s , QCD_DD : %s  \n" % (round(top_sig_cons,2),round(top_bkg_cons,2),round(EWK_bkg_cons,2),round(QCD_bkg_cons,2)))
        
            print("\n hist integral before rescaling: \n top_sig_1725 : %s , top_bkg_1725 : %s , EWK_bkg : %s , QCD_DD : %s  \n" % (top_sig.Integral(),top_bkg.Integral(),EWK_bkg.Integral(),QCD_bkg.Integral())
        #top_sig_1725 : 201394.006714 , top_bkg_1725 : 181647.221924 , EWK_bkg : 89704.8017273 , QCD_DD : 30032.5866966  
)
            top_sig.Scale(top_sig_norm_postfit/top_sig_norm_prefit)
            top_bkg.Scale(top_bkg_norm_postfit/top_bkg_norm_prefit)
            EWK_bkg.Scale(EWK_bkg_norm_postfit/EWK_bkg_norm_prefit)    
            QCD_bkg.Scale(QCD_bkg_norm_postfit/QCD_bkg_norm_prefit)
            print("\n hist integral after rescaling: \n top_sig_1725 : %s , top_bkg_1725 : %s , EWK_bkg : %s , QCD_DD : %s  \n" % (top_sig.Integral(),top_bkg.Integral(),EWK_bkg.Integral(),QCD_bkg.Integral()))
            del top_sig_norm_postfit,top_bkg_norm_postfit,EWK_bkg_norm_postfit,QCD_bkg_norm_postfit,top_sig_norm_prefit,top_bkg_norm_prefit,EWK_bkg_norm_prefit,QCD_bkg_norm_prefit

	    propagate_rate_uncertainity(top_sig, top_sig_cons)
	    propagate_rate_uncertainity(top_bkg, top_bkg_cons)
	    propagate_rate_uncertainity(EWK_bkg, EWK_bkg_cons)
  	    propagate_rate_uncertainity(QCD_bkg, QCD_bkg_cons)


	hMC = top_sig.Clone()
	hMC.Add(top_bkg)
	hMC.Add(EWK_bkg)
	hMC.Add(QCD_bkg)
        #hMC.GetXaxis().SetRangeUser(0.0, 150)

        hMC_unct_band = hMC.Clone()
        #hMC_unct_band.GetXaxis.SetLabelSize(0.0)
        hMC_unct_band.SetLineColor(rt.kGray+3)
        hMC_unct_band.SetFillColor(rt.kGray+3)
        hMC_unct_band.SetFillStyle(3018)
        #hMC_unct_band.GetXaxis().SetRangeUser(0.0, 150)

	Data = Dir.Get("data_obs")
	Data.SetMarkerColor(1)
	Data.SetMarkerStyle(20)
	Data.SetLineColor(rt.kBlack)
        #Data.GetXaxis().SetRangeUser(0.0, 150)

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
	legend.AddEntry(top_sig, "sig. top","f")#"Corr. top ", "f")
	legend.AddEntry(top_bkg, "top bkg", "f")#"InCorr. top ", "f")
	legend.AddEntry(EWK_bkg, "V+Jets, VV", "f")
	legend.AddEntry(QCD_bkg, "QCD", "f")
	#legend.AddEntry(hMC,"Total Unc.","f")



	myComingCanvases = rt.TCanvas("c1","", 600,600,600,600)
	myComingCanvases.cd()
	rt.TGaxis.SetMaxDigits(3)

	top_sig.GetXaxis().SetTitle(top_sig.GetXaxis().GetTitle()) 
     	hs = rt.THStack("hs",";"";Events")
	hs.Add(QCD_bkg)
	hs.Add(EWK_bkg)
	hs.Add(top_bkg)
	hs.Add(top_sig)
	hs.SetMaximum(Data.GetMaximum() * 1.2)
	#hs.GetHistogram().GetXaxis().SetRangeUser(0.0, 150.0)
        #reset_stack_range(hs, 0.0, 150)

	pad1 = rt.TPad('pad1', 'pad1', 0.0, 0.195259, 1.0, 0.990683)
	pad1.SetBottomMargin(0.089)
	pad1.SetTicky()
	pad1.SetTickx()
	#pad1.SetRightMargin(0.143)
        #pad1.SetLogy()
	pad1.Draw()
	pad1.cd()

	hs.Draw("hist")
	legend.Draw()

        CMSpreliminary = getCMSpre_tag(0.38, 0.84, 0.46, 0.88)
        CMSpreliminary.Draw("same")
        lepjet_tag = leptonjet_tag(lep,0.32, 0.80, 0.43, 0.83)
        lepjet_tag.Draw("same")
        #region_tag = getregion_tag("2J1T", 0.17, 0.92, 0.22, 0.96)
        #region_tag.Draw("same")
        yearNlumitag = year_tag(year,0.82, 0.92, 0.9, 0.96)
        yearNlumitag.Draw("same")

	myComingCanvases.Update()
        hMC_unct_band.Draw("E2;same")
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

	#print Data.GetBinContent(6)
        #print hMC.GetBinContent(6)
	h_ratio = rt.TGraphAsymmErrors(Data, hMC, 'pois')
        #h_ratio.Print()
	axis = h_ratio.GetXaxis()
	axis.SetLimits(Data.GetXaxis().GetXmin(), Data.GetXaxis().GetXmax())
	h_ratio.SetMarkerColor(1)
	h_ratio.SetMarkerStyle(20)
	h_ratio.SetMarkerSize(0.89)
	h_ratio.SetLineColor(rt.kBlack)


	h2_ratio = Data.Clone()
	h2_ratio.Divide(hMC)
	nbin = h2_ratio.GetXaxis().GetNbins()
	#ledge = h2_ratio.GetXaxis().GetXmin()
	#uedge = h2_ratio.GetXaxis().GetXmax()
	band = top_sig.Clone();band.Reset();band.SetTitle("")  #rt.TH1D('Band', '', nbin, ledge, uedge)
	rt.gStyle.SetOptStat(0)
	for i in range(nbin):
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
        band.GetXaxis().SetTitle(top_sig.GetXaxis().GetTitle()) 
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
        print(Fitdignostic_outFile)
        if ("Run2.root" in Fitdignostic_outFile) and DNN_recale==True:
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+"_comb.png")
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+"_comb.pdf")
	elif(DNN_recale==True):
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+".png")	
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+".pdf")
        else:
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+"_prefit.png")	
                myComingCanvases.Print("Plots/"+top_sig.GetXaxis().GetTitle()+"_validation_"+lep+"_"+dataYear+"_prefit.pdf")
        

if __name__ == "__main__":

        lep = args.lepton[0]
        year= args.year[0]
        DNN_recale = args.DNNscale[0]
        Combine_InFile = args.combine_InFile[0]
        Fitdignostic_outFile = args.fitdignostic_outFile[0]
        print DNN_recale
        stack_plot_from_histfile(lep,year,DNN_recale,Combine_InFile,Fitdignostic_outFile)

