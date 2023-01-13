import ROOT as rt
import numpy as np
import scipy.integrate as sp
import argparse as arg
import math

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

lep = args.lepton[0]
year= args.year[0]

if(lep=="mu"):
        lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)



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


#applydir = 'DNN_output_with_mtwCut/Apply_all/' ;  output_fileName = "ROC_TGraphs/Efficiency_info_"+year+"_"+lep+"_with_weights.root"
applydir = 'DNN_output_without_mtwCut/Apply_all/' ;  output_fileName = "ROC_TGraphs/Efficiency_Optimization_info_"+year+"_"+lep+"_with_weights.root"

channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
MCcut ="Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)"
Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"

Fpaths = {}
EvtWeight_Fpaths = {} 
for channel in channels:
        Fpaths[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
        if(year=="ULpreVFP2016"): 
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        elif(year=="ULpostVFP2016"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        elif(year=="UL2017"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        elif(year=="UL2018"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"

           
print(Fpaths)
print()
print(EvtWeight_Fpaths)

Variable="lntopMass"
Variable="TMath::Log(topMass)"
X_axies="ln(m_{Top})"
Y_axies="Events/(20)"
lest_bin=math.log(100.0)
max_bin=math.log(400.0)
Num_bin=15


hs = {}
hs_wrong_assignment = {}
infiles = {}
intree = {}
DNN_sig_bins =  np.array([0.0 , 0.05 , 0.1 , 0.15 , 0.2 , 0.25 , 0.3 ,  0.35 , 0.4 , 0.45 , 0.5 , 0.55 , 0.6 , 0.65 , 0.7 , 0.75 ,  0.8 , 0.85 , 0.90, 0.95])
#DNN_sig_bins =  np.array([0.0 , 0.5])
len_DNN_sig_bins = len(DNN_sig_bins)
n_sel_sig = np.zeros(len_DNN_sig_bins+1)
n_sel_bkg = np.zeros(len_DNN_sig_bins+1)

N_QCD = 0.0
N_NonQCD = 0.0

for channel in channels:
    print(channel)
    infiles[channel] = rt.TFile.Open(Fpaths[channel], 'READ')
    intree[channel] = infiles[channel].Get('Events')
    if(channel!="QCD"): 
        intree[channel].AddFriend ("Events",EvtWeight_Fpaths[channel])
    else: intree[channel].AddFriend ("Events",QCDAntiISO_Fpath)

    rt.gROOT.cd()

    hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
    hs_wrong_assignment[channel] = rt.TH1F('hs_wrong_assignment' + channel, '', Num_bin, lest_bin, max_bin)

DNNcut_sig = 0.0
for channel in channels:
        #print( channel," integral_bin ", int(hs[channel].GetNbinsX()))
        if(channel=='Tchannel' or channel=='Tbarchannel'):
                final_cut_corr_assg =  MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)*(t_ch_CAsi>="+str(DNNcut_sig)+")"
                final_cut_wrong_assg = MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)*(t_ch_CAsi>="+str(DNNcut_sig)+")"
                print(final_cut_corr_assg)
                print(final_cut_wrong_assg)
                intree[channel].Project('hs' + channel, Variable, final_cut_corr_assg)
                intree[channel].Project('hs_wrong_assignment' + channel, Variable, final_cut_wrong_assg)
                hs[channel].Print()
                hs_wrong_assignment[channel].Print()
        elif(channel!='QCD'):
                final_cut_bkg = MCcut+"*(t_ch_CAsi>="+str(DNNcut_sig)+")"
                intree[channel].Project('hs' + channel, Variable, final_cut_bkg)
                hs[channel].Print()
        else:
                final_cut_data = Datacut+"*(t_ch_CAsi>="+str(DNNcut_sig)+")"
                intree[channel].Project('hs' + channel, Variable, final_cut_data)
                hs[channel].Print()
                
        if(channel != "QCD"):
            N_NonQCD += round(hs[channel].Integral(1,Num_bin),4)
            N_NonQCD += round(hs_wrong_assignment[channel].Integral(1, Num_bin),4)
        else:
            hs[channel].Print()
            N_QCD += round(hs[channel].Integral(1, Num_bin),4)

print("QCD EVents = ",N_QCD," NonQCD Events = ",N_NonQCD)
MCSF=0.0 ; QCDSF=0.0;
MCSF=(NonQCDScale_mtwFit/N_NonQCD)
QCDSF=(QCDScale_mtwFit/N_QCD) 
print("QCDSF = ",QCDSF," MCSF = ",MCSF)

Totle_sig = 0
Totle_bkg = 0
for channel in channels:
        if(channel == "Tchannel" or channel == "Tbarchannel"):
            hs[channel].Scale(MCSF)
            Totle_sig += round(hs[channel].Integral(1, Num_bin),4)
            hs[channel].Reset()
            hs_wrong_assignment[channel].Scale(MCSF)
            Totle_bkg += round(hs_wrong_assignment[channel].Integral(1, Num_bin),4)
            hs_wrong_assignment[channel].Reset()
        elif(channel == "QCD"):
            hs[channel].Scale(QCDSF)
            Totle_bkg += round(hs[channel].Integral(1, Num_bin),4)
            hs[channel].Reset()
        else:
            hs[channel].Scale(MCSF)
            Totle_bkg += round(hs[channel].Integral(1, Num_bin),4)
            hs[channel].Reset()

print("Totle_sig = ",Totle_sig," Totle_bkg = ",Totle_bkg) 

      
SToB_ratio = np.zeros(len_DNN_sig_bins)

hs_opt_purity = rt.TH2F('hs_opt_purity', 'Purity;DNN corr. tch assign ; DNN corr. (ttbar+tch) assign ', len_DNN_sig_bins-1, DNN_sig_bins,len_DNN_sig_bins-1, DNN_sig_bins)
hs_opt_SE = rt.TH2F('hs_opt_SE', 'Signal Efficiency;DNN corr. tch assign; DNN corr. (ttbar+tch) assign', len_DNN_sig_bins-1, DNN_sig_bins,len_DNN_sig_bins-1, DNN_sig_bins)
hs_opt_BE = rt.TH2F('hs_opt_BE', 'Bkg Efficiency;DNN corr. tch assign; DNN corr. (ttbar+tch) assign', len_DNN_sig_bins-1, DNN_sig_bins,len_DNN_sig_bins-1, DNN_sig_bins)
hs_opt_SbB = rt.TH2F('hs_opt_SbB', 'Sig to Bkg ratio;DNN corr. tch assign; DNN corr. (ttbar+tch) assign', len_DNN_sig_bins-1, DNN_sig_bins,len_DNN_sig_bins-1, DNN_sig_bins)


for DNNcut_bin_ttbar_num,DNNcut_ttbar in enumerate(DNN_sig_bins):
        n_sel_sig = np.zeros(len_DNN_sig_bins+1)
        n_sel_bkg = np.zeros(len_DNN_sig_bins+1)
        Sig_effi = np.zeros(len_DNN_sig_bins)
        Bkg_effi = np.zeros(len_DNN_sig_bins)
        purity = np.zeros(len_DNN_sig_bins)
        SToB_ratio = np.zeros(len_DNN_sig_bins)


        DNNcut_ttbar_str = "*((t_ch_CAsi+ttbar_CAsi)>"+str(DNNcut_ttbar)+")"
        #DNNcut_ttbar_str = "*(ttbar_CAsi>"+str(DNNcut_ttbar)+")"
        for DNNcut_bin_num,DNNcut_sig in enumerate(DNN_sig_bins):
                print()
                print("-------------------------  ",  DNNcut_sig,DNNcut_ttbar  ,"  ----------------------------------")
                print()
                DNNcut_sig_str = "*(t_ch_CAsi>"+str(DNNcut_sig)+")"
                for channel in channels:
                        if(channel=='Tchannel' or channel=='Tbarchannel'):
                                final_cut_corr_assg =  MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)"+DNNcut_ttbar_str+DNNcut_sig_str
                                final_cut_wrong_assg = MCcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"+DNNcut_ttbar_str+DNNcut_sig_str
                                print(final_cut_corr_assg)
                                print(final_cut_wrong_assg)
                                intree[channel].Project('hs' + channel, Variable, final_cut_corr_assg)
                                intree[channel].Project('hs_wrong_assignment' + channel, Variable, final_cut_wrong_assg)
                                hs[channel].Print()
                                hs_wrong_assignment[channel].Print()
                        elif(channel!='QCD'):
                                final_cut_bkg = MCcut+DNNcut_ttbar_str+DNNcut_sig_str
                                intree[channel].Project('hs' + channel, Variable, final_cut_bkg)
                                hs[channel].Print()
                        else:
                                final_cut_data = Datacut+DNNcut_ttbar_str+DNNcut_sig_str
                                intree[channel].Project('hs' + channel, Variable, final_cut_data)
                                hs[channel].Print()
                        if(channel == "Tchannel" or channel == "Tbarchannel"):
                            hs[channel].Scale(MCSF)
                            n_sel_sig[DNNcut_bin_num] += round(hs[channel].Integral(1, Num_bin),4)
                            hs_wrong_assignment[channel].Scale(MCSF)
                            n_sel_bkg[DNNcut_bin_num] += round(hs_wrong_assignment[channel].Integral(1, Num_bin),4)
                        elif(channel == "QCD"):
                            hs[channel].Scale(QCDSF)
                            n_sel_bkg[DNNcut_bin_num] += round(hs[channel].Integral(1, Num_bin),4)
                        else:
                            hs[channel].Scale(MCSF)
                            n_sel_bkg[DNNcut_bin_num] += round(hs[channel].Integral(1, Num_bin),4)
                            
                
                    
                 #signal to background ratio
                if(n_sel_bkg[DNNcut_bin_num] == 0): SToB_ratio[DNNcut_bin_num] = 100.0
                else: SToB_ratio[DNNcut_bin_num] = round((n_sel_sig[DNNcut_bin_num]/n_sel_bkg[DNNcut_bin_num]),4)
                    
                #Purity calculation
                if((n_sel_sig[DNNcut_bin_num] + n_sel_bkg[DNNcut_bin_num]) == 0): purity[DNNcut_bin_num] = 10.0
                else: purity[DNNcut_bin_num] = round((n_sel_sig[DNNcut_bin_num]/(n_sel_sig[DNNcut_bin_num] + n_sel_bkg[DNNcut_bin_num])),4)
                    
                #signal efficiency calulation
                if(n_sel_sig[DNNcut_bin_num] == 0): Sig_effi[DNNcut_bin_num] = 0.00001 
                else: 
                    Sig_effi[DNNcut_bin_num] = round(n_sel_sig[DNNcut_bin_num]/Totle_sig,4)
                    if(Sig_effi[DNNcut_bin_num]==0): 
                         Sig_effi[DNNcut_bin_num] = 0.00001
                
                #Background efficiency calulation
                if(n_sel_bkg[DNNcut_bin_num] == 0): Bkg_effi[DNNcut_bin_num] =  0.00001
                else: 
                     Bkg_effi[DNNcut_bin_num] = round(n_sel_bkg[DNNcut_bin_num]/Totle_bkg,4)
                     if(Bkg_effi[DNNcut_bin_num]==0): 
                        Bkg_effi[DNNcut_bin_num] = 0.00001
                
                print("----> ",DNN_sig_bins[DNNcut_bin_num]," PU : ", purity[DNNcut_bin_num]*100, " SE : ",Sig_effi[DNNcut_bin_num]*100," BE : ",Bkg_effi[DNNcut_bin_num]*100, " S/B : ",SToB_ratio[DNNcut_bin_num])
                if(purity[DNNcut_bin_num]<=0.68 and purity[DNNcut_bin_num]>=0.50):
                    print("----> ",DNN_sig_bins[DNNcut_bin_num]," PU : ", purity[DNNcut_bin_num]*100, " SE : ",Sig_effi[DNNcut_bin_num]*100," BE : ",Bkg_effi[DNNcut_bin_num]*100, " S/B : ",SToB_ratio[DNNcut_bin_num])
                
        Sig_effi =  100.0*Sig_effi
        Bkg_effi =  100.0*Bkg_effi
        purity =   100.0*purity
        SToB_ratio = SToB_ratio
        
        for count_tch,tch_axies, in enumerate(DNN_sig_bins):
                tch_DNN_bin = hs_opt_purity.GetXaxis().FindBin(tch_axies)
                ttbar_tch_DNN_bin = hs_opt_purity.GetXaxis().FindBin(DNNcut_ttbar)
                hs_opt_purity.SetBinContent(tch_DNN_bin,ttbar_tch_DNN_bin,round(purity[count_tch],1))
                hs_opt_SE.SetBinContent(tch_DNN_bin,ttbar_tch_DNN_bin,round(Sig_effi[count_tch],1))
                hs_opt_BE.SetBinContent(tch_DNN_bin,ttbar_tch_DNN_bin,round(Bkg_effi[count_tch],1))
                hs_opt_SbB.SetBinContent(tch_DNN_bin,ttbar_tch_DNN_bin,round(SToB_ratio[count_tch],1))


        del n_sel_bkg 
        del n_sel_sig
        del SToB_ratio
        del purity
        del Sig_effi
        del Bkg_effi

outfile = rt.TFile(output_fileName, "recreate")
outfile.cd()
hs_opt_purity.Write("Purity")
hs_opt_SE.Write("Sig_Efficiency")
hs_opt_BE.Write("Bkg_Efficiency")
hs_opt_SbB.Write("Sig_by_Bkg_Ratio")


outfile.Close()
