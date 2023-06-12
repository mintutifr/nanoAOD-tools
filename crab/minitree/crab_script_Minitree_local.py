#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

import MinitreeModule as minitree
import cut_strings  as cs
import hdamp_ttbar_variation_module as hdamp
import btv_readfromJson as btv
import dummy_module as dummy
import jme as JME
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p', '--path', dest='path',  nargs='+',type=str, default='', help="Path to input file")
parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='', help="Dataset")
parser.add_argument('-t', '--tag', dest='tag', type=str, default='', help="year and mode tag")
parser.add_argument('-o', '--out', dest='out_dir', type=str, default='', help="output_dir")
args = parser.parse_args()
print('--------------------')
print(args)


region = args.tag.split('_')[0]
lep = args.tag.split('_')[1]
year = args.tag.split('_')[3]
dataset = args.dataset
inputFiles = args.path
#num = inputFiles[0].split('/')[-1].split('.')[0].split('_')[-1]

#Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
treecut = getattr(cs, 'cut_' + region + '_' + lep + '_' + year)
btvmodule = getattr(btv,'btagSF'+year)
minitreemodule = getattr(minitree,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year)
jmeCorrection = getattr(JME,'jmeCorrections'+year+'_MC_AK4CHS')
hdampmodule = getattr(hdamp,'hdamp_vari_mainModule')


if( ('ttbar_SemiLeptonic' == dataset) or ('ttbar_FullyLeptonic' == dataset)):
	runmodules = [btvmodule(),minitreemodule(),jmeCorrection(),hdampmodule()]
else:
	runmodules = [btvmodule(),minitreemodule(),jmeCorrection()]


print('treecut : ',treecut)
print('inputFiles : ',inputFiles)
#@print('file number : ',num)
print('modules imported : ','btagSF'+year,'MinitreeModuleConstr'+region+'_'+lep+'_mc_'+year,'jmeCorrections'+year+'_MC_AK4CHS','hdamp_vari_mainModule')
print('modules run : ',runmodules)

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

