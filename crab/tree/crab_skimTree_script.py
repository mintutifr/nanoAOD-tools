#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
from MainModule import *
from jme import *
#from EfficiencyModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr16 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0) && Entry$<1000"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleMuon/NANOAOD/02Apr2020-v1/50000/FBFADBAD-5164-6A4D-A19E-EFF003090EC5.root"]
#inputFiles=["root://cms-xrd-global.cern.ch///store/mc/RunIISummer16NanoAODv7/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/70000/8F4FECBF-441D-1B4B-8FC5-E95B854BEF67.root"]
inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/Tree/ST_tch/09876EB9-DDB1-9A40-B887-A7AC06825101.root"]
p=PostProcessor(".",
		inputFiles,
		treecut,
		modules=[MainModuleConstr_mc_2017(),btagSF2017(),puWeight_2017(),jmeCorrections2017_MC_AK4CHS()],
		outputbranchsel="keep_and_drop.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
