import ROOT
import numpy as np
import os,sys
import math
import random
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


def mk_safe(fct, *args):
    try:
        return fct(*args)
    except Exception as e:
        if any('Error in function boost::math::erf_inv' in arg for arg in e.args):
            print('WARNING: catching exception and returning -1. Exception arguments: %s' % e.args)
            return -1.
        else:
            raise e


class gen_info(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("top_Ngenpart","F")
        self.out.branch("top_mass","F")
        self.out.branch("atop_Ngenpart","F")
        self.out.branch("atop_mass","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # Get the desired arrays from the data
        Genparts = Collection(event,"GenPart")
        ptop_Ngenpart = -9
        top_mass = -999
        patop_Ngenpart = -9
        atop_mass = -999
        Ngenpart_counter = -1
        for genpart in Genparts:
            Ngenpart_counter += 1
            if (genpart.pdgId == 6 and ((genpart.statusFlags >> 13) & 0x1) > 0):
                    ptop_Ngenpart = Ngenpart_counter
                    top_mass = genpart.mass
            if (genpart.pdgId == -6 and ((genpart.statusFlags >> 13) & 0x1) > 0):
                    patop_Ngenpart = Ngenpart_counter
                    atop_mass = genpart.mass

        self.out.fillBranch("top_Ngenpart",ptop_Ngenpart)
        self.out.fillBranch("atop_Ngenpart",patop_Ngenpart)
        self.out.fillBranch("top_mass",top_mass)
        self.out.fillBranch("atop_mass",atop_mass)

        return True

gen_info_Module = lambda : gen_info()    
