import sys
import ROOT as rt
import numpy as np
import argparse as arg
import math

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")

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

#print(args)

lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]

def get_histogram_with_DNN_cut(lep="mu",year="UL2017",Variable="lntopMass",
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L'],
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",
    DNNcut="*(t_ch_CAsi>0.7)",Fpaths_DNN_score = {}, Fpaths_ori_with_weight = {}):


        if(lep=="mu"):
                lepton = "Muon"
        elif(lep=="el"):
                lepton = "Electron"

	if(Variable=="lntopMass"):
	 	Variable="TMath::Log(topMass)"
	 	X_axies="ln(m_{t})"
	 	Y_axies="Events/(0.092)"
	 	lest_bin=rt.TMath.Log(100.0)
	 	max_bin=rt.TMath.Log(400.0)
	 	Num_bin=15 #one extra overflow bin will be added 
	 
	elif(Variable=="topMass"):
	 	X_axies="m_{t}"
	 	Y_axies="Events/(10)"
	 	lest_bin=100.0
	 	max_bin=400.0
	 	Num_bin=30 #one extra overflow bin will be added
        elif(Variable=="MuonEta"):
                X_axies="|#eta_{#mu}|"
                Y_axies="Events/(0.1)"
                lest_bin=-2.5
                max_bin=2.5
                Num_bin=25
	elif(Variable == "muSF" and lep=="mu"):
                Variable=="muSF"
	 	X_axies="Muon Scale factor"
	 	Y_axies="Events/0.1"
                lest_bin=0.7
                max_bin=1.2	
	 	Num_bin=25
        elif(Variable=="PUJetID_SF"):
                Variable="bJetPUJetID_SF*lJetPUJetID_SF"
	 	X_axies="jet PUSF"
	 	Y_axies="Events/0.1"
                lest_bin=0.7
                max_bin=1.2	
	 	Num_bin=25
        elif(Variable=="lJetPUJetID_SF"):
                Variable="lJetPUJetID_SF"
	 	X_axies="l jet puSF"
	 	Y_axies="Events/0.1"
                lest_bin=0.7
	elif(Variable=="bJetPUJetID_SF"):
                Variable="bJetPUJetID_SF"
	 	X_axies="b jet puSF"
	 	Y_axies="Events/0.1"
                lest_bin=0.7
	 	Num_bin=25
	        Num_bin=25
        elif(Variable == "elSF" and lep=="el"):
                Variable=="elSF"
                X_axies="ELectron Scale factor"
                Y_axies="Events/0.1"
                lest_bin=0.7
                max_bin=1.2
                Num_bin=25
        elif(Variable == "bWeight"):
                X_axies="Weight for b quark"
                Y_axies="Events/(0.05)"
                lest_bin=0.4
                max_bin=2.4
                Num_bin=40
        elif(Variable == "puWeight"):
                X_axies="PileUp Weight"
                Y_axies="Events/(0.05)"
                lest_bin=0.0
                max_bin=2.0
                Num_bin=40
        elif(Variable == "puWeight_new"):
                X_axies="new PileUp Weight"
                Y_axies="Events/(0.05)"
                lest_bin=0.0
                max_bin=2.0
                Num_bin=40
        elif(Variable == "bJetdeepJet"):
                X_axies="deep Jet Score for b Jets"
                Y_axies="Events/(0.05)"
                lest_bin=-1
                max_bin=1.1
                Num_bin=42
        elif(Variable=="L1PreFiringWeight_Nom"):
                X_axies="L1 PreFire Weight"
                Y_axies="Events/(0.05)"
                lest_bin=0.5
                max_bin=1.1
                Num_bin=12
        elif(Variable == "mtwMass"):
                X_axies="m_{t}"
                Y_axies="Events/(10)"
                lest_bin=0
                max_bin=200
                Num_bin=20
        elif(Variable=="dEta_mu_bJet" or Variable=="dEta_el_bJet"):
                X_axies="|#Delta#eta_{lb}|"
                Y_axies="Events/(0.1)"
                lest_bin=0.0
                max_bin=3.0
                Num_bin=30
	elif(Variable=="bJetPt"):
                X_axies="b-jet p_{T} (GeV)"
                Y_axies="Events/(5 GeV)"
                lest_bin=0.0
                max_bin=200.0
                Num_bin=40
	elif(Variable=="lJetEta"):
                Variable="abs(lJetEta)";
                X_axies="light jet #eta"
                Y_axies="Events/(0.5)"
                lest_bin=0.0
                max_bin=5.0
                Num_bin=10
        elif(Variable=="lJetPt"):
                X_axies="light jet p_{T} (GeV)"
                Y_axies="Events/(5 GeV)"
                lest_bin=0.0
                max_bin=200.0
                Num_bin=40.0
        elif(Variable=="abs_lJetEta"):
                Variable="abs(lJetEta)"
                X_axies="light jet |#eta|"
                Y_axies="Events/(0.5)"
                lest_bin=0.0
                max_bin=5.0
                Num_bin=10
        elif(Variable=="jetpTSum"):
                X_axies="p_{T}^{b}+p_{T}^{j'} {GeV)"
                Y_axies="Events/(20 GeV)"
                lest_bin=0.0
                max_bin=500.0
                Num_bin=25
        elif(Variable=="diJetMass"):
                X_axies="m_{bj'} {GeV)"
                Y_axies="Events/(20 GeV)"
                lest_bin=0.0
                max_bin=600.0
                Num_bin=30
        elif(Variable=="cosThetaStar"):
                X_axies="cos#theta*"
                Y_axies="Events/(0.1)"
                lest_bin=-1.0
                max_bin=1.0
                Num_bin=20
        elif(Variable=="dR_bJet_lJet"):
                X_axies="#DeltaR_{bj'}"
                Y_axies="Events/(0.2 )"
                lest_bin=0.0
                max_bin=5.2
                Num_bin=27
        elif(Variable=="FW1"):
                X_axies="FW1"
                Y_axies="Events/(0.5)"
                lest_bin=0.0
                max_bin=1.0
                Num_bin=20
        elif(Variable=="ElectronSCEta"):
                X_axies="electron #eta_{SC}"
                Y_axies="Events/(0.5)"
                lest_bin=-2.5
                max_bin=2.5
                Num_bin=10
        elif(Variable=="ElectronEta"):
                X_axies="electron |#eta|"
                Y_axies="Events/(0.1)"
                lest_bin=-2.5
                max_bin=2.5
                Num_bin=25	
        elif(Variable=="t_ch_CAsi"):
                X_axies="DNN Response for corr. assign top signal"
                Y_axies="Events/(0.1)"
                lest_bin=0.0
                max_bin=1.0
                Num_bin=10
	else:
		print "variable ", Variable," in not define in Get_Histogram_after_DNN_cuts.py" 
		exit()


	print
	print "############################   analising the event with the DNN cut applid ", DNNcut, "  ##################"
	print "lepton = ",lep
	print "Variable = ",Variable
	print
	# Initializing lists for histogram, TFile, TTree of Iso
	histo_corr_Array = []
        histo_wron_Array = []
	#intree = []
	rt.gROOT.cd()

	print Variable
	print "bining: ",Num_bin,", ",lest_bin,", ", max_bin

	histo_corr = rt.TH1F('histo_corr', Variable, Num_bin,lest_bin,max_bin)
        histo_wron = rt.TH1F('histo_wron', Variable, Num_bin,lest_bin,max_bin)

	#histo_corr.Sumw2()
        MCcut_corr_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)"
        MCcut_wron_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"
	for channel in channels:
    	    print channel, "  ", Fpaths_ori_with_weight[channel]
            print channel, "  ", Fpaths_DNN_score[channel]
    	    histo_corr.Reset()
            histo_wron.Reset()
            
            #print filenamei
            MCFile = rt.TFile.Open(Fpaths_ori_with_weight[channel],'Read')	
    	    intree = MCFile.Get('Events')
            intree.AddFriend ("Events",Fpaths_DNN_score[channel])
	    #intree[-1].Print()
            rt.gROOT.cd()
            
    	    intree.Project('histo_corr', Variable, MCcut_corr_Assig)
            intree.Project('histo_wron', Variable, MCcut_wron_Assig)
            
    	    histo_corr_Array.append(histo_corr.Clone())
            histo_wron_Array.append(histo_wron.Clone())
	    histo_corr_Array[-1].SetName(channel)
            histo_wron_Array[-1].SetName(channel)
            histo_corr.Print()
            histo_wron.Print()
            
            del intree

	histo_corr_Array[0].GetXaxis().SetTitle(X_axies)
        histo_wron_Array[0].GetXaxis().SetTitle(X_axies)

        return histo_corr_Array,histo_wron_Array

if __name__ == '__main__':
   
        channels = ['Tchannel']#, 'Tbarchannel', 'tw_top', 'tw_antitop', 'Schannel',
           #'ttbar', 'WToLNu_0J', 'WToLNu_1J', 'WToLNu_2J', 'DYJetsToLL',
           #'WWTo1L1Nu2Q', 'WWTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo2L2Q', 'ZZTo2L2Q',
           #'QCD']
        
        for channel in channels:
           Fpaths_DNN_score[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
           if(year=="ULpreVFP2016"): 
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="ULpostVFP2016"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2017"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2018"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"    

        applydir = 'DNN_output_without_mtwCut/Apply_all/' 
        hists_corr,hists_wron = get_histogram_with_DNN_cut(lep,year,Variable)
        print(len(hists))
        for hist in hists:
             hist.Print()


