import ROOT as rt
import numpy as np
import scipy.integrate as sp
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

#print
#print(args)

lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]



def Nomi_QCD_NoNQCD_Integral(lep="mu",year="UL2017",Variable="mtwMass",MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",EvtWeight_Fpaths_Iso = {},Data_AntiIso_Fpath=""):
    print
    print("calculating Integral of QCD and NON QCD with DNN Cut .. .. .. .. .. .. ... .......")
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    #print(lepton)
    
    if(Variable=="lntopMass"):
            Variable="TMath::Log(topMass)"
            X_axies="ln(m_{Top})"
            Y_axies="Events/(20)"
            lest_bin=math.log(100.0)
            max_bin=math.log(400.0)
            Num_bin=15

    elif(Variable=="mtwMass"):
            X_axies="m_{T} (GeV)"
            Y_axies="Events/(10)"
            lest_bin=0.0
            max_bin=200.0
            Num_bin=20
 
    elif(Variable=="topMass"):
            X_axies="m_{Top}"
            Y_axies="Events/(20)"
            lest_bin=100.0
            max_bin=400.0
            Num_bin=15
    
    elif(Variable=="t_ch_CAsi+ttbar_CAsi"):
            X_axies="Signal+TopBkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
            
    elif(Variable=="t_ch_CAsi"):
            X_axies="Signal Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
      
    elif(Variable=="t_ch_WAsi"):
            X_axies="Signal Wrong Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="ttbar_CAsi"):
            X_axies="top bkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="ttbar_WAsi"):
            X_axies="top bkg Wrong Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="EWK"):
            X_axies="EWK bkg DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="QCD"):
            X_axies="QCD bkg DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
    
    hist = {}
    WAssihist = {}
    infiles = {}
    intree = {}
    
    hist_tch_CAssig_temp = rt.TH1F('hist_sig_CAssig_temp', '', Num_bin, lest_bin, max_bin)
    hist_tch_WAssig_temp = rt.TH1F('hist_sig_WAssig_temp', '', Num_bin, lest_bin, max_bin)
    hist_ttbar_CAssig_temp = rt.TH1F('hist_bkg_CAssig_temp', '', Num_bin, lest_bin, max_bin)
    hist_ttbar_WAssig_temp = rt.TH1F('hist_big_WAssig_temp', '', Num_bin, lest_bin, max_bin)
    hist_EWK_temp = rt.TH1F('hist_EWK_temp', '', Num_bin, lest_bin, max_bin)
    hist_QCD_temp = rt.TH1F('hist_QCD_temp', '', Num_bin, lest_bin, max_bin)
    rt.gStyle.SetOptStat(0)
    
    hist_tch_CAssig_temp.SetLineColor(rt.kRed);hist_tch_CAssig_temp.SetLineWidth(2)
    hist_tch_CAssig_temp.GetXaxis().SetTitle(X_axies)
    hist_tch_CAssig_temp.GetYaxis().SetTitle(Y_axies)  
    
    hist_tch_WAssig_temp.SetLineColor(rt.kBlue); hist_tch_WAssig_temp.SetLineWidth(2)
    hist_ttbar_CAssig_temp.SetLineColor(rt.kOrange-1); hist_ttbar_CAssig_temp.SetLineWidth(2)
    hist_ttbar_WAssig_temp.SetLineColor(rt.kCyan+1); hist_ttbar_WAssig_temp.SetLineWidth(2)
    hist_EWK_temp.SetLineColor(rt.kMagenta); hist_EWK_temp.SetLineWidth(2)
    hist_QCD_temp.SetLineColor(rt.kGray); hist_QCD_temp.SetLineWidth(2)
    print
    
    for channel in channels:
        if(channel=="QCD"): 
                print channel, " ", Data_AntiIso_Fpath
                infiles[channel] = rt.TFile(Data_AntiIso_Fpath, 'READ')
        else:
                print channel, " ", EvtWeight_Fpaths_Iso[channel]
                infiles[channel] = rt.TFile(EvtWeight_Fpaths_Iso[channel], 'READ')
    
        intree[channel] = infiles[channel].Get('Events')
        hist[channel] = rt.TH1F('hist' + channel, '', Num_bin, lest_bin, max_bin)
        WAssihist[channel] = rt.TH1F('temphist' + channel, '', Num_bin, lest_bin, max_bin)
    
        if(channel=='Tchannel' or channel=='Tbarchannel'):
            Mccut_corr_assi = MCcut +"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)"
            #print "Mccut_corr_assi : ",Mccut_corr_assi
            intree[channel].Project('hist' + channel, Variable, Mccut_corr_assi) 
            Mccut_wron_assi = MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"
            intree[channel].Project('temphist' + channel, Variable,Mccut_wron_assi)
            #print "Mccut_wron_assi : ",Mccut_wron_assi
            hist_tch_CAssig_temp.Add(hist[channel])
            hist_tch_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        elif(channel=='tw_top'  or channel=='tw_antitop' or channel=='Schannel' or channel=='ttbar_SemiLeptonic' or channel=='ttbar_FullyLeptonic'):
            intree[channel].Project('hist' + channel, Variable,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)")
            intree[channel].Project('temphist' + channel, Variable,MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)")
            hist_ttbar_CAssig_temp.Add(hist[channel])
            hist_ttbar_WAssig_temp.Add(WAssihist[channel])
            #hist[channel].Print()
            #WAssihist[channel].Print()
        elif(channel=='QCD'):
            intree[channel].Project('hist' + channel, Variable,Datacut)
            hist_QCD_temp.Add(hist[channel])
            #hist_QCD_temp.Print()
        else:
            #print MCcut
            intree[channel].Project('hist' + channel,Variable,MCcut)
            hist_EWK_temp.Add(hist[channel])
            #hist[channel].Print()
    
    NonQCD_Inte = (hist_tch_CAssig_temp.Integral(0,Num_bin)+hist_tch_WAssig_temp.Integral(0,Num_bin)+hist_ttbar_CAssig_temp.Integral(0,Num_bin)+hist_ttbar_WAssig_temp.Integral(0,Num_bin)+hist_EWK_temp.Integral(0,Num_bin))
    QCD_Inte = (hist_QCD_temp.Integral(0,Num_bin+1))
    print 
    print "NonQCD_Inte: ",NonQCD_Inte," QCD_Inte: ",QCD_Inte
    
    return NonQCD_Inte,QCD_Inte


if __name__ == "__main__":
    NonQCD_Inte,QCD_Inte =  Nomi_QCD_NoNQCD_Integral()
    print "NonQCD_Inte: ",NonQCD_Inte," QCD_Inte: ",QCD_Inte
    
    #c1.Print('Plots/'+year+'_'+lep+'_'+Variable+'.png')#'_cut_tch_CAssig_p_ttbar_CAssigGT0p4.png')
    #c1.Print('Plots/'+year+'_'+lep+'_'+Variable+'.pdf')#'_cut_tch_CAssig_p_ttbar_CAssigGT0p4.pdf')
