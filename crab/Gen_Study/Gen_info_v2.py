import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *


import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
#from exampleModule import *
#from MainModule import *





class MainProducer(Module):
    def __init__(self):
	pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	self.out.branch("top_mass_gen", "F")	

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
	Genparts = Collection(event,"GenPart")
	for genpart in Genparts:
	    if(abs(genpart.pdgId)==6):
		motheridx =  genpart.genPartIdxMother
                PDG = genpart.pdgId
                motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
		if(abs(motherPDG!=6)):
		    top_mass_gen = genpart.mass
                    #self.top_mass_hist.Fill(genpart.mass)
                    self.out.fillBranch("top_mass_gen", top_mass_gen)
        return True


# define modules using the pt_Thes_mu[self.datayear]syntax 'name = lambda : constructor' to avoid having them loaded when not needed

MainModuleConstr_Gen = lambda : MainProducer()

treecut = "nJet>0 && Jet_pt>20 && (Sum$(Muon_pt>20)>0 || Sum$(Electron_pt>30)>0)"
treecutEN = "Entry$<100"#(nMuon>0 || nElectron>0)" # && (Muon_pt>5 || Electron_pt>10) (nMuon>0 || nElectron>0)"

inputFiles=[	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tbarchannel_2J1T1_el.root",
		"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]

p=PostProcessor(".",
		inputFiles,
		treecutEN,
		modules=[MainModuleConstr_Gen()],
		outputbranchsel="clean.txt",
		provenance=True,
		fwkJobReport=True,
		jsonInput=runsAndLumis())
		
p.run()

print "DONE"
