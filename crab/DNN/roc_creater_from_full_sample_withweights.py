import ROOT as rt
import numpy as np
import scipy.integrate as sp
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

lep = args.lepton[0]
year= args.year[0]

if(lep=="mu"):
        lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)

#applydir = 'DNN_output_without_mtwCut/2J1T1/Apply_all/' ; output_fileName = "ROC_TGraphs/ROC_info_"+year+"_"+lep+"_with_weights.root"

applydir = 'DNN_output/traing_and_application_file_check_depth8/2J1T1/Apply_all/' ; output_fileName = "ROC_TGraphs/ROC_info_"+year+"_"+lep+"_with_weights_check_depth8.root"

channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)" ## 
#MCcut ="(dR_bJet_lJet>0.4)*(mtwMass>50)" 
DNN_cut = ""#*((t_ch_CAsi+ttbar_CAsi)>0.5)"
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
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/RUN2_new_Files/SEVENTEEN/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/RUN2_new_Files/SEVENTEEN/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
        elif(year=="UL2018"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/RUN2_new_Files/EIGHTEEN/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/RUN2_new_Files/EIGHTEEN/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"

           
print(Fpaths)
print()
print (EvtWeight_Fpaths)

classes = ['sig', 'tbkg', 'obkg', 'sig_ws', 'tbkg_ws', 'qcd']
discriminators = {
	'sig': 't_ch_CAsi', 
	'sig_ws': 't_ch_WAsi', 
	'tbkg': 'ttbar_CAsi', 
	'tbkg_ws': 'ttbar_WAsi', 
	'obkg': 'EWK', 
	'qcd': 'QCD'}
hs = {}
hs_wrong_assignment = {}
infiles = {}
intree = {}
n_bins = 100
n_sel_sig = np.zeros(n_bins+1)
n_sel_bkg = np.zeros(n_bins+1)

for channel in channels:
    print(channel)
    infiles[channel] = rt.TFile.Open(Fpaths[channel], 'READ')
    intree[channel] = infiles[channel].Get('Events')
    if(channel!="QCD"): 
        intree[channel].AddFriend ("Events",EvtWeight_Fpaths[channel])
    else: intree[channel].AddFriend ("Events",QCDAntiISO_Fpath)

    rt.gROOT.cd()

    hs[channel] = rt.TH1F('hs' + channel, '', n_bins, 0.0, 1.0)
    hs_wrong_assignment[channel] = rt.TH1F('hs_wrong_assignment' + channel, '', n_bins, 0.0, 1.0)

    if(channel=='Tchannel' or channel=='Tbarchannel'):
        intree[channel].Project('hs' + channel, discriminators['sig'],MCcut+DNN_cut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)")
        intree[channel].Project('hs_wrong_assignment' + channel, discriminators['sig'],MCcut+DNN_cut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)")
        hs[channel].Print()
        hs_wrong_assignment[channel].Print()
    elif(channel!='QCD'):
        intree[channel].Project('hs' + channel, discriminators['sig'],MCcut+DNN_cut)
    else:
        intree[channel].Project('hs' + channel, discriminators['sig'],Datacut+DNN_cut)
    print( "DNN score hist bin ",int(hs[channel].GetNbinsX()))
    for j in range(n_bins):
        if(channel == "Tchannel" or channel == "Tbarchannel"):
            n_sel_sig[j] += round(hs[channel].Integral(j+1, n_bins),4)
            n_sel_bkg[j] += round(hs_wrong_assignment[channel].Integral(j+1, n_bins),4)
        else:
            n_sel_bkg[j] += round(hs[channel].Integral(j+1, n_bins),4)
            
DNN_values = np.arange(0, 1, 0.01) 
DNN_Score_plots = []
roc_int_limit_Sig_effi = False
roc_int_limit_Bkg_effi = False
Sig_effi = np.zeros(n_bins)
Bkg_effi = np.zeros(n_bins)

print("tottal integral of sig = ",n_sel_sig[0])
print("tottal integral of bkg = ",n_sel_bkg[0])


for count,DNN_score in enumerate(DNN_values):

    #signal efficiency calulation
    if(n_sel_sig[count] == 0): Sig_effi[count] = - 10.0 
    else: 
        Sig_effi[count] = round(n_sel_sig[count]/n_sel_sig[0],4)
        if(Sig_effi[count]==0): 
            Sig_effi[count] = - 10.0
            if(roc_int_limit_Sig_effi == False): roc_int_limit_Sig_effi = count

    #Background efficiency calulation
    if(n_sel_bkg[count] == 0): Bkg_effi[count] = - 10.0
    else: 
        Bkg_effi[count] = round(n_sel_bkg[count]/n_sel_bkg[0],4)
        if(Bkg_effi[count]==0): 
            Bkg_effi[count] = - 10.0
            if(roc_int_limit_Bkg_effi == False): roc_int_limit_Bkg_effi = count


Sig_effi =  100.0*Sig_effi
Bkg_effi =  100.0*Bkg_effi
                
roc = rt.TGraph(len(Sig_effi), Sig_effi, Bkg_effi)
roc.SetMaximum(100.0)
roc.SetMinimum(0.0)
roc.GetXaxis().SetLimits(0.0, 100.0)
roc.GetXaxis().SetTitle('Signal Efficiency')
roc.GetYaxis().SetTitle('Background Efficiency')
roc.SetLineWidth(4)

#print(roc.Integral())
print(roc_int_limit_Sig_effi," : ",roc_int_limit_Bkg_effi)
roc_integral_limit = (100-roc_int_limit_Sig_effi) if roc_int_limit_Sig_effi<roc_int_limit_Bkg_effi else (100-roc_int_limit_Bkg_effi)
rocInt = float(sp.simps(Bkg_effi[:-roc_integral_limit], Sig_effi[:-roc_integral_limit]))
print(rocInt)
rocIntG = rt.TGraph(1, np.array([1.0]),np.array([-1.0*rocInt/10000]))

outfile = rt.TFile(output_fileName, "recreate")
outfile.cd()
roc.Write("roc")
rocIntG.Write("rocInt")
outfile.Close()
