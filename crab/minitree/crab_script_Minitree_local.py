#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from MinitreeModule import *
import cut_strings  as cs
from hdamp_ttbar_variation_module import *
from btv_readfromJson import *
from dummy_module import *
from jme import *
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p', '--path', dest='path', type=str, default='', help="Path to input file")
parser.add_argument('-d', '--dataset', dest='dataset', type=str, default='', help="Dataset")
parser.add_argument('-t', '--tag', dest='tag', type=str, default='', help="year and mode tag")
parser.add_argument('-o', '--out', dest='out_dir', type=str, default='', help="output_dir")
args = parser.parse_args()
print('--------------------')
print(args)

#Minitree_module = getattr(mt , 'MinitreeModuleConstr' + args.tag)
treecut_tag = args.tag.split('_')[0] + '_' + args.tag.split('_')[1] + '_' + args.tag.split('_')[3]
treecut = getattr(cs, 'cut_' + treecut_tag)
year = args.tag.split('_')[3]
print('treecut : ',treecut)
inputFiles = [args.path]
print('inputFiles : ',inputFiles)
dataset = args.dataset
#for inputFil in inputFiles:
num = inputFiles[0].split('/')[-1].split('.')[0].split('_')[-1]
print(num)
#inputFile = [inputFil]
print('--------------------')
p=PostProcessor(args.out_dir,
    		inputFiles,
		treecut,   #in cutflow there should not be any cut
		modules=[btagSFUL2017(),MinitreeModuleConstr2J1T1_el_mc_UL2017(),jmeCorrectionsUL2017_MC_AK4CHS()],
		provenance=True,
		fwkJobReport=False,
        	#haddFileName=args.out_dir + '/Minitree_' + num + '.root',
		jsonInput=runsAndLumis())
p.run()
print("DONE")

