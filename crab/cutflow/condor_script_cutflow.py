#!/usr/bin/env python

from cutflowModule_new import *

inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/QCD_Pt-800To1000_MuEnriched/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/Tree_22_Apr22_MCUL2016preVFP_QCD_Pt-800To1000_MuEnriched_check/220422_154743/0000/tree_44.root"]


MCIso = ROOT.TFile.Open(inputFiles[0],'Read')
ROOT.gROOT.cd()
myTree = MCIso.Get('Events')
#myTree.Print()

modules=cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP()
modules.analyze(myTree)

print "DONE"

