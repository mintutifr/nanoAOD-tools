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
        self.out.branch("top_ID","I")
        self.out.branch("top_is_lastcopy","F")
        self.out.branch("top_mass_gen", "F")
        self.out.branch("top_mass_gen_reco", "F")
        self.out.branch("top_pt_gen", "F")
        self.out.branch("top_pt_gen_reco", "F")
        self.out.branch("top_eta_gen", "F")
        self.out.branch("top_eta_gen_reco", "F")
        self.out.branch("top_phi_gen", "F")
        self.out.branch("top_phi_gen_reco", "F")

        self.out.branch("tau_to_el_flag", "F")
        self.out.branch("tau_to_mu_flag", "F")
        self.out.branch("el_flag", "F")
        self.out.branch("mu_flag", "F")

        self.out.branch("lepton_ID","I")
        self.out.branch("lepton_pt_gen", "F")
        self.out.branch("lepton_eta_gen", "F")
        self.out.branch("lepton_phi_gen", "F")

        self.out.branch("minidR_dresslep","F")
        self.out.branch("DressLep_pt_gen", "F")
        self.out.branch("DressLep_eta_gen", "F")
        self.out.branch("DressLep_phi_gen", "F")
        self.out.branch("DressLep_mass_gen", "F")
        self.out.branch("DressLep_ID", "I")

        self.out.branch("neutrino_ID","I")
        self.out.branch("neutrino_pt_gen", "F")
        self.out.branch("neutrino_eta_gen", "F")
        self.out.branch("neutrino_phi_gen", "F")
        self.out.branch("neutrino_el_flag", "F")
        self.out.branch("neutrino_mu_flag", "F")

        self.out.branch("W_ID","I")
        self.out.branch("W_mass_gen", "F")
        self.out.branch("W_mass_gen_reco", "F")
        self.out.branch("W_pt_gen", "F")
        self.out.branch("W_pt_gen_reco", "F")
        self.out.branch("W_eta_gen", "F")
        self.out.branch("W_eta_gen_reco", "F")
        self.out.branch("W_phi_gen", "F")
        self.out.branch("W_phi_gen_reco", "F")
        self.out.branch("W_to_el_flag", "F")
        self.out.branch("W_to_mu_flag", "F")

        self.out.branch("bjet_ID","I")
        self.out.branch("bjet_pt_gen", "F")
        self.out.branch("bjet_eta_gen", "F")
        self.out.branch("bjet_phi_gen", "F")
        self.out.branch("bjet_mass_gen", "F")

        self.out.branch("bpart_ID","I")
        self.out.branch("bpart_pt_gen", "F")
        self.out.branch("bpart_eta_gen", "F")
        self.out.branch("bpart_phi_gen", "F")
        self.out.branch("minDR_bpart_bjet","F")
        self.out.branch("DR_dresslepton_bjet","F")
        ## create inference session using ort.InferenceSession from a given model
        
       
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    ##Def of rapidity
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        # Get the desired arrays from the data
        Genparts = Collection(event,"GenPart")
        GenPart_pdgId,GenPart_statusFlags,GenPart_pt,GenPart_phi,GenPart_eta,GenPart_mass = ([] for i in range(6))
        for genpart in Genparts:
            GenPart_statusFlags.append(genpart.statusFlags)
            GenPart_pt.append(genpart.pt)
            GenPart_phi.append(genpart.phi)
            GenPart_eta.append(genpart.eta)
            GenPart_mass.append(genpart.mass)
            GenPart_pdgId.append(genpart.pdgId)

        #print(GenPart_pdgId)
        countTop = 0
        ptop = ROOT.TLorentzVector()
        patop = ROOT.TLorentzVector()
        ptop_Ngenpart = -99
        patop_Ngenpart = -99
        for i in range(0, len(GenPart_pdgId)):
            if GenPart_pdgId[i] == 6:
                if (((GenPart_statusFlags[i] >> 12) & 0x1) > 0):
                    countTop += 1
                    ptop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i])
                    ptop_Ngenpart = i  
            if GenPart_pdgId[i] == -6:
                if (((GenPart_statusFlags[i] >> 12) & 0x1) > 0):
                    countTop += 1
                    patop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i])
                    patop_Ngenpart = i
        
            # Creating the array with all info needed to pass to the NN model, already normalised
        #print(ptop.M())

        return True

gen_info_Module = lambda : gen_info()    
