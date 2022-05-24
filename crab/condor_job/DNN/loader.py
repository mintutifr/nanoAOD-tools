#from __future__ import print_function
#import pickle
import ROOT 
import numpy as np  
import pandas as pd
import sys
import os
import root_numpy

dir16 = '/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/'
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
        'FW1'
    ]
def load_dataset_signal_mu ( max_entries = -1 ):
    chain = ROOT.TChain('Events')
    chain.Add(dir16+'Minitree_Tchannel_2J1T1_mu.root')
    
    print(chain.GetEntries())

    _dataset = root_numpy.tree2array (chain,
      	branches = _branches_mu,
      	selection = '', 
      	stop = max_entries
     	)

    return { b : _dataset[b] for b in _branches_mu }

def load_dataset_ttbkg_mu ( max_entries = -1 ):
    chain = ROOT.TChain('Events')
    chain.Add(dir16+'Minitree_ttbar_2J1T1_mu.root')

    print(chain.GetEntries())

    _dataset = root_numpy.tree2array (chain,
        branches = _branches_mu,
        selection = '',
        stop = max_entries
        )

    return { b : _dataset[b] for b in _branches_mu }

def load_dataset_EWKbkg_mu ( max_entries = -1 ):
    chain = ROOT.TChain('Events')
    chain.Add(dir16+'Minitree_WToLNu_1J_2J1T1_mu.root')

    print(chain.GetEntries())

    _dataset = root_numpy.tree2array (chain,
        branches = _branches_mu,
        selection = '',
        stop = max_entries
        )

    return { b : _dataset[b] for b in _branches_mu }

if __name__ == '__main__':

     print("Starting mu datsets \n")
    
     dataset_signal_mu = load_dataset_signal_mu(10000)
     dataset_ttbkg_mu = load_dataset_ttbkg_mu(10000)
     dataset_EWKbkg_mu = load_dataset_EWKbkg_mu(10000)
     #print(dataset_mu)
     Muon_Eta = dataset_EWKbkg_mu ["MuonEta"]
     #print(Muon_Eta)
     
