#from __future__ import print_function
#import pickle
import ROOT 
import numpy as np  
import pandas as pd
import sys
import os
import root_numpy

dir16 = '/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/'
dir17 = ''
dir18 = ''

_branches_mu = [
        'MuonEta',
        'dEta_mu_bJet',
        'mtwMass',
        'abs_lJetEta',
        'jetpTSum',
        'diJetMass',
        'cosThetaStar',
        'dR_bJet_lJet',
        'FW1',
        'Jet_pt',
        'Jet_btagDeepFlavB',
        'nbjet_sel'
    ]
def load_dataset ( max_entries = -1, channel = "Tchannel", lep = "mu" ):
    chain = ROOT.TChain('Events')
    chain.Add(dir16+'Minitree_'+channel+'_2J1T1_'+lep+'.root')

    print(chain.GetEntries())

    _dataset = root_numpy.tree2array (chain,
        branches = _branches_mu,
        selection = '',
        stop = max_entries
        )

    return { b : _dataset[b] for b in _branches_mu }


if __name__ == '__main__':

     print("Starting mu datsets \n")
    
     dataset_Tchannel_mu = load_dataset(10000,"Tchannel", "mu")
     dataset_ttbkg_mu = load_dataset(10000,"ttbar", "mu")
     dataset_WToLNu_2J_mu = load_dataset(10000, "WToLNu_2J" ,"mu")
     #print(dataset_mu)
     Muon_Eta = dataset_WToLNu_2J_mu ["MuonEta"]
     print(Muon_Eta)
     
