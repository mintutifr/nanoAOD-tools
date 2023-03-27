import ROOT
import  sys , os
#https://indico.cern.ch/event/704163/contributions/2936719/attachments/1693833/2726445/Tutorial-PyROOT.pdf


FileName_Mc   = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/Ele_trigger_ttbar_FullyLeptonic_mu.root"
FileName_data = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/Ele_trigger_Data_mu_mu.root"
print "Reading  Mc from Events ", FileName_Mc
print "Reading  Data from Events ", FileName_data

#read histogram and store
inFile_Mc = ROOT.TFile.Open(FileName_Mc,"READ")
inFile_data = ROOT.TFile.Open(FileName_data,"READ")

hist_Mc_elNmu = inFile_Mc.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet")
hist_Mc_mu = inFile_Mc.Get("Events_2D_hist/Event_HLT_IsoMu27")

hist_data_elNmu = inFile_data.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet")
hist_data_mu = inFile_data.Get("Events_2D_hist/Event_HLT_IsoMu27")
		
		
#calculate Efficiency
Effi_Mc = ROOT.TEfficiency(hist_Mc_elNmu,hist_Mc_mu)
Effi_data = ROOT.TEfficiency(hist_data_elNmu,hist_data_mu)

Effi_Mc_hist = Effi_Mc.CreateHistogram()
Effi_Mc_hist.GetYaxis().SetTitle("p_{T} [GeV]")
Effi_Mc_hist.GetXaxis().SetTitle("SuperCluster #eta") #SuperCluster

Effi_data_hist = Effi_data.CreateHistogram()
Effi_data_hist.GetYaxis().SetTitle("p_{T} [GeV]")
Effi_data_hist.GetXaxis().SetTitle("SuperCluster #eta") #SuperCluster

SF = Effi_data_hist.Clone()
SF.Divide(Effi_Mc_hist)

outfile="/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/egammaEffi.txt_EGM2D.root"

outRootFile = ROOT.TFile.Open(outfile ,"RECREATE")
print 'output file = ',outfile
outRootFile.cd()

Effi_Mc_hist.Write("EGamma_EffMC2D")
Effi_data_hist.Write("EGamma_EffData2D")
SF.Write("EGamma_SF2D")
