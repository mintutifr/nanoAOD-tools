#!/usr/bin/env python
import os, sys
import ROOT

def hdampvariation_ttbar(top_pt, top_rapidity, top_phi,top_mass,top_pdgid,antitop_pt, antitop_rapidity, antitop_phi,antitop_mass,antitop_pdgid,hdamp):

    ROOT.gStyle.SetOptStat(0)
    hdamp_weight = 1.0
    inputs = [[top_pt, top_rapidity, top_phi,top_mass,top_pdgid,hdamp],[antitop_pt, antitop_rapidity, antitop_phi,antitop_mass,antitop_pdgid,hdamp]]





print(create_elSF('UL2018',300,-1.3,50,'Tight','noSyst'))
print(create_elSF('UL2018',300,-1.3,50,'Veto','noSyst'))
