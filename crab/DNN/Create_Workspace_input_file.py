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

print(args)

lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]

from Get_Nomi_histogram_Integral import Nomi_QCD_NoNQCD_Integral 
from Get_Histogram_after_DNN_cuts_v3 import get_histogram_with_DNN_cut 
def Create_Workspace_input_file(lep="mu",year="UL2017",Variable="lntopMass"):

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
    
   ################################################## QCD and NonQCD scale form mtw fit ############################# 
    if(year == "ULpreVFP2016"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 10991.0
                   NonQCDScale_mtwFit = 231378.0
            if(lep=="el"):
                   QCDScale_mtwFit = 6892.0
                   NonQCDScale_mtwFit = 146947.0
    if(year == "ULpostVFP2016"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 11457.0
                   NonQCDScale_mtwFit = 209030.0
            if(lep=="el"):
                   QCDScale_mtwFit = 12848.0
                   NonQCDScale_mtwFit = 122089.0
    if(year == "UL2017"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 30145.0
                   NonQCDScale_mtwFit = 472746.0
            if(lep=="el"):
                   QCDScale_mtwFit = 7509.0
                   NonQCDScale_mtwFit = 315426.0
    #################### Genral Dir and selection ##################################################
    
    applydir = 'DNN_output_without_mtwCut/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut="*(t_ch_CAsi>0.7)"
    
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']


    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            if(year=="ULpreVFP2016"): 
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="ULpostVFP2016"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="UL2017"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="UL2018"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
    
               
    #print EvtWeight_Fpaths_Iso
      
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # claculation of the scale QCD and NonQCD
    #NonQCD_Inte,QCD_Inte = Nomi_QCD_NoNQCD_Integral(lep,year,Variable,MCcut,Datacut,EvtWeight_Fpaths_Iso,Data_AntiIso_Fpath)
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut , Datacut , DNNcut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso
    del Data_AntiIso_Fpath
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 

    MCSF = 1#NonQCDScale_mtwFit/NonQCD_Inte
    QCDSF = 1#QCDScale_mtwFit/QCD_Inte
    print
    print "MCSF: ",MCSF," QCDSF: ",QCDSF

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi[:-1]):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Scale(MCSF)
        hist_wron_assig[channel].Scale(MCSF)        

    del hists_corr
    del hists_wron

    #print hist_corr_assig
    #print hist_wron_assig
    top_sig_Nomi = hist_corr_assig["Tchannel"]; top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_172p5")

    top_bkg_Nomi = hist_wron_assig["Tchannel"]; top_bkg_Nomi.Add(hist_wron_assig["Tbarchannel"]);
    for channel in ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_Nomi.Add(hist_corr_assig[channel]); top_bkg_Nomi.Add(hist_wron_assig[channel]) 
    top_bkg_Nomi.SetLineColor(rt.kOrange-1); top_bkg_Nomi.SetLineWidth(2)
    top_bkg_Nomi.SetName("top_bkg_172p5")
    
    hist_EWK = hist_corr_assig["WJetsToLNu_0J"]; hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.SetName("EWK_bkg")

    #################### Data and DD QCD  ######################################################## 
    print    
    print "Data and DDQCD with ", DNNcut, " .. .. .. .... ..... ..."
    print
    
    hs = {}
    infiles = {}
    intree = {}
    Fpaths_DNN_apply = {}
    rt.gStyle.SetOptStat(0)
    
    Data_AntiIso_Fpath = ""
    Data_Iso_Fpath = "" 
    for channel in ["QCD","Data"+year]:
           Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
    if(year=="ULpreVFP2016"):
        Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        Data_Iso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_Data"+year+"_2J1T1_"+lep+".root"
    elif(year=="ULpostVFP2016"):
        Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        Data_Iso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_Data"+year+"_2J1T1_"+lep+".root"
    elif(year=="UL2017"):
        Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        Data_Iso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_Data"+year+"_2J1T1_"+lep+".root"
    elif(year=="UL2018"):
        Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        Data_Iso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_Data"+year+"_2J1T1_"+lep+".root"
    
    #print Fpaths_DNN_apply

    for channel_no,channel in enumerate(["QCD","Data"+year]):
        if(channel=="QCD"):
                print channel, " ", Data_AntiIso_Fpath
                print channel, " ", Fpaths_DNN_apply[channel]
                infiles[channel] = rt.TFile.Open(Data_AntiIso_Fpath, 'READ')
        else:
                print channel, " ", Data_Iso_Fpath
                print channel, " ", Fpaths_DNN_apply[channel]
                infiles[channel] = rt.TFile.Open(Data_Iso_Fpath, 'READ')

        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",Fpaths_DNN_apply[channel])

        hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
        #rt.gROOT.cd()
    
        intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut)
        
    Data = hs['Data'+year].Clone()
    rt.gROOT.cd()
    DDQCD = hs['QCD'].Clone()
    DDQCD.Scale(QCDSF)
    DDQCD.SetName("QCD_DD")
    DDQCD.Print()
    DDQCD.SetLineColor(rt.kGray); DDQCD.SetLineWidth(2)
    
    del hs
    del Data_Iso_Fpath,Data_AntiIso_Fpath
    
    hist_to_return = [] 

    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(top_bkg_Nomi)
    hist_to_return.append(hist_EWK)
    hist_to_return.append(DDQCD)

    return hist_to_return


if __name__ == "__main__":
    
    hists = Create_Workspace_input_file(lep,year,Variable) 
    outfile = rt.TFile("Combine_Input_histograms.root","recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir("mujets")
    Dir_mu.cd()
    
    for hist in hists:
        hist.Write()
        
    rt.gROOT.cd()
 
    outfile.cd()
    Dir_el = outfile.mkdir("eljets")
    Dir_el.cd()

    rt.gROOT.cd()

    outfile.Close()

    
