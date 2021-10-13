#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
from MainModule import *
from jme import *
#from EfficiencyModule import *
from  btv import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr16 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)"# && Entry$<10000"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleMuon/NANOAOD/02Apr2020-v1/50000/FBFADBAD-5164-6A4D-A19E-EFF003090EC5.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/single_muondata_2016_runD/5A4AA866-8941-334C-A591-7D2728C6F63F.root"]
#inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/ST_tch/06314878-0D6B-544B-9E2C-C5EDCD0666D3_2017.root"]
p=PostProcessor(".",
		inputFiles(),
		treecut,
		modules=[MainModuleConstr_data_2016_singleMuon(),jmeCorrectionsRun2016H_DATA_AK4CHS()],
		outputbranchsel="keep_and_drop.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
