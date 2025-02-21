import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys, os 
parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")
parser.add_argument('-DC', '--DNNCut  ', dest='DNNCut', type=str, nargs=1, help="if need to apply DNNCut [ >=0.0 ,>=0.7]")
args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>] -v <variable>"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018',"Run2"]:
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
DNNCut = args.DNNCut[0]

print("DNNcut = ",DNNCut)
gt_or_lt_tag = ''
if('>' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_gt'
if('<' in DNNCut):gt_or_lt_tag = gt_or_lt_tag+'_lt'


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
    
    #applydir = '/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/DNN_output_without_mtwCut/2J1T1/Apply_all/'
    applydir = '~/work/RUN2_UL/DNN_outputs_without_mtwCut_corr_bweight/'+yearDir[year]+'/2J1T1/Apply_all/'
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut"
    DNNcut_str = "*"+DNNCut 
    hist_to_return = [] 
    #################### Nimonal Samples MC ########################################################
 

    channels_Nomi = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']


    Fpaths_DNN_apply = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels_Nomi:
            Fpaths_DNN_apply[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            EvtWeight_Fpaths_Iso[channel] = "~/work/RUN2_UL/Minitree_corr_bweight_with_mtwMassFit_Scale/"+yearDir[year]+"/2J1T1/"+year+'_'+channel+'_Apply_all_'+lep+'.root'
    
      
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    print(type(QCDcut),"=======================")
    hists_corr,hists_wron =  get_histogram_with_DNN_cut(lep,year,Variable,channels_Nomi, MCcut ,QCDcut, Datacut , DNNCut ,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 
    del Data_AntiIso_Fpath

    hist_corr_assig = {}
    hist_wron_assig = {}

    for channel_no,channel in enumerate(channels_Nomi):
        hist_corr_assig[channel] = hists_corr[channel_no].Clone()
        hist_wron_assig[channel] = hists_wron[channel_no].Clone()
        hist_corr_assig[channel].Print()
        hist_wron_assig[channel].Print()
        print("===========================================")

    del hists_corr
    del hists_wron

    top_sig_cons = 16.0 
    top_bkg_cons = 6.0
    EWK_bkg_cons = 10.0 
    QCD_bkg_cons = 50.0 

    print("top_sig_cons = %s ; top_bkg_cons = %s ; EWK_bkg_cons = %s ; QCD_bkg_cons = %s" % (top_sig_cons, top_bkg_cons, EWK_bkg_cons, QCD_bkg_cons))
    top_sig_Nomi = hist_corr_assig["Tchannel"].Clone(); top_sig_Nomi.Add(hist_corr_assig["Tbarchannel"]);
    top_sig_Nomi.Print()
    top_sig_Nomi.SetLineColor(rt.kRed);top_sig_Nomi.SetLineWidth(2)
    top_sig_Nomi.GetXaxis().SetTitle(X_axies)
    top_sig_Nomi.SetName("top_sig_1725_corr"+tag+gt_or_lt_tag)
    propagate_rate_uncertainity(top_sig_Nomi, top_sig_cons)
    print("print after uncertinty propagation")
    top_sig_Nomi.Print()
    hist_to_return.append(top_sig_Nomi.Clone())


    missreco_single_top_bkg = hist_wron_assig["Tchannel"].Clone(); missreco_single_top_bkg.Add(hist_wron_assig["Tbarchannel"]);
    propagate_rate_uncertainity(missreco_single_top_bkg, top_sig_cons)
    missreco_single_top_bkg.SetName("top_sig_1725_wron"+tag+gt_or_lt_tag)
    hist_to_return.append(missreco_single_top_bkg.Clone())
    

    top_bkg_Nomi = hist_corr_assig['tw_top'].Clone(); missrecotop_bkg_Nomi = hist_wron_assig['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_Nomi.Add(hist_corr_assig[channel])
        missrecotop_bkg_Nomi.Add(hist_wron_assig[channel])
    missrecotop_bkg_Nomi.SetLineColor(rt.kOrange-1); missrecotop_bkg_Nomi.SetLineWidth(2)

    propagate_rate_uncertainity(top_bkg_Nomi, top_bkg_cons)
    propagate_rate_uncertainity(missrecotop_bkg_Nomi, top_bkg_cons)

    top_bkg_Nomi.SetName("top_bkg_1725_corr"+tag+gt_or_lt_tag)
    hist_to_return.append(top_bkg_Nomi.Clone())
    missrecotop_bkg_Nomi.SetName("top_bkg_1725_wron"+tag+gt_or_lt_tag)
    hist_to_return.append(missrecotop_bkg_Nomi.Clone())

    top_sig_total = top_sig_Nomi.Clone()
    top_sig_total.Add(top_bkg_Nomi.Clone()) 
    missrecotop_bkg_total = missrecotop_bkg_Nomi.Clone()
    missrecotop_bkg_total.Add(missreco_single_top_bkg.Clone())

    top_sig_total.SetName("top_sig_1725"+tag+gt_or_lt_tag)
    missrecotop_bkg_total.SetName("top_bkg_1725"+tag+gt_or_lt_tag)
    hist_to_return.append(top_sig_total.Clone())
    hist_to_return.append(missrecotop_bkg_total.Clone())
  
    cons = []    
    print("===================  "+year+"    ========================")
    cons.append("cons_top_sig            lnN     %.3f     -        - "%((1+(top_sig_cons/100))*(top_sig_Nomi.Integral()/top_sig_total.Integral())+(1+(top_bkg_cons/100))*(top_bkg_Nomi.Integral()/top_sig_total.Integral())))
    cons.append("cons_top_bkg            lnN     -        -        %.3f "%((1+(top_sig_cons/100))*(missreco_single_top_bkg.Integral()/missrecotop_bkg_total.Integral())+(1+(top_bkg_cons/100))*(missrecotop_bkg_Nomi.Integral()/missrecotop_bkg_total.Integral())))
    print(cons[0])
    print(cons[1])
    print("===========================================")

    return hist_to_return, cons


if __name__ == "__main__":
    
    years = []
    if(year != "Run2"):
        years.append(year)
    else:
        years=['UL2016preVFP', 'UL2016postVFP', 'UL2017', 'UL2018']
    output_file_name = "Redefined_cons_top_"+year+"_"+lep+".txt"
    output_file_txt = open(output_file_name, "w")

    for year in years:
        output_file_root = "Hist_Corrt_inccor_sig_topBKG/Hists_"+Variable+"_"+year+"_"+lep+"_gteq0p7_withoutDNNfit_rebin.root"
        print(output_file_root)
        hists,cons = Create_Workspace_input_file(lep,year,Variable) 
        outfile = rt.TFile(output_file_root,"recreate")
        outfile.cd()
        Dir_mu = outfile.mkdir(lep+"jets")
        Dir_mu.cd()
    
        for hist in hists:
            hist.Write()
        
        rt.gROOT.cd()

        outfile.Close()
        print("File write into "+output_file_root+" and saved")
        output_file_txt.write("\n===================  "+year+"    ========================")
        output_file_txt.write("\n"+cons[0])
        output_file_txt.write("\n"+cons[1])
        output_file_txt.write("\n===========================================")

    output_file_txt.close()
    print("File with cons into "+output_file_name+" and saved")
    
