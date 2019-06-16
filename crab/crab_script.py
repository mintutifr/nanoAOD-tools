#!/usr/bin/env python
import os,sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self, jetSelection):
        self.jetSel = jetSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("EventMass",  "F");
	#self.out.branch("emuLvector",  "ROOT.TLorentzVector()");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        eventSum = ROOT.TLorentzVector()
        for lep in muons :
            eventSum += lep.p4()
        for lep in electrons :
            eventSum += lep.p4()
        for j in filter(self.jetSel,jets):
            eventSum += j.p4()
        self.out.fillBranch("EventMass",eventSum.M())
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

exampleModuleConstr = lambda : exampleProducer(jetSelection= lambda j : j.pt > 200) 
 

treeCut="Entry$<500"
#treeCut="Jet_pt>200 && Entry$<500"
p=PostProcessor("rootfile",inputFiles(),treeCut,outputbranchsel="keep_and_drop.txt",modules=[exampleModuleConstr()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"
os.system("ls -lR")
