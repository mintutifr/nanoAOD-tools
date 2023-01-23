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

#print(args)

lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]

def get_histogram_with_DNN_cut(lep="mu",year="UL2017",Variable="lntopMass",applydir = 'DNN_output_without_mtwCut/Apply_all/',
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L'],
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",
    DNNcut="*(t_ch_CAsi>0.7)",Fpaths_DNN_score = {}, EvtWeight_Fpaths_Iso = {}):

    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    if(Variable=="lntopMass"):
            Variable="TMath::Log(topMass)"
            X_axies="ln(m_{Top})"
            Y_axies="Events/(20)"
            lest_bin=math.log(100.0)
            max_bin=math.log(400.0)
            Num_bin=15
    
    elif(Variable=="topMass"):
            X_axies="m_{Top}"
            Y_axies="Events/(20)"
            lest_bin=100.0
            max_bin=400.0
            Num_bin=15

    elif(Variable=="mtwMass"):
            X_axies="m_{T} (GeV)"
            Y_axies="Events/(10)"
            lest_bin=0.0
            max_bin=200.0
            Num_bin=20
    
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
    
    
    Fpaths_DNN_score = {}
    EvtWeight_Fpaths_Iso = {}
    for channel in channels:
            Fpaths_DNN_score[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            if(year=="ULpreVFP2016"): 
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            elif(year=="ULpostVFP2016"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            elif(year=="UL2017"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            elif(year=="UL2018"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
    
               
    #print EvtWeight_Fpaths_Iso
      
    #define histoframs
    hs_array = []
    WAssihs_array = []
    infiles = {}
    intree = {}

   
    hist_corr = rt.TH1F('hist_corr', 'hist_corr', Num_bin, lest_bin, max_bin)
    hist_wron = rt.TH1F('hist_wron', 'hist_wron', Num_bin, lest_bin, max_bin)
   
 
    print    
    print "analysising tree withh DNN cut : ", DNNcut, " .. .. .. .... ..... ..."
    print 
    for channel in channels:
        hist_corr.Reset()
        hist_wron.Reset()
        print channel, " ", EvtWeight_Fpaths_Iso[channel]
        infiles[channel] = rt.TFile.Open(EvtWeight_Fpaths_Iso[channel], 'READ')
        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",Fpaths_DNN_score[channel])

        MCcut_corr_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)" 
        MCcut_wron_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"

        rt.gROOT.cd()        
        intree[channel].Project('hist_corr', Variable, MCcut_corr_Assig)
        intree[channel].Project('hist_wron', Variable, MCcut_wron_Assig)
         
        hs_array.append(hist_corr)
        hs_array[-1].SetName(channel)
        WAssihs_array.append(hist_wron)
        WAssihs_array[-1].SetName(channel)
        #hs_array[-1].Print()

    
    #hs_array[0].Print() 
    return hs_array, WAssihs_array

if __name__ == "__main__":
    hists_corr, hists_wron = get_histogram_with_DNN_cut(lep,year,Variable,'DNN_output_without_mtwCut/Apply_all/') 
    for hist in hists_corr:
         hist.Print()
  
    #print hists_wron
