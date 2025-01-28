#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#import main module
from Gen_mass_reconstract_SingleTop import *

#treecut = "Entry$<1000"
treecut = "nGenDressedLepton>0 && nGenJet>0" #&& Entry$<1000"
#nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)" #&& Entry$<10000"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"
#inputFiles=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer22UL16wmLHENanoGEN/ST_t-channel_antitop_4f_InclusiveDecays_wtop0p55_TuneCP5_fixWidth_13TeV-powheg-madspin-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v13-v1/70000/364D8C12-4C30-8C48-B0BF-3C8AD26F8987.root"]
#inputFiles=[ "/home/mikumar/t3store3/workarea/Nanoaod_tools/CMSSW_10_2_28/src/PhysicsTools/NanoAODTools/crab/Gen_Study/NANOGEN_file_wtop1p0.root"] 
	
p=PostProcessor( ".",
        inputFiles(),
        treecut,
	modules=[NanoGenConstr_UL2016()],
        outputbranchsel="clean_All_keep_GenPart.txt",
        provenance=True,
        fwkJobReport=True,
        jsonInput=runsAndLumis())
 
p.run()

print("DONE")
