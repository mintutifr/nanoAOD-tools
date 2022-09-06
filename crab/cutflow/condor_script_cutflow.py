#!/usr/bin/env python

from cutflowModule_new import *

inputFiles=["root://cms-xrd-global.cern.ch//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP_v2/Tchannel/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_06_Aug22_MCUL2016preVFP_Tchannel/220806_113029/0000/tree_1.root"]
#inputFiles=["tree_1.root"]

MCIso = ROOT.TFile.Open(inputFiles[0],'Read')
ROOT.gROOT.cd()
myTree = MCIso.Get('Events')
#myTree.Print()

modules=cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP()
modules.analyze(myTree)

print "DONE"

