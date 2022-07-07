#!/usr/bin/env python

from cutflowModule_new import *

inputFiles=["root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/Tbarchannel/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_05_Jun22_MCUL2016preVFP_Tbarchannel/220605_064232/0000/tree_4.root"]


MCIso = ROOT.TFile.Open(inputFiles[0],'Read')
ROOT.gROOT.cd()
myTree = MCIso.Get('Events')
#myTree.Print()

modules=cutflowModuleConstr_2J1T1_mu_mc_UL2016preVFP()
modules.analyze(myTree)

print "DONE"

