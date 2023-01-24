#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from EfficiencyModule import *


treecut=" Entry$<500 "
#inputFiles=["root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv3/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/NANOAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v1/120000/E4046A1B-A2E1-E811-8878-0025905B85DC.root"]
inputFiles=["A85EB5FE-5F7F-7947-A070-1FC00B3A4591.root"]
#/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/condor_job/lepton_trigger_eff/tree_5.root"]
p=PostProcessor(".",
		inputFiles,
		#treecut,  #efficecncy histogram there should be no cut
		modules=[EfficiencyConstr_UL2017()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis(),
		noOut=False,
		histFileName="Ele_trigger_hist.root",
		histDirName="Events_2D_hist")
p.run()

print "DONE"

