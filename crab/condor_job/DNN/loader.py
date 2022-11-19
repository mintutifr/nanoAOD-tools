#from __future__ import print_function
#import pickle
import ROOT 
import numpy as np  
#import pandas as pd
import pandas as pd
import sys
import os
import root_numpy

dir = {
	'ULpreVFP2016' : '/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/',
	'ULpostVFP2016' : '/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/',
	'UL2017' : '/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/',
	'UL2018' : ''
}

def load_dataset ( max_entries = -1, channel = "Tchannel", lep = "mu",year = "ULpreVFP2016" ):
    if(lep=="mu"):
        lepton = "Muon"
    elif(lep=="el"):
        lepton = "Electron" 

    _branches_mu = [
        	lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E', lepton+'Charge',
        	'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        	'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        	'Px_nu', 'Py_nu', 'Pz_nu',
        	'dEta_'+lep+'_lJet', 'dEta_'+lep+'_bJet',
        	'dPhi_'+lep+'_lJet', 'dPhi_'+lep+'_bJet', 
        	'bJetdeepJet', 'lJetdeepJet',
        	'Jet_pt', 'Jet_partonFlavour',
        	'dR_bJet_lJet',
        	'nbjet_sel',
        	'mtwMass',
        	'abs_lJetEta',
        	'jetpTSum',
        	'diJetMass',
        	'cosThetaStar',
        	'FW1',
        	'Xsec_wgt',
        	'LHEWeightSign',
        	'L1PreFiringWeight_Nom',
        	'event',
        	'topMass'
    	]
    _branches_mu_Data = [
        	lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E',   lepton+'Charge',
        	'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        	'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        	'Px_nu', 'Py_nu', 'Pz_nu',
        	'dEta_'+lep+'_lJet', 'dEta_'+lep+'_bJet', 
        	'dPhi_'+lep+'_lJet', 'dPhi_'+lep+'_bJet',
        	'bJetdeepJet', 'lJetdeepJet',
        	'Jet_pt', 
        	'dR_bJet_lJet',
        	'nbjet_sel',
        	'mtwMass',
        	'abs_lJetEta',
        	'jetpTSum',
        	'diJetMass',
        	'cosThetaStar',
        	'FW1',
        	'L1PreFiringWeight_Nom',
        	'event',
        	'topMass'
    	]


    chain = ROOT.TChain('Events')
    if "Data" in channel:
        _branches_mu.remove('Xsec_wgt')
        _branches_mu.remove('LHEWeightSign')
        _branches_mu.remove('Jet_partonFlavour')

        chain.Add(dir[year]+'2J1T0/Minitree_'+channel+'_2J1T0_'+lep+'.root')
        print( 'Entries Data: ',chain.GetEntries(), "\tSelected : ",max_entries)

        _dataset = root_numpy.tree2array (chain,
                branches = _branches_mu,
                selection = '',
                stop = max_entries
                )
        return { b : _dataset[b] for b in _branches_mu }
    else:
        chain.Add(dir[year]+'2J1T1/Minitree_'+channel+'_2J1T1_'+lep+'.root')

        print( 'Entries '+channel+': ',chain.GetEntries(), "\tSelected : ",max_entries)

        _dataset = root_numpy.tree2array (chain,
                branches = _branches_mu,
                selection = '',
                stop = max_entries
                )

        return { b : _dataset[b] for b in _branches_mu }


if __name__ == '__main__':

     print("Starting mu datsets \n")
    
     dataset_Tchannel_mu = load_dataset(10000,"Tchannel", "mu")
     dataset_ttbkg_mu = load_dataset(10000,"ttbar_FullyLeptonic", "mu")
     #dataset_WToLNu_2J_mu = load_dataset(10000, "WToLNu_2J" ,"mu")
     #print(dataset_mu)
     Muon_Eta =  dataset_Tchannel_mu ["MuonEta"]
     print(Muon_Eta)
     
