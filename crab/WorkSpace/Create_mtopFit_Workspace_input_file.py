import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys, os 
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ UL2016preVFP  UL2016postVFP  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
parser.add_argument('-f', '--fitdignostic_outFile ', dest='fitdignostic_outFile', type=str, default=[ None ],nargs=1, help="DNNFit dignostic output file which has histogram files i.e /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2017.root")
parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ >=0.0 ,>=0.7]")
parser.add_argument('-Alt', '--is_Alt_samp_add ', dest='is_Alt_samp_add',  action="store_true", help="Enable this feature if alternate mass and width variation from gen weights will be added")
parser.add_argument('-weight_sys', '--is_weight_sys ', dest='is_weight_sys_add',  action="store_true", help="Enable this feature if weights depent sys will be added like lepSF, Bweight,puWeightUp")
parser.add_argument('-samesys', '--is_same_sys_add ', dest='is_same_sys_add',  action="store_true", help="Enable this feature if sys samples from minitree weights will be added")
parser.add_argument('-colorRecinnect_sys', '--is_color_reconection_sys_add ', dest='is_color_reconection_sys_add',  action="store_true", help="Enable this feature if sys samples for color reconnection need to be added")
parser.add_argument('-JES_JER_sys', '--is_JES_JER_sys_add', dest='is_JES_JER_sys_add',  action="store_true", help="Enable this feature if sys samples for JES and JER")
parser.add_argument('-allsys', '--is_all_sys_add ', dest='is_all_sys_add',  action="store_true", help="Enable this feature if sys samples from minitree weights will be added")
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
isAltSample=args.is_Alt_samp_add
isSameSys = args.is_same_sys_add
allsys = args.is_all_sys_add
weightSys = args.is_weight_sys_add
colorReconect = args.is_color_reconection_sys_add
JES_JERSys = args.is_JES_JER_sys_add 

if(DNNFit_rescale_file!=None):
    if(os.path.isfile(DNNFit_rescale_file)): print("Reading the Normalization form the "+DNNFit_rescale_file)
    else:
        print(DNNFit_rescale_file, " does not exist")
        exit(0)

print("DNNcut = ",DNNCut)
gt_or_lt_tag = ''
if('>' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_gt'
if('<' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_lt'


from Histogram_discribtions import get_histogram_distciption 
from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow
from mlfitNormsToText import *
from create_Alt_sample import alt_hypotheis_sample

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinContent(i, int(hist.GetBinContent(i)))
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

def get_Weight_sys_top(lep,year,Variable,channels_weight_sys,MCcut,DNNCut,hist_sys_name,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_cons,top_bkg_cons,Original_minitrees="None"):
    QCDcut=""
    Datacut=""
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(lep,year,Variable,channels_weight_sys, MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,Original_minitrees)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"

    hist_corr_assig_weight_sys = {}
    hist_wron_assig_weight_sys = {}
    for channel_no,channel in enumerate(channels_weight_sys):
        hist_corr_assig_weight_sys[channel] = hists_corr_weight_sys[channel_no].Clone()
        hist_wron_assig_weight_sys[channel] = hists_wron_weight_sys[channel_no].Clone()
    del hists_corr_weight_sys
    del hists_wron_weight_sys

    top_sig_weight_sys = hist_corr_assig_weight_sys["Tchannel"].Clone(); top_sig_weight_sys.Add(hist_corr_assig_weight_sys["Tbarchannel"]);

    top_bkg_weight_sys = hist_wron_assig_weight_sys["Tchannel"].Clone(); top_bkg_weight_sys.Add(hist_wron_assig_weight_sys["Tbarchannel"]);


    top_bkg_weight_sys_corr = hist_corr_assig_weight_sys['tw_top'].Clone();
    top_bkg_weight_sys_wron = hist_wron_assig_weight_sys['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_weight_sys_corr.Add(hist_corr_assig_weight_sys[channel])
        top_bkg_weight_sys_wron.Add(hist_wron_assig_weight_sys[channel])

    top_sig_weight_sys.Add(top_bkg_weight_sys_corr)
    top_bkg_weight_sys.Add(top_bkg_weight_sys_wron)

    top_sig_weight_sys.Print()
    top_bkg_weight_sys.Print()

    return top_sig_weight_sys,top_bkg_weight_sys

def get_Weight_sys_EWK(lep,year,Variable,channels_weight_sys,MCcut,DNNCut,hist_sys_name,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,EWK_cons,Original_minitrees="None"):

    QCDcut=""
    Datacut=""
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(lep,year,Variable,channels_weight_sys, MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,Original_minitrees)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"


    hist_corr_assig_weight_sys = {}
    hist_wron_assig_weight_sys = {}
    for channel_no,channel in enumerate(channels_weight_sys):
        hist_corr_assig_weight_sys[channel] = hists_corr_weight_sys[channel_no].Clone()
        hist_wron_assig_weight_sys[channel] = hists_wron_weight_sys[channel_no].Clone()
    del hists_corr_weight_sys
    del hists_wron_weight_sys


    EWK_weight_sys = hist_corr_assig_weight_sys['WJetsToLNu_0J'].Clone()
    EWK_weight_sys.Add(hist_wron_assig_weight_sys['WJetsToLNu_0J'])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        EWK_weight_sys.Add(hist_corr_assig_weight_sys[channel])
        EWK_weight_sys.Add(hist_wron_assig_weight_sys[channel])


    EWK_weight_sys.Print()

    return EWK_weight_sys

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
    
    #applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    applydir = '/feynman/home/dphp/mk277705/work/RUN2_UL/DNN_outputs_without_mtwCut_corr_bweight/'+yearDir[year]+'/2J1T1/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
    DNNcut_str = "*"+DNNCut 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']
    channels_top_only = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']

    Fpaths_DNN_apply = {}
    File_with_mtwMassFit_weight_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            #File_with_mtwMassFit_weight_Iso[channel] = "/nfs/home/common/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            #if(channel=="QCD"): Data_AntiIso_Fpath =  "/nfs/home/common/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            File_with_mtwMassFit_weight_Iso[channel] = "/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
            if(channel=="QCD"): Data_AntiIso_Fpath =  "/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'

    #print File_with_mtwMassFit_weight_Iso

    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    # get histogram with DNN cut
    print(type(QCDcut),"=======================")
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi[:-1], MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Data_AntiIso_Fpath

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi[:-1]):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        if(channel in ['Tchannel' , 'Tbarchannel']):
            print("===========================================")
            hist_corr_assig[channel].Print()
            print("===========================================")

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
    top_sig_Nomi.Print()
    top_sig_Nomi.Scale(top_sig_DNNfitrescale) 
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_1725"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(top_sig_Nomi, top_sig_cons)
    print("print after uncertinty propagation")
    top_sig_Nomi.Print()

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

    missrecotop_bkg_Nomi.SetName("top_bkg_1725"+tag+gt_or_lt_tag)
    

    hist_EWK = hist_corr_assig["WJetsToLNu_0J"].Clone();hist_EWK.Add(hist_wron_assig["WJetsToLNu_0J"])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        hist_EWK.Add(hist_corr_assig[channel]); hist_EWK.Add(hist_wron_assig[channel])
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_EWK.Scale(EWK_bkg_DNNfitrescale)
    signal_region_EWK_Integral = hist_EWK.Integral()
    
    channels_EWK_only = ['WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']
    Control_EWK_hist = get_Weight_sys_EWK(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_EWK_only,MCcut = MCcut, DNNCut = "(t_ch_CAsi>=0.3) ", hist_sys_name="_"+lep,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,EWK_cons=EWK_bkg_cons)
    control_region_EWK_Integral = Control_EWK_hist.Integral()

    hist_EWK = Control_EWK_hist.Clone()
    hist_EWK.Scale(signal_region_EWK_Integral/control_region_EWK_Integral)

    hist_EWK.SetName("EWK_bkg"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(hist_EWK, EWK_bkg_cons)

    #for Bin in range(0,top_bkg_Nomi.GetNbinsX()+1):
    #                 print("Bin : %s, (%s,%s)"%(Bin,top_bkg_Nomi.GetBinContent(Bin),top_bkg_Nomi.GetBinError(Bin)))

    #################### Data and DD QCD  ######################################################## 
    print    
    print("Data and DDQCD with ", DNNcut_str, " .. .. .. .... ..... ...")
    print

    hs = {}
    infiles = {}
    intree = {}
    Fpaths_DNN_apply_data = {}
    rt.gStyle.SetOptStat(0)

    Data_AntiIso_Fpath = ""
    Data_Iso_Fpath = "" 
    for channel in ["QCD","Data"+year]:
           Fpaths_DNN_apply_data[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
    Data_AntiIso_Fpath =  "~/work/RUN2_UL/Minitree_with_mtw_weight/2J1T1/"+year+'_QCD_Apply_all_'+lep+'.root'
    Data_Iso_Fpath =  "~/work/RUN2_UL/Minitree_with_mtw_weight/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'

    #print Fpaths_DNN_apply

    for channel_no,channel in enumerate(["QCD","Data"+year]):
        if(channel=="QCD"):
                print(channel, " ", Data_AntiIso_Fpath)
                print(channel, " ", Fpaths_DNN_apply_data[channel])
                infiles[channel] = rt.TFile.Open(Data_AntiIso_Fpath, 'READ')
        else:
                print(channel, " ", Data_Iso_Fpath)
                print(channel, " ", Fpaths_DNN_apply_data[channel])
                infiles[channel] = rt.TFile.Open(Data_Iso_Fpath, 'READ')

        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",Fpaths_DNN_apply_data[channel])

        hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
        #rt.gROOT.cd()
        if(channel=="QCD"):
            print(type(QCDcut),type(DNNcut_str))
            intree[channel].Project('hs' + channel, Variable,QCDcut+DNNcut_str)
        else:
            intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut_str)
        #hs[channel] = DrawOverflow_N_DrawUnderflow(hs[channel])
        #hs[channel].Print()
    del Fpaths_DNN_apply_data   
    rt.gROOT.cd()
    Data = hs['Data'+year].Clone()
    DDQCD = hs['QCD'].Clone()
    #DDQCD.Scale(QCDSF)
    DDQCD.SetName("QCD_DD"+tag+gt_or_lt_tag)
    DDQCD.Scale(QCD_bkg_DNNfitrescale)
    propagate_rate_uncertainity(DDQCD, QCD_bkg_cons)
    #for i in range(1,DDQCD.GetNbinsX()+1):
    #    print "--------------------"
    #    print "QCD DDD : ",DDQCD.GetBinContent(i), DDQCD.GetBinError(i)
    DDQCD.Print()

    DDQCD_subs_data = Data.Clone()
    DDQCD_subs_data.Add(DDQCD,-1)

    DDQCD_subs_data.SetName("data_obs")
    print('True QCD substracted data ---- >')
    DDQCD_subs_data.Print()

    Total_MC_for_fit = top_sig_Nomi.Clone()
    Total_MC_for_fit.Add(missrecotop_bkg_Nomi)
    Total_MC_for_fit.Add(hist_EWK)
    Total_MC_for_fit.SetLineColor(rt.kBlack)
    Total_MC_for_fit.SetName("data_obs")
    print("MC saved as data ---- >")
    Total_MC_for_fit.Print()

    DDQCD.SetLineColor(rt.kGray); DDQCD.SetLineWidth(2)
    
    del hs
    del Data_Iso_Fpath,Data_AntiIso_Fpath 



    #----------------- Add Nomi histograms ------------------ #
    hist_to_return.append(top_sig_Nomi)
    hist_to_return.append(missrecotop_bkg_Nomi)
    hist_to_return.append(hist_EWK)
    hist_to_return.append(DDQCD)
    #hist_to_return.append(DDQCD_subs_data) #since analysis is blind
    hist_to_return.append(Total_MC_for_fit)

    #################### ALternate mass and width  #################################################### 
    #top_sig_DNNfitrescale=1 ; top_bkg_DNNfitrescale = 1
    if(isAltSample):
        print("creating histogram for the Alt mass and with samples .............")
        print()
        Alt_mass_weights = ["Mtop1695", "Mtop1705", "Mtop1710","Mtop1715", "Mtop1735", "Mtop1745","Mtop1755"]
        Alt_width_weights = ["Wtop190", "Wtop170", "Wtop150","Wtop130", "Wtop110","Wtop090","Wtop075"]

        channels_alt = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']


        weight_file = {}
        for Channel_alt in channels_alt:
            #weight_file[Channel_alt] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/NanoGen/GenWeight/GenWeight_"+Channel_alt+"_"+lep+"_"+year+".root"
            weight_file[Channel_alt] = "/feynman/home/dphp/mk277705/work/HiggsCombine/CMSSW_12_3_4/src/Run2UL_Analysis/NanoGen/GenWeight/GenWeight_"+Channel_alt+"_"+lep+"_"+year+"_new.root"

        for weight in Alt_mass_weights:
            print("\n #################  ", weight, "############## \n")
            hist_mass = alt_hypotheis_sample(lepton,Variable,MCcut,DNNcut_str,weight,weight_file,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons)
            hist_mass.SetName("top_sig_"+weight.split("top")[1]+tag+gt_or_lt_tag)
            hist_mass.Print()
            hist_to_return.append(hist_mass)
            
            
        for weight in Alt_width_weights:
            print("\n #################  ", weight, "############## \n")
            hist_width = alt_hypotheis_sample(lepton,Variable,MCcut,DNNcut_str,weight,weight_file,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons)
            hist_width.Print()
            hist_width.SetName("top_sig_"+weight.split("top")[1]+tag+gt_or_lt_tag)
            hist_to_return.append(hist_width)
        del weight_file
        #del File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,weight_file
    
    #################### Systematic saved as weight in same minitree ############################# 
    if(isSameSys or allsys):
        #File_with_mtwMassFit_weight_Iso = None
        #Fpaths_DNN_apply = None
        print("creating histogram for the sys samples from same minitree .............")
        print()
        Alt_same_sys = ["PSWeight[0]", "PSWeight[2]", "PSWeight[1]", "PSWeight[3]"]
        Alt_same_sys_Name = ["PSWeight_ISR_Up", "PSWeight_ISR_Down", "PSWeight_FSR_Up", "PSWeight_FSR_Down"]

        channels_same_sys = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
         
        
        QCDcut_same_sys = "" # since not been used in this case
        Datacut_same_sys = ""  # since not been used in this case

        hist_corr_assig_same_sys = {}
        hist_wron_assig_same_sys = {}
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        for sys,sys_name in zip(Alt_same_sys,Alt_same_sys_Name):
            print("\n #################  ", sys, "############## \n")
            MCcut_same_sys =  MCcut+ "*"+ sys
            hists_corr_same_sys,hists_wron_same_sys =  get_histogram_with_DNN_cut(lep,year,Variable,channels_same_sys, MCcut_same_sys ,QCDcut_same_sys, Datacut_same_sys, DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)


            for channel_no,channel in enumerate(channels_same_sys):
                print(channel, " same sys")
                hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
                hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
                #hist_corr_assig_same_sys[sys][channel].Print()
                #hist_wron_assig_same_sys[sys][channel].Print()
        
            del hists_corr_same_sys
            del hists_wron_same_sys
        
            top_sig_same_sys = hist_corr_assig_same_sys["Tchannel"].Clone()
            top_sig_same_sys.Add(hist_corr_assig["Tbarchannel"]);
            top_sig_same_sys.Print()
            top_sig_same_sys.Scale(top_sig_DNNfitrescale) 
            top_sig_same_sys.SetLineColor(rt.kRed);top_sig_same_sys.SetLineWidth(2)
            top_sig_same_sys.GetXaxis().SetTitle(X_axies)
            top_sig_same_sys.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys)
            propagate_rate_uncertainity(top_sig_same_sys, top_sig_cons)
            print("print after uncertinty propagation")
            top_sig_same_sys.Print()
            hist_to_return.append(top_sig_same_sys)
        
            missreco_single_top_bkg_same_sys = hist_wron_assig_same_sys["Tchannel"].Clone()
            missreco_single_top_bkg_same_sys.Add(hist_wron_assig_same_sys["Tbarchannel"]);
            missreco_single_top_bkg_same_sys.Scale(top_sig_DNNfitrescale)
            propagate_rate_uncertainity(missreco_single_top_bkg_same_sys, top_sig_cons)

    

            top_bkg_same_sys = hist_corr_assig_same_sys['tw_top'].Clone()
            missrecotop_bkg_same_sys = hist_wron_assig_same_sys['tw_top'].Clone();
            for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
                top_bkg_same_sys.Add(hist_corr_assig_same_sys[channel])
                missrecotop_bkg_same_sys.Add(hist_wron_assig_same_sys[channel])

            missrecotop_bkg_same_sys.SetLineColor(rt.kOrange-1); missrecotop_bkg_same_sys.SetLineWidth(2)

            top_bkg_same_sys.Scale(top_bkg_DNNfitrescale)
            propagate_rate_uncertainity(top_bkg_same_sys, top_bkg_cons)

            missrecotop_bkg_same_sys.Scale(top_bkg_DNNfitrescale)
            propagate_rate_uncertainity(missrecotop_bkg_same_sys, top_bkg_cons)

            top_sig_same_sys.Add(top_bkg_same_sys)    
            missrecotop_bkg_same_sys.Add(missreco_single_top_bkg_same_sys)

            missrecotop_bkg_same_sys.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys) 

            hist_to_return.append(missrecotop_bkg_same_sys)
    
        del hist_corr_assig_same_sys
        del hist_wron_assig_same_sys

        
        
        
        
        
        print("creating histogram for the ==hdamp== sys samples from same minitree .............")
        print()

        Alt_same_sys = ["hdamp_Up", "hdamp_Down"]

        channels = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel',]
        channels_hdamp_sys = ['ttbar_SemiLeptonic','ttbar_FullyLeptonic'] 
        
        QCDcut_same_sys = "" # since not been used in this case
        Datacut_same_sys = ""  # since not been used in this case

        hist_corr_assig_same_sys = {}
        hist_wron_assig_same_sys = {}
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        for sys in Alt_same_sys:
            print("\n #################  ", sys, "############## \n")
            MCcut_same_sys = MCcut+ "*"+ sys
            hists_corr_same_sys,hists_wron_same_sys =  get_histogram_with_DNN_cut(lep,year,Variable,channels_hdamp_sys, MCcut_same_sys ,QCDcut_same_sys, Datacut_same_sys, DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)


            for channel_no,channel in enumerate(channels_hdamp_sys):
                print(channel, " same sys")
                hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
                hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
                #hist_corr_assig_same_sys[sys][channel].Print()
                #hist_wron_assig_same_sys[sys][channel].Print()
        
            del hists_corr_same_sys
            del hists_wron_same_sys
            
            hists_corr_same_sys,hists_wron_same_sys =  get_histogram_with_DNN_cut(lep,year,Variable,channels, MCcut ,QCDcut_same_sys, Datacut_same_sys, DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)


            for channel_no,channel in enumerate(channels):
                print(channel, " same sys")
                hist_corr_assig_same_sys[channel] = hists_corr_same_sys[channel_no].Clone()
                hist_wron_assig_same_sys[channel] = hists_wron_same_sys[channel_no].Clone()
                #hist_corr_assig_same_sys[sys][channel].Print()
                #hist_wron_assig_same_sys[sys][channel].Print()
        
            del hists_corr_same_sys
            del hists_wron_same_sys
            
        
            top_sig_same_sys = hist_corr_assig_same_sys["Tchannel"].Clone()
            top_sig_same_sys.Add(hist_corr_assig["Tbarchannel"]);
            top_sig_same_sys.Print()
            top_sig_same_sys.Scale(top_sig_DNNfitrescale) 
            top_sig_same_sys.SetLineColor(rt.kRed);top_sig_same_sys.SetLineWidth(2)
            top_sig_same_sys.GetXaxis().SetTitle(X_axies)
            top_sig_same_sys.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys)
            propagate_rate_uncertainity(top_sig_same_sys, top_sig_cons)
            print("print after uncertinty propagation")
            top_sig_same_sys.Print()
            hist_to_return.append(top_sig_same_sys)
        
            missreco_single_top_bkg_same_sys = hist_wron_assig_same_sys["Tchannel"].Clone()
            missreco_single_top_bkg_same_sys.Add(hist_wron_assig_same_sys["Tbarchannel"]);
            missreco_single_top_bkg_same_sys.Scale(top_sig_DNNfitrescale)
            propagate_rate_uncertainity(missreco_single_top_bkg_same_sys, top_sig_cons)

    

            top_bkg_same_sys = hist_corr_assig_same_sys['tw_top'].Clone()
            missrecotop_bkg_same_sys = hist_wron_assig_same_sys['tw_top'].Clone();
            for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
                top_bkg_same_sys.Add(hist_corr_assig_same_sys[channel])
                missrecotop_bkg_same_sys.Add(hist_wron_assig_same_sys[channel])

            missrecotop_bkg_same_sys.SetLineColor(rt.kOrange-1); missrecotop_bkg_same_sys.SetLineWidth(2)

            top_bkg_same_sys.Scale(top_bkg_DNNfitrescale)
            propagate_rate_uncertainity(top_bkg_same_sys, top_bkg_cons)

            missrecotop_bkg_same_sys.Scale(top_bkg_DNNfitrescale)
            propagate_rate_uncertainity(missrecotop_bkg_same_sys, top_bkg_cons)

            top_sig_same_sys.Add(top_bkg_same_sys)    
            missrecotop_bkg_same_sys.Add(missreco_single_top_bkg_same_sys)

            missrecotop_bkg_same_sys.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys)

            hist_to_return.append(missrecotop_bkg_same_sys)
    
        del hist_corr_assig_same_sys
        del hist_wron_assig_same_sys

    #################### Systematic samples  #################################################### 
    if(allsys or weightSys):
        print()
        print("  ================    weight sys   ==============")
        print()
        sys_lep_SF = {"el":["SF_Iso_IDUp" "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown","SF_Veto_IDUp", "SF_Veto_IDDown", "SF_Veto_TrigUp", "SF_Veto_TrigDown"],
                      "mu":["SF_IsoUp", "SF_IsoDown", "SF_Iso_IDUp", "SF_Iso_IDDown", "SF_Iso_TrigUp", "SF_Iso_TrigDown"]
        }
        for sys in sys_lep_SF[lep]:
            print("\n #################  ", sys, "############## \n")
            MCcut_sys_lep_SF = "Xsec_wgt*LHEWeightSign*puWeight*"+lepton+"_"+sys+"*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
            topSig_hists_syst,topBkg_hists_syst = get_Weight_sys_top(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_top_only,MCcut = MCcut_sys_lep_SF,DNNCut = DNNCut,hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,top_sig_cons=top_sig_cons,top_bkg_cons=top_bkg_cons)
            topSig_hists_syst.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys)
            topBkg_hists_syst.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys)
            hist_to_return.append(topSig_hists_syst.Clone())
            hist_to_return.append(topBkg_hists_syst.Clone())
            del topSig_hists_syst,topBkg_hists_syst
            EWK_hists_syst = get_Weight_sys_EWK(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_EWK_only,MCcut = MCcut_sys_lep_SF,DNNCut = DNNCut, hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,EWK_cons=EWK_bkg_cons)
            sys_EWK_Integral = EWK_hists_syst.Integral()
            EWK_hists_syst = Control_EWK_hist.Clone()
            EWK_hists_syst.Scale(sys_EWK_Integral/control_region_EWK_Integral)
            EWK_hists_syst.SetName("EWK_bkg"+tag+gt_or_lt_tag+sys)
            hist_to_return.append(EWK_hists_syst.Clone())
            del EWK_hists_syst
        del sys_lep_SF
        #####   puileup  ######

        sys_pileup = ["puWeightUp","puWeightDown"]
        sys_variation = ["Up","Down"]
        for variation_no,sys in enumerate(sys_pileup):
            print("\n #################  ", sys, "############## \n")
            MCcut_sys_pileup = "Xsec_wgt*LHEWeightSign*"+sys+"*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
            topSig_hists_syst,topBkg_hists_syst = get_Weight_sys_top(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_top_only,MCcut = MCcut_sys_pileup,DNNCut = DNNCut,hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,top_sig_cons=top_sig_cons,top_bkg_cons=top_bkg_cons)
            topSig_hists_syst.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys)
            topBkg_hists_syst.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys)
            hist_to_return.append(topSig_hists_syst.Clone())
            hist_to_return.append(topBkg_hists_syst.Clone())
            del topSig_hists_syst,topBkg_hists_syst
            EWK_hists_syst = get_Weight_sys_EWK(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_EWK_only,MCcut = MCcut_sys_pileup,DNNCut = DNNCut, hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,EWK_cons=EWK_bkg_cons)
            sys_EWK_Integral = EWK_hists_syst.Integral()
            EWK_hists_syst = Control_EWK_hist.Clone()
            EWK_hists_syst.Scale(sys_EWK_Integral/control_region_EWK_Integral)
            EWK_hists_syst.SetName("EWK_bkg"+tag+gt_or_lt_tag+sys)
            hist_to_return.append(EWK_hists_syst.Clone())
            del EWK_hists_syst
        del sys_pileup,sys_variation

        sys_bWeight = ["bWeight_lf","bWeight_hf" , "bWeight_cferr1", "bWeight_cferr2", "bWeight_lfstats1", "bWeight_lfstats2", "bWeight_hfstats1", "bWeight_hfstats2", "bWeight_jes"]
        sys_variation = ["Up","Down"]
        for sys in sys_bWeight:
            for variation_no,variation in enumerate(sys_variation):
                print("\n #################  ", sys+variation, "############## \n")
                MCcut_sys_bWeight = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*"+sys+variation+"*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
                topSig_hists_syst,topBkg_hists_syst = get_Weight_sys_top(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_top_only,MCcut = MCcut_sys_bWeight,DNNCut = DNNCut,hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,top_sig_cons=top_sig_cons,top_bkg_cons=top_bkg_cons)
                topSig_hists_syst.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys+variation)
                topBkg_hists_syst.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys+variation)
                hist_to_return.append(topSig_hists_syst.Clone())
                hist_to_return.append(topBkg_hists_syst.Clone())
                del topSig_hists_syst,topBkg_hists_syst
                EWK_hists_syst = get_Weight_sys_EWK(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_EWK_only,MCcut = MCcut_sys_bWeight,DNNCut = DNNCut, hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,EWK_cons=EWK_bkg_cons)
                sys_EWK_Integral = EWK_hists_syst.Integral()
                EWK_hists_syst = Control_EWK_hist.Clone()
                EWK_hists_syst.Scale(sys_EWK_Integral/control_region_EWK_Integral)
                EWK_hists_syst.SetName("EWK_bkg"+tag+gt_or_lt_tag+sys)
                hist_to_return.append(EWK_hists_syst.Clone())
                del EWK_hists_syst
        del sys_bWeight,sys_variation
    if(allsys or JES_JERSys):
        sys_JES = ["jesAbsoluteStat"]
        sys_variation = ["Up","Down"]
        channel_JES = ["Tchannel"]
        Fpaths_sys_samples = {}
        for channel in channel_JES:
            Fpaths_sys_samples[channel] = "/feynman/home/dphp/mk277705/work/RUN2_UL/Minitree_corr_bweight/JER_JES_Trees/JERJEStree_"+year+"_"+channel+"_2J1T1_"+lep+".root"
            
        for sys in sys_JES:
            for variation_no,variation in enumerate(sys_variation):
                print("\n #################  ", sys+variation, "############## \n")
                print(f"{MCcut = }")
                if(Variable=="TMath::Log(topMass)"): Variable="lntopMass_"+sys+variation
                hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channel_JES, MCcut ,QCDcut, Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,Fpaths_sys_samples = Fpaths_sys_samples)
                if("lntopMass_" in Variable): Variable="TMath::Log(topMass)"

                #topSig_hists_syst,topBkg_hists_syst = get_histogram_with_DNN_cut(lep=lep,year=year,Variable=Variable,channels_weight_sys=channel_JES,MCcut = MCcut,DNNCut = DNNCut,hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,top_sig_cons=top_sig_cons,top_bkg_cons=top_bkg_cons)
                # topSig_hists_syst.SetName("top_sig_1725"+tag+gt_or_lt_tag+sys+variation)
                # topBkg_hists_syst.SetName("top_bkg_1725"+tag+gt_or_lt_tag+sys+variation)
                # hist_to_return.append(topSig_hists_syst.Clone())
                # hist_to_return.append(topBkg_hists_syst.Clone())
                # del topSig_hists_syst,topBkg_hists_syst
                # EWK_hists_syst = get_Weight_sys_EWK(lep=lep,year=year,Variable=Variable,channels_weight_sys=channels_EWK_only,MCcut = MCcut_sys_bWeight,DNNCut = DNNCut, hist_sys_name="_"+lep+sys,File_with_mtwMassFit_weight_Iso=File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply=Fpaths_DNN_apply,EWK_cons=EWK_bkg_cons)
                # sys_EWK_Integral = EWK_hists_syst.Integral()
                # EWK_hists_syst = Control_EWK_hist.Clone()
                # EWK_hists_syst.Scale(sys_EWK_Integral/control_region_EWK_Integral)
                # EWK_hists_syst.SetName("EWK_bkg"+tag+gt_or_lt_tag+sys)
                # hist_to_return.append(EWK_hists_syst.Clone())
                # del EWK_hists_syst
        del sys_JES,sys_variation

    if(allsys or colorReconect):
        print()
        print("creating histogram for the color reconnection systematic samples .............")
        print()

        systs = ['TuneCP5CR2',  'TuneCP5CR1', 'TuneCP5up',   'TuneCP5down',  'erdON' ]
   
        channels_sys_tch = []
        channels_sys_tbarch = []

        for syst in systs:
            channels_sys_tch.append("Tchannel_"+syst)
            channels_sys_tbarch.append("Tbarchannel_"+syst)

        Channels_systs = channels_sys_tch+channels_sys_tbarch
        print(f"{MCcut = }")
















        """Fpaths_DNN_apply = {}
        File_with_mtwMassFit_weight_Iso = {}

        for channel in Channels_systs:
               Fpaths_DNN_apply[channel] = applydir+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
               File_with_mtwMassFit_weight_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/"+yearDir[year]+"/minitree/Mc/2J1T1_sys/Minitree_"+channel+"_2J1T1_"+lep+".root"

        #print Fpaths_DNN_apply
        #print File_with_mtwMassFit_weight_Iso   
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        # get histogram with DNN cut
        hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,Channels_systs, MCcut , Datacut , DNNCut ,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply)
        if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
        del Fpaths_DNN_apply
        del File_with_mtwMassFit_weight_Iso

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
        del systs"""

       
    print("total number of histogram shaved :", len(hist_to_return))
    return hist_to_return


if __name__ == "__main__":
    
    
    if(">=0.7" in DNNCut and DNNFit_rescale_file!=None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p7_withDNNfit_rebin.root"
    elif("<0.7" in DNNCut and "0.5" in DNNCut and DNNFit_rescale_file!=None): 
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p5_withDNNfit_rebin.root"
    elif(">=0.3" in DNNCut and "<0.7" in DNNCut and DNNFit_rescale_file!=None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p3_withDNNfit_rebin.root"
    elif(">=0.3" in DNNCut and DNNFit_rescale_file!=None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p3_withDNNfit_rebin.root"        
    elif(">=0.7" in DNNCut and DNNFit_rescale_file==None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p7_withoutDNNfit_rebin.root"
    elif("<0.7" in DNNCut and "0.5" in DNNCut and DNNFit_rescale_file==None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p5_withoutDNNfit_rebin.root"
    elif(">=0.3" in DNNCut and "<0.7" in DNNCut and DNNFit_rescale_file==None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_lt0p7gteq0p3_withoutDNNfit_rebin.root"
    elif(">=0.3" in DNNCut and DNNFit_rescale_file==None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p3_withoutDNNfit_rebin.root"
    elif(">=0.1" in DNNCut and DNNFit_rescale_file==None):
            output_file = "Hist_for_workspace/Combine_Input_"+Variable+"_histograms_"+year+"_"+lep+"_gteq0p1_withoutDNNfit_rebin.root"
    else:
        print("something wrong with DNNcut")
        exit(0)
    print(output_file)
    hists = Create_Workspace_input_file(lep,year,Variable) 
    outfile = rt.TFile(output_file,"recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir(lep+"jets")
    Dir_mu.cd()
    
    for hist in hists:
        hist.Write()
        
    rt.gROOT.cd()

    outfile.Close()
    print("File write into "+output_file+" and saved")
    
