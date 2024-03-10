import ROOT as rt
import numpy as np
import scipy.integrate as sp
import argparse as arg
import math

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['ULpreVFP2016', 'ULpostVFP2016','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.lepton[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

print(args)

lep = args.lepton[0]
year= args.year[0]

if(lep=="mu"):
        lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)



#applydir = 'DNN_output_with_mtwCut/Apply_all/' ;  output_fileName = "ROC_TGraphs/Efficiency_info_"+year+"_"+lep+"_with_weights.root"
DNN_applydir = 'DNN_output_without_mtwCut/2J1T1/Apply_all/' 
output_fileName = "Plots/Correlation_Reco_top_mass_t_ch_CAsi"+year+"_"+lep+"."

channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop',]# 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
MCcut ="Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*bWeight*L1PreFiringWeight_Nom*(mtwMass>50.0)*(dR_bJet_lJet>0.4)*bJetPUJetID_SF*lJetPUJetID_SF*mtw_weight_50GeVCut"
Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"

DNN_Fpaths = {}
EvtWeight_Fpaths = {} 
for channel in channels:
        DNN_Fpaths[channel] = DNN_applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
        EvtWeight_Fpaths[channel] = "/home/mikumar/t3store/workarea/Nanoaod_tools/CMSSW_10_2_28/src/Run2UL_Analysis/stack_plots_before_ML/Minitree_with_mtw_weight/2J1T1/"+year+"_"+channel+"_Apply_all_"+lep+".root"
        
           
print(DNN_Fpaths)
print()
print(EvtWeight_Fpaths)

Variable = "lntopMass"
Variable = "TMath::Log(topMass)"
Variable = "topMass"
X_axies = "ln(m_{Top})"
Y_axies = "Events/(20)"
lest_bin = math.log(100.0)
max_bin = math.log(400.0)
lest_bin =100.0
max_bin = 400.0
Num_bin = 6


hs = {}
hs_wrong_assignment = {}
infiles = {}
intree = {}
DNN_sig_bins =  np.array([0.0 , 0.1 , 0.2 , 0.3 ,  0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.90, 1.0])
len_DNN_sig_bins = len(DNN_sig_bins)
topMass_bins =  np.array([100.0 ,125.0,150.0,175.0 ,200.0,225.0 , 250.0 ,275.0,  300.0 ,325.0, 350.0 ,375.0, 400.0])
len_topMass_bins = len(topMass_bins)

hs_corre_Tchannel_CAssig = rt.TH2F('corre_Tchannel_CAssig', 't-ch. sig;m_{t} (GeV) ;DNN  Score corr. tch assign ',len_topMass_bins-1, topMass_bins, len_DNN_sig_bins-1, DNN_sig_bins)
hs_corre_Ttbar_CAssig = rt.TH2F('corre_Ttbar_CAssig', 't#bar{t};m_{t} (GeV) ;DNN corr. tch assign',len_topMass_bins-1, topMass_bins, len_DNN_sig_bins-1, DNN_sig_bins)

hs_corre_Tchannel_CAssig_temp = rt.TH2F('corre_Tchannel_CAssig_temp', 't-ch. sig;m_{t} (GeV) ;DNN Score corr. tch assign ',len_topMass_bins-1, topMass_bins, len_DNN_sig_bins-1, DNN_sig_bins)
hs_corre_Ttbar_CAssig_temp = rt.TH2F('corre_Ttbar_CAssig_temp', 't#bar{t};m_{t} (GeV) ;DNN Score corr. tch assign',len_topMass_bins-1, topMass_bins, len_DNN_sig_bins-1, DNN_sig_bins)

top_mass_hist_ttbar_list = {}
top_mass_hist_ttbar = rt.TH1D('top_mass_hist_ttbar', ';m_{t} (GeV) ;Unit Normalized ',len_topMass_bins-1, topMass_bins)
top_mass_hist_ttbar_temp = rt.TH1D('top_mass_hist_ttbar_temp', ';m_{t} (GeV) ;Unit Normalized ',len_topMass_bins-1, topMass_bins)

top_mass_hist_tch_list = {}
top_mass_hist_tch = rt.TH1D('top_mass_hist_tch', ';m_{t} (GeV) ;Unit Normalized ',len_topMass_bins-1, topMass_bins)
top_mass_hist_tch_temp = rt.TH1D('top_mass_hist_tch_temp', ';m_{t} (GeV) ;Unit Normalized ',len_topMass_bins-1, topMass_bins)

DNN_Cuts = [0.5,0.6,0.7,0.8,0.9]

n_sel_sig = np.zeros(len_DNN_sig_bins+1)
n_sel_bkg = np.zeros(len_DNN_sig_bins+1)

N_QCD = 0.0
N_NonQCD = 0.0

for channel in channels:
    print(channel)
    infiles[channel] = rt.TFile.Open(DNN_Fpaths[channel], 'READ')
    intree[channel] = infiles[channel].Get('Events')
    intree[channel].AddFriend ("Events",EvtWeight_Fpaths[channel])
    
    rt.gROOT.cd()

    hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
    hs_wrong_assignment[channel] = rt.TH1F('hs_wrong_assignment' + channel, '', Num_bin, lest_bin, max_bin)

DNNcut_sig = 0.0
final_cut_corr_assg =  MCcut+"*(bjet_partonFlavour*"+lepton+"Charge==5)*(t_ch_CAsi>="+str(DNNcut_sig)+")"
final_cut_wrong_assg = MCcut+"*(bjet_partonFlavour*"+lepton+"Charge!=5)*(t_ch_CAsi>="+str(DNNcut_sig)+")"
print(final_cut_corr_assg)
print(final_cut_wrong_assg)


for channel in channels:       
    intree[channel].Project('hs' + channel, Variable, final_cut_corr_assg)
    intree[channel].Project('hs_wrong_assignment' + channel, Variable, final_cut_wrong_assg)
    if(channel in ['Tchannel' , 'Tbarchannel']):
        hs_corre_Tchannel_CAssig_temp.Reset()
        #intree[channel].Scan(Variable+":t_ch_CAsi")
        intree[channel].Project('corre_Tchannel_CAssig_temp', "t_ch_CAsi:"+Variable, final_cut_corr_assg)
        hs_corre_Tchannel_CAssig_temp.Print()
        hs_corre_Tchannel_CAssig.Add(hs_corre_Tchannel_CAssig_temp)
       
    if(channel in ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
        hs_corre_Ttbar_CAssig_temp.Reset()
        intree[channel].Project('corre_Ttbar_CAssig_temp', "t_ch_CAsi:"+Variable, final_cut_corr_assg)
        hs_corre_Ttbar_CAssig_temp.Print()
        hs_corre_Ttbar_CAssig.Add(hs_corre_Ttbar_CAssig_temp)
        

    #hs[channel].Print()
    #hs_wrong_assignment[channel].Print()


    N_NonQCD += round(hs[channel].Integral(1,Num_bin),4)
    N_NonQCD += round(hs_wrong_assignment[channel].Integral(1, Num_bin),4)
        
      
        
        
print(" NonQCD Events = ",N_NonQCD)
print(hs_corre_Tchannel_CAssig.GetCorrelationFactor())

outfile = rt.TFile(output_fileName+"root", "recreate")
outfile.cd()
hs_corre_Tchannel_CAssig.Write("Tchannel_corr")
hs_corre_Ttbar_CAssig.Write("Ttbar_corr")

outfile.Close()


c2 = rt.TCanvas('c2', '', 1400, 800)
c2.Divide(2,1)

c2.cd(1)
rt.gStyle.SetOptStat(0)
pad1 = rt.TPad("pad1","pad1",0,0,1,1)
pad1.SetRightMargin(0.11)
pad1.Draw()
hs_corre_Tchannel_CAssig.Draw("colz")

corr_tch = rt.TPaveText(0.26, 0.93, 0.36, 0.95, "brNDC");
corr_tch.SetFillStyle(0)
corr_tch.SetBorderSize(0)
corr_tch.SetMargin(0)
corr_tch.SetTextFont(42)
corr_tch.SetTextSize(0.05)
corr_tch.SetTextAlign(33)
corr_tch.AddText("#rho = "+str(100*round(hs_corre_Tchannel_CAssig.GetCorrelationFactor(),2))+"%")
corr_tch.GetListOfLines().Last().SetTextFont(42)
corr_tch.Draw()


c2.cd(2)
rt.gStyle.SetOptStat(0)
pad2 = rt.TPad("pad2","pad2",0,0,1,1)
pad2.SetRightMargin(1000)
pad2.SetLeftMargin(0.5)
pad2.Draw()

hs_corre_Ttbar_CAssig.Draw("colz")

corr_ttbar = rt.TPaveText(0.26, 0.93, 0.36, 0.95, "brNDC");
corr_ttbar.SetFillStyle(0)
corr_ttbar.SetBorderSize(0)
corr_ttbar.SetMargin(0)
corr_ttbar.SetTextFont(42)
corr_ttbar.SetTextSize(0.05)
corr_ttbar.SetTextAlign(33)
corr_ttbar.AddText("#rho = "+str(100*round(hs_corre_Ttbar_CAssig.GetCorrelationFactor(),2))+"%")
corr_ttbar.GetListOfLines().Last().SetTextFont(42)
corr_ttbar.Draw()

c2.Update()

c2.SaveAs(output_fileName+"png")
c2.SaveAs(output_fileName+"pdf")


            
for cut in DNN_Cuts:
    DNNcut = MCcut+"*(bjet_partonFlavour*"+lepton+"Charge==5)*"+"(t_ch_CAsi>="+str(cut)+")"
    print(DNNcut)
    top_mass_hist_ttbar.Reset()
    top_mass_hist_tch.Reset()
    for channel in channels:
        if(channel in ['Tchannel' , 'Tbarchannel']):
            top_mass_hist_tch_temp.Reset()
            intree[channel].Project('top_mass_hist_tch_temp',Variable, DNNcut)
            top_mass_hist_tch.Add(top_mass_hist_tch_temp)
         
        if(channel in ['tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
            top_mass_hist_ttbar_temp.Reset()
            intree[channel].Project('top_mass_hist_ttbar_temp',Variable, DNNcut)
            top_mass_hist_ttbar.Add(top_mass_hist_ttbar_temp)
            
    top_mass_hist_ttbar_list[str(cut)]=top_mass_hist_ttbar.Clone()
    top_mass_hist_tch_list[str(cut)]=top_mass_hist_tch.Clone()
    top_mass_hist_ttbar_list[str(cut)].Print()
    top_mass_hist_tch_list[str(cut)].Print()
    
for i,cut in enumerate(DNN_Cuts):
    print(str(cut))
    top_mass_hist_tch_list[str(cut)].Print()
    top_mass_hist_ttbar_list[str(cut)].Print()
     
         
colors = [rt.kRed, rt.kBlue, rt.kGreen, rt.kOrange, rt.kBlack]
legend = rt.TLegend(0.55, 0.65, 0.75, 0.85)
legend.SetBorderSize(0)
legend.SetTextSize(0.05)
legend.SetLineColor(0)
legend.SetLineStyle(1)
legend.SetLineWidth(1)
legend.SetFillColor(0)
legend.SetFillStyle(1001)
    
c3 = rt.TCanvas('c3', '', 1400, 800)
c3.Divide(2,1)

c3.cd(1)
rt.gStyle.SetOptStat(0)
pad1 = rt.TPad("pad1","pad1",0,0,1,1)
pad1.SetRightMargin(0.11)
pad1.Draw()

top_mass_hist_tch_list["0.5"].SetLineColor(colors[0])
top_mass_hist_tch_list["0.5"].Draw("hist")
for i,cut in enumerate(DNN_Cuts):
    #print(str(cut))
    #top_mass_hist_tch_list[str(cut)].Print()
    top_mass_hist_tch_list[str(cut)].SetLineColor(colors[i])
    top_mass_hist_tch_list[str(cut)].Scale(1/top_mass_hist_tch_list[str(cut)].Integral())
    top_mass_hist_tch_list[str(cut)].Draw("hist;same")
    legend.AddEntry(top_mass_hist_tch_list[str(cut)], "DNN >=" + str(cut), "l")

legend.Draw()

c3.cd(2)
rt.gStyle.SetOptStat(0)
pad2 = rt.TPad("pad2","pad2",0,0,1,1)
pad2.SetRightMargin(0.11)
pad2.Draw()

top_mass_hist_ttbar_list["0.5"].SetLineColor(colors[0])
top_mass_hist_ttbar_list["0.5"].Draw("hist")
for i,cut in enumerate(DNN_Cuts):
    #print(str(cut))
    #top_mass_hist_ttbar_list[str(cut)].Print()
    top_mass_hist_ttbar_list[str(cut)].SetLineColor(colors[i])
    top_mass_hist_ttbar_list[str(cut)].Scale(1/top_mass_hist_ttbar_list[str(cut)].Integral())
    top_mass_hist_ttbar_list[str(cut)].Draw("hist;same")
legend.Draw()    

c3.Update()

c3.SaveAs("Plots/Correlation_Reco_top_mass_distribution"+year+"_"+lep+"."+"png")
c3.SaveAs("Plots/Correlation_Reco_top_mass_distribution"+year+"_"+lep+"."+"pdf")

