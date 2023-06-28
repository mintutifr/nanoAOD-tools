#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

import MinitreeModule as minitree
import cut_strings  as cs
import hdamp_ttbar_variation_module as hdamp
import btv_readfromJson as btv
import gen_info_module as genInfo
import dummy_module as dummy
import jme as JME
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p', '--path', dest='path',  nargs='+',type=str, default='', help="Path to input file")
parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='', help="Dataset")
parser.add_argument('-t', '--tag', dest='tag', type=str, default='', help="year and mode tag")
parser.add_argument('-o', '--out', dest='out_dir', type=str, default='', help="output_dir")
parser.add_argument('-n', '--lognum', dest='lognum', type=str, default='', help="log txt file number")
parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")

args = parser.parse_args()
print('--------------------')
print(args)


region = args.tag.split('_')[0]
lep = args.tag.split('_')[1]
year = args.tag.split('_')[3]
dataset = args.dataset
inputFiles = args.path
#num = inputFiles[0].split('/')[-1].split('.')[0].split('_')[-1]
file_str=""
for File in inputFiles: file_str +=File+" "


if(args.ISDATA): print("\n python3 crab_script_Minitree_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -p "+ file_str +" -data  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
else: print("\n python3 crab_script_Minitree_local.py  -d "+dataset+" -t "+args.tag +" -o "+args.out_dir+ " -p "+ file_str + "  &> "+args.out_dir+"log/log_"+args.lognum+".txt\n")
if(year in ['UL2016_preVFP','UL2016_postVFP']):
	poststing = "_"+year.split("_")[-1] # required to define the module of jme correction for data
else:
	poststing = ""



#Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
treecut = getattr(cs, 'cut_' + region + '_' + lep + '_' + year)  # + " && Entry$<500"
btvmodule = getattr(btv,'btagSF'+year)
jmeCorrection = getattr(JME,'jmeCorrections'+year+'_MC_AK4CHS')
hdampmodule = getattr(hdamp,'hdamp_vari_mainModule')
geninfomodule =  getattr(genInfo,'gen_info_Module')

if(args.ISDATA):
	minitreemodule = getattr(minitree,'MinitreeModuleConstr'+region+'_'+lep+'_data_'+year)
	jmeCorrection = getattr(JME, "jmeCorrectionsUL"+dataset.split('_')[0]+poststing+"_DATA_AK4CHS")			

	Met_filter_UL16 = " && (Flag_goodVertices || Flag_globalSuperTightHalo2016Filter || Flag_HBHENoiseFilter || Flag_HBHENoiseIsoFilter || Flag_EcalDeadCellTriggerPrimitiveFilter || Flag_BadPFMuonFilter || Flag_BadPFMuonDzFilter || Flag_eeBadScFilter)==1"
	Met_filter_UL17_UL18 = " && (Flag_goodVertices || Flag_globalSuperTightHalo2016Filter || Flag_HBHENoiseFilter || Flag_HBHENoiseIsoFilter || Flag_EcalDeadCellTriggerPrimitiveFilter || Flag_BadPFMuonFilter || Flag_BadPFMuonDzFilter || Flag_eeBadScFilter || Flag_ecalBadCalibFilter)==1"
	if(year in ["UL2017", "UL2018"]): treecut = treecut+Met_filter_UL17_UL18	
	elif(year in ["UL2016_preVFP", "UL2016_postVFP"]): treecut = treecut+Met_filter_UL16
else:
	minitreemodule = getattr(minitree,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year)
	jmeCorrection = getattr(JME,'jmeCorrections'+year+'_MC_AK4CHS')

if( (dataset in ['ttbar_SemiLeptonic','ttbar_FullyLeptonic']) and region == "2J1T1"):
	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection(),hdampmodule(),geninfomodule()]
elif((dataset in ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel']) and region == "2J1T1"):
	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection(),geninfomodule()]
elif('Run' in dataset):
	 runmodules =[minitreemodule(),jmeCorrection()]
else:
	runmodules = [btvmodule(),minitreemodule(dataset),jmeCorrection()]


print('\n treecut : ',treecut)
print('\n inputFiles : ',inputFiles)
#@print('file number : ',num)
print('\n modules imported : ','btagSF'+year,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year,'MinitreeModuleConstr'+region+'_'+lep+'_data_'+year,'jmeCorrections'+year+'_MC_AK4CHS'," jmeCorrectionsUL"+dataset.split('_')[0]+poststing+"_DATA_AK4CHS",'hdamp_vari_mainModule')
print('\n modules run : ',runmodules)

print('--------------------')


p=PostProcessor(args.out_dir,
    	inputFiles,
		treecut,
		modules=runmodules,
		provenance=True,
		fwkJobReport=False,
		jsonInput=runsAndLumis())
p.run()
print("DONE")

