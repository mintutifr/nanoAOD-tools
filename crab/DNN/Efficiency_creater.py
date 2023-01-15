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

applydir = 'DNN_output/Apply_all/'
channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
MCcut ="Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF"
Datacut = "(dR_bJet_lJet>0.4)"

Fpaths = {}
EvtWeight_Fpaths = {} 
for channel in channels:
        Fpaths[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
        if(year=="ULpreVFP2016"): 
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T0/Minitree_DataULpreVFP2016_2J1T0_"+lep+".root"
        elif(year=="ULpostVFP2016"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T0/Minitree_DataULpreVFP2016_2J1T0_"+lep+".root"
        elif(year=="UL2017"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T0/Minitree_DataULpreVFP2016_2J1T0_"+lep+".root"
        elif(year=="UL2018"):
            EvtWeight_Fpaths[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
            if(channel=="QCD"): QCDAntiISO_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T0/Minitree_DataULpreVFP2016_2J1T0_"+lep+".root"

           
print Fpaths
print
print EvtWeight_Fpaths

classes = ['sig', 'tbkg', 'obkg', 'sig_ws', 'tbkg_ws', 'qcd']
discriminators = {
	'sig': 't_ch_CAsi', 
	'sig_ws': 't_ch_WAsi', 
	'tbkg': 'ttbar_CAsi', 
	'tbkg_ws': 'ttbar_WAsi', 
	'obkg': 'EWK', 
	'qcd': 'QCD'}
hs = {}
infiles = {}
intree = {}
n_bins = 100
n_sel_sig = np.zeros(n_bins+1)
n_sel_bkg = np.zeros(n_bins+1)
purity = np.zeros(n_bins+1)

for channel in channels:
    infiles[channel] = rt.TFile.Open(Fpaths[channel], 'READ')
    intree[channel] = infiles[channel].Get('Events')
    if(channel!="QCD"): 
        intree[channel].AddFriend ("Events",EvtWeight_Fpaths[channel])
    else: intree[channel].AddFriend ("Events",QCDAntiISO_Fpath)

    rt.gROOT.cd()

    hs[channel] = rt.TH1F('hs' + channel, '', n_bins, 0.0, 1.0)
    if(channel!="QCD"): 
        intree[channel].Project('hs' + channel, discriminators['sig'],MCcut)
    else:
        intree[channel].Project('hs' + channel, discriminators['sig'],Datacut)
    print(int(hs[channel].GetNbinsX()))
    for j in range(n_bins):
        if(channel == "Tchannel" or channel == "Tbarchannel"):
            n_sel_sig[j] += hs[channel].Integral(j+1, n_bins)
        else:
            n_sel_bkg[j] += hs[channel].Integral(j+1, n_bins)
            
DNN_values = np.linspace(0.0, 1.0, num=100)
#Sig_effi = 100.0*(n_sel_sig/n_sel_sig[0])
#Bkg_effi = 100.0*(n_sel_bkg/n_sel_bkg[0])   
Sig_effi = np.zeros(n_bins+1)
Bkg_effi = np.zeros(n_bins+1)

for count in range(0,len(DNN_values)):
    if((n_sel_sig[count] + n_sel_bkg[count]) != 0): 
        purity[count] = (n_sel_sig[count]/(n_sel_sig[count] + n_sel_bkg[count]))
    else:purity[count] = -10.0
    
    if(n_sel_sig[count] == 0): Sig_effi[count] = - 10.0
    else: Sig_effi[count] = n_sel_sig[count]/n_sel_sig[0]

    if(n_sel_bkg[count] == 0): Bkg_effi[count] = - 10.0
    else: Bkg_effi[count] = n_sel_bkg[count]/n_sel_bkg[0]

Sig_effi =  100.0*Sig_effi
Bkg_effi =  100.0*Bkg_effi
purity =  100.0*purity

roc = rt.TGraph(len(Sig_effi), Sig_effi, Bkg_effi)
roc.SetMaximum(100.0)
roc.SetMinimum(0.0)
roc.GetXaxis().SetLimits(0.0, 100.0)
roc.GetXaxis().SetTitle('Signal Efficiency')
roc.GetYaxis().SetTitle('Background Efficiency')
roc.SetLineWidth(4)

sig_effi_gr = rt.TGraph(len(Sig_effi), DNN_values, Sig_effi)
sig_effi_gr.SetMaximum(100.0)
sig_effi_gr.SetMinimum(0.0)
sig_effi_gr.GetXaxis().SetLimits(0.0, 1.0)
sig_effi_gr.GetXaxis().SetTitle('DNN responce')
sig_effi_gr.GetYaxis().SetTitle('Signal Efficiency')
sig_effi_gr.SetLineWidth(4)

Bkg_effi_gr = rt.TGraph(len(Bkg_effi), DNN_values, Bkg_effi)
Bkg_effi_gr.SetMaximum(100.0)
Bkg_effi_gr.SetMinimum(0.0)
Bkg_effi_gr.GetXaxis().SetLimits(0.0, 1.0)
Bkg_effi_gr.GetXaxis().SetTitle('DNN responce')
Bkg_effi_gr.GetYaxis().SetTitle('Bkg Efficiency')
Bkg_effi_gr.SetLineWidth(4)

purity_gr = rt.TGraph(len(purity), DNN_values, purity)
purity_gr.SetMaximum(100.0)
purity_gr.SetMinimum(0.0)
purity_gr.GetXaxis().SetLimits(0.0, 1.0)
purity_gr.GetXaxis().SetTitle('DNN responce')
purity_gr.GetYaxis().SetTitle('Purity')
purity_gr.SetLineWidth(4) 

#print(roc.Integral())

rocInt = float(sp.simps(Bkg_effi[:-10], Sig_effi[:-10]))
print(rocInt)
rocIntG = rt.TGraph(1, np.array([1.0]),np.array([-1.0*rocInt/10000]))

outfile = rt.TFile("ROC_TGraphs/Efficiency_info_"+year+"_"+lep+".root", "recreate")
outfile.cd()
roc.Write("roc")
rocIntG.Write("rocInt")
sig_effi_gr.Write("sig_effi")
Bkg_effi_gr.Write("bkg_effi")
purity_gr.Write("Purity")
outfile.Close()
