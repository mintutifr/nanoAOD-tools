#source /cvmfs/cms.cern.ch/cmsset_default.sh
#source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
import sys, os
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc_Nomi , Mc_Alt , Mc_sys , Data ]")
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

if args.samples[0] not in ['Mc_Nomi', 'Mc_Alt', 'Mc_sys', 'Data']:
    print('Error: Incorrect choice of sample type, use -h for help')
    exit()


print(args)

lep = args.lepton[0]
year= args.year[0]
sample = args.samples[0]
if(lep=="mu"):
	lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)

import glob
import torch
import pandas as pd
import numpy as np
import ROOT as rt
import root_numpy
from IPython.display import display
from torch.utils.data import TensorDataset, DataLoader
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
import os


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        #self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(18, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 6),
            #nn.Softmax(dim=1),
        )



    def forward(self, x):
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


VARS = [lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E',
        'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        'Px_nu', 'Py_nu', 'Pz_nu',
        'FW1', 'bJetdeepJet', 'lJetdeepJet',
        ]
VARS_list = {lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E',
        'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        'Px_nu', 'Py_nu', 'Pz_nu',
        'FW1', 'bJetdeepJet', 'lJetdeepJet',
        }

data_channels = {
	"ULpreVFP2016" : "DataULpreVFP2016",
        "ULpostVFP2016" :  "DataULpostVFP2016",
        "UL2017" : "DataUL2017" 
	}
if(sample=="Mc_Nomi"):
        channels = ['Tchannel', 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel', 'ttbar_SemiLeptonic', 'ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
        channels.append("Data"+year) 
elif(sample=="Mc_Alt"):
        channels = ['Tbarchannel_mtop1695', 'ttbar_SemiLeptonic_mtop1695',   'ttbar_FullyLeptonic_mtop1695',   'Tbarchannel_mtop1735',   'ttbar_FullyLeptonic_widthx0p55',   'ttbar_FullyLeptonic_widthx0p7',   'ttbar_FullyLeptonic_mtop1735',   'Tbarchannel_mtop1715',   'ttbar_FullyLeptonic_widthx1p3',   'ttbar_FullyLeptonic_mtop1755',   'ttbar_FullyLeptonic_widthx1p45',   'ttbar_FullyLeptonic_mtop1715',   'Tchannel_mtop1715',   'ttbar_SemiLeptonic_mtop1755',   'ttbar_SemiLeptonic_mtop1735',   'ttbar_SemiLeptonic_mtop1715',   'ttbar_FullyLeptonic_widthx0p85',   'Tbarchannel_mtop1755',   'Tchannel_mtop1695',   'ttbar_FullyLeptonic_widthx1p15',   'Tchannel_mtop1735',   'Tchannel_mtop1755']
elif(sample=="Mc_sys"):
        channels =['Tchannel_TuneCP5CR2',  'Tchannel_TuneCP5CR1',   'Tchannel_hdampdown',   'Tbarchannel_hdampdown',  'Tchannel_TuneCP5down',   'Tbarchannel_hdampup',   'Tchannel_hdampup',   'Tbarchannel_TuneCP5down',   'Tchannel_erdON',   'Tchannel_TuneCP5up',   'Tbarchannel_TuneCP5up',  'Tbarchannel_erdON',   'Tbarchannel_TuneCP5CR1',   'Tbarchannel_TuneCP5CR2']

print(channels)
#channels.append(data_channels[year])

types = ['Apply_all']#,'train']
files = []

#ML_DIR='dataframe_saved_with_mtwCut/' ; wightfolder = 'weight_with_mtwCut/' ; MainOutputDir = 'DNN_output_with_mtwCut/'
ML_DIR='dataframe_saved_without_mtwCut/' ; wightfolder = 'weight_without_mtwCut/' ; MainOutputDir = 'DNN_output_without_mtwCut/'

if not os.path.exists(MainOutputDir): os.mkdir(MainOutputDir)
if not os.path.exists(MainOutputDir+'Apply_all/'): os.mkdir(MainOutputDir+'Apply_all/')
if not os.path.exists(MainOutputDir+'Apply_all/sys_N_Alt'): os.mkdir(MainOutputDir+'Apply_all/sys_N_Alt')

#if(sample=="Mc_Nomi"):
OriginalFileDir = {
        "ULpreVFP2016" : "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/"+ML_DIR,
        "ULpostVFP2016" :  "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/"+ML_DIR,
        "UL2017" : "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/"+ML_DIR,
        "UL2018" : ""
 }

for channel in channels:
    if(sample=="Mc_Nomi"):
        for typ in types:
            files.append(OriginalFileDir[year]+year+'_'+channel+'_Apply_all_'+lep+'.root')	
    elif(sample=="Mc_Alt" or sample=="Mc_sys"):
            files.append(OriginalFileDir[year]+"sys_N_Alt/"+year+'_'+channel+'_Apply_all_'+lep+'.root')

#files = ['/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/DNN/dataframe_saved_without_mtwCut/sys_N_Alt/UL2017_Tchannel_TuneCP5CR2_Apply_all_mu.root']
print(files)
m = nn.LogSoftmax(dim=1)
for fil in files:
	print(fil)
	#df_test = rt.RDataFrame("Events",fil).AsNumpy()
	df_test = rt.RDataFrame("Events",fil,VARS_list).AsNumpy()
	print(type(df_test))		
	#display(df_tr_top_signal_new)

	x_te = np.vstack([df_test[var] for var in VARS]).T
	print("shape of x for application" ,x_te.shape)

	y_te = np.vstack([0]*(x_te.shape[0]))
	y_te = np.vstack([y_te]).astype(int)
	print("shape of y for application", y_te.shape)

	tensor_x_te = torch.Tensor(x_te) # transform to torch tensor
	tensor_y_te = torch.Tensor(y_te)

	device = "cuda:1" if torch.cuda.is_available() else "cpu"
	print("Using {device} device")

	if torch.cuda.is_available():
		tensor_x_te = tensor_x_te.to(device)
		tensor_y_te = tensor_y_te.to(device)


	batch = 200
	test_dataset = TensorDataset(tensor_x_te,tensor_y_te) # create your datset
	testing_loader = DataLoader(test_dataset, batch_size = batch, shuffle = False) # create your dataloader

	model = NeuralNetwork().to(device)
	wightpath = wightfolder+year+'/'+lep
	list_of_files = glob.glob(wightpath+'/*')
	latest_weight_file = max(list_of_files, key=os.path.getctime)
	print("using ",latest_weight_file, "file for the evaluation")
	model.load_state_dict(torch.load(latest_weight_file))
	y_arr = np.zeros((x_te.shape[0], 6))

	for i, tdata in enumerate(testing_loader):
		#print(i)
		tinputs, tlabels = tdata
		toutput = model(tinputs)
		toutput1 = m(toutput)
		toutputs = torch.Tensor.cpu(toutput1)
		#print(np.shape(toutputs))
		if i < x_te.shape[0]//batch:
			y_arr[batch*i:batch*(i+1), :] = np.exp(toutputs.detach().numpy())
		else:
			y_arr[batch*i:, :] = np.exp(toutputs.detach().numpy())
	#print(y_arr[:10,:])
	#print(y_arr[-10:,:])
	#print(np.shape(y_arr))
	y_arr = y_arr.ravel().view(dtype = np.dtype([('t_ch_WAsi', np.double), ('t_ch_CAsi', np.double), ('ttbar_CAsi', np.double), ('ttbar_WAsi', np.double), ('EWK', np.double), ('QCD', np.double)]))
	fname, ext = os.path.splitext(fil)
	print("writing out put file : ", MainOutputDir+'Apply_all/sys_N_Alt/'+fname.rsplit('/')[-1],"_apply.root")

	if(sample == "Mc_Nomi"): root_numpy.array2root(y_arr, MainOutputDir+'Apply_all/'+ fname.rsplit('/')[-1] + '.root', treename='Events',mode='recreate')
	else: root_numpy.array2root(y_arr, MainOutputDir+'Apply_all/sys_N_Alt/'+ fname.rsplit('/')[-1] + '.root', treename='Events',mode='recreate')
