#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from jme import *

from MinitreeModule import *
from cut_strings import *

treecut = cut_2J1T1_mu_UL2016preVFP
inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP_v2/Tbarchannel/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_06_Aug22_MCUL2016preVFP_Tbarchannel/220806_112911/0000/tree_14.root"]
#inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Data_preVFP_mu/Run2016D-HIPM_mu/SingleMuon/Tree_04_Jun22_Run2016D-HIPM_mu/220604_165834/0000/tree_1.root"]
#inputFiles=['tree_10.root']
p=PostProcessor(".",
		inputFiles,
		treecut,
		modules=[MinitreeModuleConstr2J1T1_mu_mc_UL2016preVFP()],#, jmeCorrectionsULRun2016C_preVFP_DATA_AK4CHS()],
		outputbranchsel="keep_and_drop_mu_Minitree.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
