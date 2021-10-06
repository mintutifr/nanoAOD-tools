#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from cutflowModule import *

#treecut = "(HLT_IsoMu24==1 || HLT_IsoTkMu24 ==1) && (Sum$(Muon_pt>26 && abs(Muon_eta)<2.4 && Muon_pfRelIso04_all<0.06 && Muon_tightId==1)==1) && (Sum$(Muon_looseId==1 && Muon_pt>10 && abs(Muon_eta)<2.4 && Muon_pfRelIso04_all<0.2)==1) && (Sum$(Electron_cutBased ==1 && Electron_pt>15 && abs(Electron_eta)<2.5 && (abs(Electron_eta) < 1.4442 || abs(Electron_eta) > 1.566))==0) && (Sum$(Jet_pt>40 && abs(Jet_eta)<4.7 && Jet_jetId!=0 && Jet_dR_Ljet_Isomu>0.4)==2) && (Sum$(Jet_pt>40 && Jet_dR_Ljet_Isomu>0.4 && Jet_jetId!=0 && abs(Jet_eta)<2.4 && Jet_btagDeepB>0.7527)==0)"#"(abs(Jet_eta)<3.5 && abs(Jet_eta)>2.5)"#(event==18857645 || event==18866000)"# && Entry$<=487000 && event==2396359"#2014531"#2396359"
treecut = "Entry$<10000"
inputFiles=["/afs/cern.ch/user/m/mikumar/work/private/NanoAOD_new/CMSSW_10_6_0/src/Inputroot_files/mintree/ST_tch/06314878-0D6B-544B-9E2C-C5EDCD0666D3_2017_Skim_2017.root"]
p=PostProcessor(".",
		inputFiles,
		#treecut,   #in cutflow there should not be any cut
		modules=[cutflowModuleConstr_2J1T1_mu_mc_2017()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis(),
		noOut=False,
		histFileName="Cutflow_hist.root",
		histDirName="histograms")
p.run()

print "DONE"

