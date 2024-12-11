import math
import ROOT
import numpy as np
from foxwol_n_fourmomentumSolver import solveNu4Momentum

def calculate_top_quark_momentum(MuonPt, MuonEta, MuonPhi, MuonM, met, metphi, bJetMass, bJetPt, bJetEta, bJetPhi):
    # Step 1: Create Muon 4-momentum (muon4V)
    muon4V = ROOT.TLorentzVector()
    muon4V.SetPtEtaPhiM(MuonPt, MuonEta, MuonPhi, MuonM)

    # Step 2: Calculate Px and Py for neutrino from met and metphi
    Px_nu = met * math.cos(metphi)
    Py_nu = met * math.sin(metphi)

    # Step 3: Calculate transverse mass of the W boson (mtwMass)
    mtwMass = math.sqrt(abs((MuonPt + met)**2 - (MuonPt * math.cos(MuonPhi) + met * math.cos(metphi))**2 - (MuonPt * math.sin(MuonPhi) + met * math.sin(metphi))**2))

    # Step 4: Solve for the neutrino 4-momentum (neutrino4V) using the provided solver
    neutrino4V = solveNu4Momentum(muon4V, Px_nu, Py_nu)

    # Step 5: Calculate the W boson 4-momentum (w4V) by adding muon and neutrino 4-momenta
    w4V = muon4V + neutrino4V

    # Step 6: Create b-quark 4-momentum (bquark4V)
    bquark4V = ROOT.TLorentzVector()
    bquark4V.SetPtEtaPhiM(bJetPt, bJetEta, bJetPhi, bJetMass)

    # Step 7: Calculate the top quark 4-momentum (top4V) by adding W boson and b-quark 4-momenta
    top4V = w4V + bquark4V

    return top4V

def save_top_quark_properties_to_file(top4V, output_filename="top_quark_properties.root"):
    # Create a ROOT file and a TTree to store the top quark properties
    root_file = ROOT.TFile(output_filename, "RECREATE")
    tree = ROOT.TTree("TopQuarkTree", "Top Quark Properties")

    # Define variables to store the properties
    top_pt = ROOT.std.vector('float')()
    top_phi = ROOT.std.vector('float')()
    top_eta = ROOT.std.vector('float')()
    top_mass = ROOT.std.vector('float')()
    top_energy = ROOT.std.vector('float')()

    # Assign branches to the tree
    tree.Branch("top_pt", top_pt)
    tree.Branch("top_phi", top_phi)
    tree.Branch("top_eta", top_eta)
    tree.Branch("top_mass", top_mass)
    tree.Branch("top_energy", top_energy)

    # Fill the values into the branches
    top_pt.push_back(top4V.Pt())
    top_phi.push_back(top4V.Phi())
    top_eta.push_back(top4V.Eta())
    top_mass.push_back(top4V.M())
    top_energy.push_back(top4V.E())

    # Fill the tree
    tree.Fill()

    # Write to the file and close it
    root_file.Write()
    root_file.Close()
    print(f"Output saved to {output_filename}")


# Run the calculation
#top_quark_4momentum = calculate_top_quark_momentum(MuonPt, MuonEta, MuonPhi, MuonE, met, metphi, bJetMass, bJetPt, bJetEta, bJetPhi)

# Save the top quark properties to a ROOT file
#save_top_quark_properties_to_file(top_quark_4momentum, "top_quark_properties.root")





if __name__ == "__main__":
   # Step 1: Open the ROOT file
   file_path = "/nfs/home/common/RUN2_UL/Minitree_corr_bweight/EIGHTEEN/2J1T1/Minitree_Tchannel_2J1T1_mu.root"
   root_file = ROOT.TFile.Open(file_path)
   
   # Step 2: Access the "Events" tree in the file
   tree_name = "Events"
   tree = root_file.Get(tree_name)
   
   # Step 3: Prepare ardddrays to hold 4-momentum components
   #muon_pt, muon_eta, muon_phi, muon_mass = [],[],[],[]
   #bJet_mass, bJet_pt, bJet_eta, bJet_phi = [],[],[],[]
   #met, metphi = [], []
   
     

   # Step 4: Loop over events in the tree and extract relevant branches
   #for event in tree:
   bJet = ROOT.TLorentzVector()
   lepton = ROOT.TLorentzVector()
   for i, event in enumerate(tree):
       if i >= 10:  # Process only the first 10 entries
            break
       lepton_pt = event.MuonPt
       lepton_eta = event.MuonEta
       lepton_phi = event.MuonPhi
       lepton_mass = event.MuonMass
       lepton.SetPtEtaPhiM(muon_pt, muon_eta, muon_phi, muon_mass)
 	
       b_jet = event.nbjet_sel
       bJet_pt = event.Jet_pt[b_jet]
       bJet_eta = event.Jet_eta[b_jet]
       bJet_phi = event.Jet_phi[b_jet]
       bJet_mass = event.Jet_mass[b_jet]
       bJet.SetPtEtaPhiM(bJet_pt, bJet_eta, bJet_phi, bJet_mass) 

       met = event.MET_pt
       metphi = event.MET_phi
  
       top4v =  calculate_top_quark_momentum(muon_pt, muon_eta, muon_phi, muon_mass, met, metphi, bJet_mass, bJet_pt, bJet_eta, bJet_phi)
       print("mass = ",top4v.M())
      
   # Step 6: Clean up
   root_file.Close()
