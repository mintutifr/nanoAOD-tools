import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys 
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
parser.add_argument('-f', '--fitdignostic_outFile ', dest='fitdignostic_outFile', type=str, default=[ None ],nargs=1, help="DNNFit dignostic output file which has histogram files i.e /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2017.root")
parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ 0.0 ,0.7]")

args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>] -v <variable>"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.lepton[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

if (args.var == None):
        print("Error: Incorrect choice of Variable, use -v <variable>"%(sys.argv [0]))
        sys.exit (1)

print(args)

lep = args.lepton[0]
year= args.year[0]
Variable = args.var[0]
DNNFit_rescale_file = args.fitdignostic_outFile[0]
DNNCut = args.DNNCut[0]
from Histogram_discribtions import get_histogram_distciption 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Get_Nomi_histogram_Integral import Nomi_QCD_NoNQCD_Integral 
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from mlfitNormsToText import *

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)



def Create_Workspace_input_file(lep="mu",year="UL2017",Variable="lntopMass"):

    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)
                
    yearDir={
                'UL2016preVFP' :  "SIXTEEN_preVFP",
                'UL2016postVFP' : "SIXTEEN_postVFP",
                'UL2017' : "SEVENTEEN",
                'UL2018' : "EIGHTEEN"}
    Combine_year_tag={
                'UL2016preVFP' :  "_ULpre16",
                'UL2016postVFP' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"} 

    tag = Combine_year_tag[year]

    #################### Genral Dir and selection ##################################################
    
    applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
    DNNcut_str = "*(t_ch_CAsi>="+DNNCut+")" 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']


    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            if(channel=="QCD"): Data_AntiIso_Fpath =  "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
    
               
    #print EvtWeight_Fpaths_Iso
      
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # claculation of the scale QCD and NonQCD
    NonQCD_Inte,QCD_Inte = Nomi_QCD_NoNQCD_Integral(lep,year,Variable,MCcut,Datacut,EvtWeight_Fpaths_Iso,Data_AntiIso_Fpath,Fpaths_DNN_apply)
    # get histogram with DNN cut
    print(type(QCDcut),"=======================")
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut ,QCDcut, Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso
    del Data_AntiIso_Fpath

    #MCSF = NonQCDScale_mtwFit[lep][year]/NonQCD_Inte
    #QCDSF = QCDScale_mtwFit[lep][year]/QCD_Inte
    #print
    #print "MCSF: ",MCSF," QCDSF: ",QCDSF

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi[:-1]):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()

    del hists_corr
    del hists_wron

    top_sig_cons = 15.0 ; top_sig_DNNfitrescale = 1.0
    top_bkg_cons = 6.0  ; top_bkg_DNNfitrescale = 1.0
    EWK_bkg_cons = 10.0 ; EWK_bkg_DNNfitrescale = 1.0
    QCD_bkg_cons = 50.0 ; QCD_bkg_DNNfitrescale = 1.0

    if(DNNFit_rescale_file!=None):
        print("===================== geting new DNNFit rescale parapmeters =================")
        print("Reading the Normalization form the "+DNNFit_rescale_file)
        Norm_and_error_from_fit = Get_Norm_N_error(errors=True,InFile = DNNFit_rescale_file,year=year)
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
        top_sig_cons = top_sig_cons_el if(top_sig_cons_el >= top_sig_cons_mu) else top_sig_cons_mu

        top_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Norm'])*100
        top_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['top_bkg_1725'+tag]['S+B-Fit']['Norm'])*100
        top_bkg_cons = top_bkg_cons_el if(top_bkg_cons_el >= top_bkg_cons_mu) else top_bkg_cons_mu

        EWK_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Norm'])*100
        EWK_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['EWK_bkg'+tag]['S+B-Fit']['Norm'])*100
        EWK_bkg_cons = EWK_bkg_cons_el if(EWK_bkg_cons_el >= EWK_bkg_cons_mu) else EWK_bkg_cons_mu

        QCD_bkg_cons_el = (Norm_and_error_from_fit['eljets'+tag]['QCD_DD'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['eljets'+tag]['QCD_DD'+tag]['S+B-Fit']['Norm'])*100
        QCD_bkg_cons_mu = (Norm_and_error_from_fit['mujets'+tag]['QCD_DD'+tag]['S+B-Fit']['Error']/Norm_and_error_from_fit['mujets'+tag]['QCD_DD'+tag]['S+B-Fit']['Norm'])*100
        QCD_bkg_cons = QCD_bkg_cons_el if(QCD_bkg_cons_el >= QCD_bkg_cons_mu) else QCD_bkg_cons_mu

        print("\n new constraints : \n top_sig_1725 : %s , top_bkg_1725 : %s , EWK_bkg : %s , QCD_DD : %s  \n" % (round(top_sig_cons,2),round(top_bkg_cons,2),round(EWK_bkg_cons,2),round(QCD_bkg_cons,2)))

        top_sig_DNNfitrescale = top_sig_norm_postfit/top_sig_norm_prefit
        top_bkg_DNNfitrescale = top_bkg_norm_postfit/top_bkg_norm_prefit
        EWK_bkg_DNNfitrescale = EWK_bkg_norm_postfit/EWK_bkg_norm_prefit   
        QCD_bkg_DNNfitrescale = QCD_bkg_norm_postfit/QCD_bkg_norm_prefit
        print("===================== successfully got new DNNFit rescale parapmeters =================")
        
    print("top_sig_cons = %s ; top_bkg_cons = %s ; EWK_bkg_cons = %s ; QCD_bkg_cons = %s" % (top_sig_cons, top_bkg_cons, EWK_bkg_cons, QCD_bkg_cons))
    print("top_sig_DNNfitrescale = %s ; top_bkg_DNNfitrescale = %s ; EWK_bkg_DNNfitrescale = %s ; QCD_bkg_DNNfitrescale = %s "%(top_sig_DNNfitrescale, top_bkg_DNNfitrescale, EWK_bkg_DNNfitrescale, QCD_bkg_DNNfitrescale))
    top_sig_Nomi = hist_corr_assig["Tchannel"].Clone(); top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
    top_sig_Nomi.Scale(top_sig_DNNfitrescale)
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_1725"+tag)
    propagate_rate_uncertainity(top_sig_Nomi, top_sig_cons)

    missreco_single_top_bkg = hist_wron_assig["Tchannel"].Clone(); missreco_single_top_bkg.Add(hist_wron_assig["Tbarchannel"]);
    missreco_single_top_bkg.Scale(top_sig_DNNfitrescale)
    propagate_rate_uncertainity(missreco_single_top_bkg, top_sig_cons)

    top_bkg_Nomi = hist_corr_assig['tw_top'].Clone(); missrecotop_bkg_Nomi = hist_wron_assig['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_Nomi.Add(hist_corr_assig[channel]); missrecotop_bkg_Nomi.Add(hist_wron_assig[channel])
    missrecotop_bkg_Nomi.SetLineColor(rt.kOrange-1); missrecotop_bkg_Nomi.SetLineWidth(2)

    top_bkg_Nomi.Scale(top_bkg_DNNfitrescale)
    propagate_rate_uncertainity(top_bkg_Nomi, top_bkg_cons)

    missrecotop_bkg_Nomi.Scale(top_bkg_DNNfitrescale)
    propagate_rate_uncertainity(missrecotop_bkg_Nomi, top_bkg_cons)

    top_sig_Nomi.Add(top_bkg_Nomi)    
    missrecotop_bkg_Nomi.Add(missreco_single_top_bkg)

    missrecotop_bkg_Nomi.SetName("top_bkg_1725"+tag)
    

    hist_EWK = hist_corr_assig["WJetsToLNu_0J"].Clone();hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.SetName("EWK_bkg"+tag)
    hist_EWK.Scale(EWK_bkg_DNNfitrescale)
    propagate_rate_uncertainity(hist_EWK, EWK_bkg_cons)
    
    #for Bin in range(0,top_bkg_Nomi.GetNbinsX()+1):
    #                 print("Bin : %s, (%s,%s)"%(Bin,top_bkg_Nomi.GetBinContent(Bin),top_bkg_Nomi.GetBinError(Bin)))
    
    #################### Data and DD QCD  ######################################################## 
    print    
    print "Data and DDQCD with ", DNNcut_str, " .. .. .. .... ..... ..."
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
    Data_AntiIso_Fpath =  "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_QCD_Apply_all_'+lep+'.root'
    Data_Iso_Fpath =  "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
    
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
        if(channel=="QCD"):
            print(type(QCDcut),type(DNNcut_str))
            intree[channel].Project('hs' + channel, Variable,QCDcut+DNNcut_str)
        else:
            intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut_str)
        #hs[channel] = DrawOverflow_N_DrawUnderflow(hs[channel])
        #hs[channel].Print()
        
    rt.gROOT.cd()
    Data = hs['Data'+year].Clone()
    DDQCD = hs['QCD'].Clone()
    #DDQCD.Scale(QCDSF)
    DDQCD.SetName("QCD_DD"+tag)
    DDQCD.Scale(QCD_bkg_DNNfitrescale)
    propagate_rate_uncertainity(DDQCD, QCD_bkg_cons)
    #for i in range(1,DDQCD.GetNbinsX()+1):
    #    print "--------------------"
    #    print "QCD DDD : ",DDQCD.GetBinContent(i), DDQCD.GetBinError(i)
    DDQCD.Print()

    Data.SetName("data_obs")
    Data.Print()

    DDQCD.SetLineColor(rt.kGray); DDQCD.SetLineWidth(2)
    
    del hs
    del Data_Iso_Fpath,Data_AntiIso_Fpath



    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(missrecotop_bkg_Nomi)
    hist_to_return.append(hist_EWK)
    hist_to_return.append(DDQCD)
    hist_to_return.append(Data)

    """#################### ALternate mass and width  #################################################### 

    
    print "creating histogram for the Alt mass and with samples ............."
    print 
    Alt_mass = ["1695","1715","1735","1755"]
    Alt_width = ["0p55","0p7","1p3","1p45"]
    channels_Alt_ttbar_semi = []
    channels_Alt_ttbar_full_mass = []
    channels_Alt_ttbar_full_width = []
    channels_Alt_tch = []
    channels_Alt_tbarch = []
    for mass in Alt_mass:
        channels_Alt_ttbar_semi.append("ttbar_SemiLeptonic_mtop"+mass)
        channels_Alt_ttbar_full_mass.append("ttbar_FullyLeptonic_mtop"+mass)
        channels_Alt_tch.append("Tchannel_mtop"+mass)
        channels_Alt_tbarch.append("Tbarchannel_mtop"+mass)
    for width in Alt_width:
        channels_Alt_ttbar_full_width.append("ttbar_FullyLeptonic_widthx"+width)

    channels_Alt= channels_Alt_tch+channels_Alt_tbarch+channels_Alt_ttbar_semi+channels_Alt_ttbar_full_mass +channels_Alt_ttbar_full_width
    
    del channels_Alt_tch
    del channels_Alt_tbarch 
    del channels_Alt_ttbar_semi
    del channels_Alt_ttbar_full_mass
    
    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    
    for channel in channels_Alt:
            Fpaths_DNN_apply[channel] = applydir+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1_Alt/Minitree_"+channel+"_2J1T1_"+lep+".root"
    
    #print Fpaths_DNN_apply
    #print EvtWeight_Fpaths_Iso   
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Alt, MCcut , Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso

    hist_corr_assig = {}
    hist_wron_assig = {}
    
    #MCSF = 1 
    #QCDSF = 1
    for channel_no,channel in enumerate(channels_Alt):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Scale(MCSF)
        hist_wron_assig[channel].Scale(MCSF)        
    
    del hists_corr
    del hists_wron
    top_sig_alt = {}
    top_bkg_alt = {}
   

    for mass in Alt_mass:
        top_sig_alt["top_sig_"+mass] = rt.TH1F('top_sig_'+mass, '', Num_bin, lest_bin, max_bin)
        top_bkg_alt["top_bkg_"+mass] = rt.TH1F('top_bkg_'+mass, '', Num_bin, lest_bin, max_bin)

        top_sig_alt["top_sig_"+mass].Add(hist_corr_assig["Tchannel_mtop"+mass])
        top_sig_alt["top_sig_"+mass].Add(hist_corr_assig["Tbarchannel_mtop"+mass])

        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["Tchannel_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["Tbarchannel_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_corr_assig["ttbar_SemiLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["ttbar_SemiLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_corr_assig["ttbar_FullyLeptonic_mtop"+mass])
        top_bkg_alt["top_bkg_"+mass].Add(hist_wron_assig["ttbar_FullyLeptonic_mtop"+mass])

    for width in Alt_width:
        top_bkg_alt["top_bkg_Nomix"+width] = rt.TH1F('top_bkg_Nomix'+width, '', Num_bin, lest_bin, max_bin)
        top_bkg_alt["top_bkg_Nomix"+width].Add(hist_corr_assig["ttbar_FullyLeptonic_widthx"+width])
        top_bkg_alt["top_bkg_Nomix"+width].Add(hist_wron_assig["ttbar_FullyLeptonic_widthx"+width])
        
        

    del hist_corr_assig
    del hist_wron_assig
 
    for mass in Alt_mass:
        hist_to_return.append(top_sig_alt["top_sig_"+mass]) 
        hist_to_return.append(top_bkg_alt["top_bkg_"+mass])
    del Alt_mass

    for width in Alt_width:
        hist_to_return.append(top_bkg_alt["top_bkg_Nomix"+width])

    del Alt_width
    del top_sig_alt
    del top_bkg_alt

    #################### Systematic samples  #################################################### 

    print "creating histogram for the systematic samples ............."
    print
    systs = ['TuneCP5CR2',  'TuneCP5CR1',   'hdampdown',    'hdampup', 'TuneCP5up',   'TuneCP5down',  'erdON' ]
   
    channels_sys_tch = []
    channels_sys_tbarch = []

    for syst in systs:
        channels_sys_tch.append("Tchannel_"+syst)
        channels_sys_tbarch.append("Tbarchannel_"+syst)

    Channels_systs = channels_sys_tch+channels_sys_tbarch      
    
    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}

    for channel in Channels_systs:
           Fpaths_DNN_apply[channel] = applydir+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
           EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1_sys/Minitree_"+channel+"_2J1T1_"+lep+".root"

    #print Fpaths_DNN_apply
    #print EvtWeight_Fpaths_Iso   
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,Channels_systs, MCcut , Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
    del Fpaths_DNN_apply
    del EvtWeight_Fpaths_Iso

    hist_corr_assig = {}
    hist_wron_assig = {}

    #MCSF = 1
    #QCDSF = 1
    for channel_no,channel in enumerate(Channels_systs):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Scale(MCSF)
        hist_wron_assig[channel].Scale(MCSF)

    del hists_corr
    del hists_wron

    top_sig_sys = {}
    top_bkg_sys = {}

    
    for syst in systs:
        top_sig_sys["top_sig_"+syst] = rt.TH1F('top_sig_'+syst, '', Num_bin, lest_bin, max_bin)
        top_bkg_sys["top_bkg_"+syst] = rt.TH1F('top_bkg_'+syst, '', Num_bin, lest_bin, max_bin)

        top_sig_sys["top_sig_"+syst].Add(hist_corr_assig["Tchannel_"+syst])
        top_sig_sys["top_sig_"+syst].Add(hist_corr_assig["Tbarchannel_"+syst])

        top_bkg_sys["top_bkg_"+syst].Add(hist_wron_assig["Tchannel_"+syst])
        top_bkg_sys["top_bkg_"+syst].Add(hist_wron_assig["Tbarchannel_"+syst])


    del hist_corr_assig
    del hist_wron_assig

   



    for syst in systs:
        hist_to_return.append(top_sig_sys["top_sig_"+syst])
        hist_to_return.append(top_bkg_sys["top_bkg_"+syst])
    del top_sig_sys
    del top_bkg_sys
    del systs


   #----------------- Add Altrenate mass and width samples ------------#"""

       

    return hist_to_return


if __name__ == "__main__":
    
    hists = Create_Workspace_input_file(lep,year,Variable) 
    output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+".root"
    outfile = rt.TFile(output_file,"recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir(lep+"jets")
    Dir_mu.cd()
    
    for hist in hists:
        hist.Write()
        
    rt.gROOT.cd()

    outfile.Close()
    print("File write into "+output_file+" and saved")
    
