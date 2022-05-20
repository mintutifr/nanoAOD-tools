#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from jme import *

from MinitreeModule import *
from cut_strings import *

treecut = cut_2J1T1_mu_2016

#inputFiles=["6E1B25E9-BBAE-B14F-92C1-FDC95C9EC4A2_Skim.root"]
#inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2/Tree_crab/SIXTEEN/Data_mu_new/Run2016D_mu/SingleMuon/Tree_12_Oct21_Run2016D_mu/211012_170845/0000/tree_1.root"]
inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_24/src/Inputfiles/skimtree/DATA/Single_muon/RUNB/tree_10.root"]
p=PostProcessor(".",
		inputFiles(),
		treecut,
		modules=[MinitreeModuleConstr2J1T1_mu_data_UL2016preVFP(), jmeCorrectionsULRun2016C_preVFP_DATA_AK4CHS()],
		outputbranchsel="keep_and_drop_mu_Minitree.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
