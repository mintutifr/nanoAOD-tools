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

files = {
	'sig': 		year+'_Top_signal_test_'+lep+'_apply.root',
	'tbkg': 	year+'_Top_bkg_test_'+lep+'_apply.root', 
	'obkg': 	year+'_EWK_BKG_test_'+lep+'_apply.root', 
	'sig_ws':	year+ '_WS_Top_signal_test_'+lep+'_apply.root', 
	'tbkg_ws':	year+ '_WS_Top_bkg_test_'+lep+'_apply.root', 
	'qcd': 		year+'_QCD_BKG_test_'+lep+'_apply.root'
	}
classes = ['sig', 'tbkg', 'obkg', 'sig_ws', 'tbkg_ws', 'qcd']
discriminators = {
	'sig': 't_ch_CAsi', 
	'sig_ws': 't_ch_WAsi', 
	'tbkg': 'ttbar_CAsi', 
	'tbkg_ws': 'ttbar_WAsi', 
	'obkg': 'EWK', 
	'qcd': 'QCD'}
hs = {}
signal = 'sig'
infiles = {}
intree = {}
n_bins = 100
n_sel_sig = np.zeros(n_bins+1)
n_sel_bkg = np.zeros(n_bins+1)


applydir = 'DNN_output_without_mtwCut/' ; output_fileName = "ROC_TGraphs/ROC_info_"+year+"_"+lep+"_without_weights.root"

for key in classes:
    infiles[key] = rt.TFile.Open(applydir +files[key], 'READ')
    intree[key] = infiles[key].Get('tree')
    rt.gROOT.cd()
    hs[key] = rt.TH1F('hs' + key, '', n_bins, 0.0, 1.0)
    intree[key].Project('hs' + key, discriminators[signal])
    print(int(hs[key].GetNbinsX()))
    for j in range(n_bins):
        if key == signal:
            n_sel_sig[j] += hs[key].Integral(j+1, n_bins)
        else:
            n_sel_bkg[j] += hs[key].Integral(j+1, n_bins)


x = 100.0*(n_sel_sig/n_sel_sig[0])
y = 100.0*(n_sel_bkg/n_sel_bkg[0])

roc_int_limit_Sig_effi = False
roc_int_limit_Bkg_effi = False

for count in range(len(x)):
    if(x[count]==0): 
           if(roc_int_limit_Sig_effi == False): roc_int_limit_Sig_effi = count
    if(y[count]==0): 
           if(roc_int_limit_Bkg_effi == False): roc_int_limit_Bkg_effi = count


roc = rt.TGraph(len(x), x, y)
roc.SetMaximum(100.0)
roc.SetMinimum(0.0)
roc.GetXaxis().SetLimits(0.0, 100.0)
roc.GetXaxis().SetTitle('Signal Efficiency')
roc.GetYaxis().SetTitle('Background Efficiency')
roc.SetLineWidth(4)

#print(roc.Integral())

print(roc_int_limit_Sig_effi," : ",roc_int_limit_Bkg_effi)
roc_integral_limit = (100-roc_int_limit_Sig_effi) if roc_int_limit_Sig_effi<roc_int_limit_Bkg_effi else (100-roc_int_limit_Bkg_effi)
roc_integral_limit = 9
print("roc integral range limit : ",roc_integral_limit)
if(roc_integral_limit==0):
    rocInt = float(sp.simps(y[:], x[:]))
else:
    rocInt = float(sp.simps(y[:-roc_integral_limit], x[:-roc_integral_limit]))
print(rocInt)
rocIntG = rt.TGraph(1, np.array([1.0]),np.array([-1.0*rocInt/10000]))


outfile = rt.TFile(output_fileName, "recreate")
outfile.cd()
roc.Write("roc")
rocIntG.Write("rocInt")
outfile.Close()
