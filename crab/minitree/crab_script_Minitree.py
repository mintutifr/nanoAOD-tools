#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from jme import *

from MinitreeModule import *
from cut_strings import *

treecut = cut_3J2T1_mu_2016

#inputFiles=["6E1B25E9-BBAE-B14F-92C1-FDC95C9EC4A2_Skim.root"]
#inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2/Tree_crab/SIXTEEN/Data_mu_new/Run2016D_mu/SingleMuon/Tree_12_Oct21_Run2016D_mu/211012_170845/0000/tree_1.root"]
inputFiles=['root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_04_Jun22_MCUL2016preVFP_ttbar_SemiLeptonic/220604_162528/0000/tree_10.root']
p=PostProcessor(".",
		inputFiles,
		treecut,
		modules=[MinitreeModuleConstr3J2T1_mu_data_UL2016preVFP()],#, jmeCorrectionsULRun2016C_preVFP_DATA_AK4CHS()],
		outputbranchsel="keep_and_drop_mu_Minitree.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
