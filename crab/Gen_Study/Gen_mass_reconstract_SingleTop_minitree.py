#!/usr/bin/env python
import os, sys
import ROOT 
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *
class NanoGenModule(Module):
    def __init__(self,datayear):
	self.writeHistFile=True
	self.datayear = datayear
    #def beginJob(self,histFile=None,histDirName=None):
	#Module.beginJob(self,histFile,histDirName)
	#self.pt_hist = ROOT.TH1D("pt_hist","pt_hist",20,0.0,400)
	#self.eta_hist = ROOT.TH1D("eta_hist","eta_hist",20,0.0,5.0)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
	pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        return True

NanoGenConstr_UL2016 = lambda : NanoGenModule('UL2016')
