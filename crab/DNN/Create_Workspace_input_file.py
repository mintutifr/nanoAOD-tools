import ROOT as rt
import numpy as np
import scipy.integrate as sp
import argparse as arg
import math

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")

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
Variable = args.var[0]

from Get_Nomi_histogram_Integral import Nomi_QCD_NoNQCD_Integral 

def get_histogram_with_DNN_cut(lep="mu",year="UL2017",Variable="lntopMass"):

    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"
    print(lepton)
    
    if(Variable=="lntopMass"):
            Variable="TMath::Log(topMass)"
            X_axies="ln(m_{Top})"
            Y_axies="Events/(20)"
            lest_bin=math.log(100.0)
            max_bin=math.log(400.0)
            Num_bin=15
    
    elif(Variable=="topMass"):
            X_axies="m_{Top}"
            Y_axies="Events/(20)"
            lest_bin=100.0
            max_bin=400.0
            Num_bin=15

    elif(Variable=="mtwMass"):
            X_axies="m_{T} (GeV)"
            Y_axies="Events/(10)"
            lest_bin=0.0
            max_bin=200.0
            Num_bin=20
    
    elif(Variable=="t_ch_CAsi+ttbar_CAsi"):
            X_axies="Signal+TopBkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
            
    elif(Variable=="t_ch_CAsi"):
            X_axies="Signal Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
      
    elif(Variable=="t_ch_WAsi"):
            X_axies="Signal Wrong Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="ttbar_CAsi"):
            X_axies="top bkg Corr. Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="ttbar_WAsi"):
            X_axies="top bkg Wrong Assign DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="EWK"):
            X_axies="EWK bkg DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    elif(Variable=="QCD"):
            X_axies="QCD bkg DNN Sore"
            Y_axies="Events/(0.01)"
            lest_bin=0.0
            max_bin=1.0
            Num_bin=100
    
    
    if(year == "ULpreVFP2016"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 10991.0
                   NonQCDScale_mtwFit = 231378.0
            if(lep=="el"):
                   QCDScale_mtwFit = 6892.0
                   NonQCDScale_mtwFit = 146947.0
    if(year == "ULpostVFP2016"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 11457.0
                   NonQCDScale_mtwFit = 209030.0
            if(lep=="el"):
                   QCDScale_mtwFit = 12848.0
                   NonQCDScale_mtwFit = 122089.0
    if(year == "UL2017"):
            if(lep=="mu"):
                   QCDScale_mtwFit = 30145.0
                   NonQCDScale_mtwFit = 472746.0
            if(lep=="el"):
                   QCDScale_mtwFit = 7509.0
                   NonQCDScale_mtwFit = 315426.0
    
    
    applydir = 'DNN_output_without_mtwCut/Apply_all/'
    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']
    MCcut = "Xsec_wgt*LHEWeightSign*puWeight*"+lep+"SF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)" 
    Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)"
    DNNcut="*(t_ch_CAsi>0.7)"
    
    Fpaths = {}
    EvtWeight_Fpaths_Iso = {}
    Data_AntiIso_Fpath = "" 
    for channel in channels:
            Fpaths[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
            if(year=="ULpreVFP2016"): 
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="ULpostVFP2016"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="UL2017"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
            elif(year=="UL2018"):
                EvtWeight_Fpaths_Iso[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
                if(channel=="QCD"): Data_AntiIso_Fpath =  "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T0/Minitree_Data"+year+"_2J1T0_"+lep+".root"
    
               
    #print EvtWeight_Fpaths_Iso
      
    # claculation of the scale QCD and NonQCD
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    NonQCD_Inte,QCD_Inte = Nomi_QCD_NoNQCD_Integral(lep,year,Variable,MCcut,Datacut,EvtWeight_Fpaths_Iso,Data_AntiIso_Fpath)
    if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)" 

    MCSF = NonQCDScale_mtwFit/NonQCD_Inte
    QCDSF = QCDScale_mtwFit/QCD_Inte
    print
    print "MCSF: ",MCSF," QCDSF: ",QCDSF

    #define histoframs 
    hs = {}
    WAssihs = {}
    infiles = {}
    intree = {}
    
    hist_tch_CAssig = rt.TH1F('hist_sig_CAssig', '', Num_bin, lest_bin, max_bin)
    hist_tch_WAssig = rt.TH1F('hist_sig_WAssig', '', Num_bin, lest_bin, max_bin)
    hist_ttbar_CAssig = rt.TH1F('hist_bkg_CAssig', '', Num_bin, lest_bin, max_bin)
    hist_ttbar_WAssig = rt.TH1F('hist_big_WAssig', '', Num_bin, lest_bin, max_bin)
    hist_EWK = rt.TH1F('hist_EWK', '', Num_bin, lest_bin, max_bin)
    hist_QCD = rt.TH1F('hist_QCD', '', Num_bin, lest_bin, max_bin)
    rt.gStyle.SetOptStat(0)
    
    hist_tch_CAssig.SetLineColor(rt.kRed);hist_tch_CAssig.SetLineWidth(2)
    hist_tch_CAssig.GetXaxis().SetTitle(X_axies)
    hist_tch_CAssig.GetYaxis().SetTitle(Y_axies)  
    
    hist_tch_WAssig.SetLineColor(rt.kBlue); hist_tch_WAssig.SetLineWidth(2)
    hist_ttbar_CAssig.SetLineColor(rt.kOrange-1); hist_ttbar_CAssig.SetLineWidth(2)
    hist_ttbar_WAssig.SetLineColor(rt.kCyan+1); hist_ttbar_WAssig.SetLineWidth(2)
    hist_EWK.SetLineColor(rt.kMagenta); hist_EWK.SetLineWidth(2)
    hist_QCD.SetLineColor(rt.kGray); hist_QCD.SetLineWidth(2)
    
    print    
    print "analysising tree withh DNN cut : ", DNNcut, " .. .. .. .... ..... ..."
    print 
    for channel in channels:
        if(channel=="QCD"):
                print channel, " ", Data_AntiIso_Fpath
                infiles[channel] = rt.TFile.Open(Data_AntiIso_Fpath, 'READ')
        else:
                print channel, " ", EvtWeight_Fpaths_Iso[channel]
                infiles[channel] = rt.TFile.Open(EvtWeight_Fpaths_Iso[channel], 'READ')
        intree[channel] = infiles[channel].Get('Events')
        intree[channel].AddFriend ("Events",Fpaths[channel])

        hs[channel] = rt.TH1F('hs' + channel, '', Num_bin, lest_bin, max_bin)
        WAssihs[channel] = rt.TH1F('temphs' + channel, '', Num_bin, lest_bin, max_bin)
        #rt.gROOT.cd()
    
        if(channel=='Tchannel' or channel=='Tbarchannel'):
            MCcut_corr_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)" 
            MCcut_wron_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"
            
            intree[channel].Project('hs' + channel, Variable,MCcut_corr_Assig)
            intree[channel].Project('temphs' + channel, Variable,MCcut_wron_Assig)
            hist_tch_CAssig.Add(hs[channel])
            hist_tch_WAssig.Add(WAssihs[channel])
            #hs[channel].Print()
        
        elif(channel=='tw_top'  or channel=='tw_antitop' or channel=='Schannel' or channel=='ttbar_SemiLeptonic' or channel=='ttbar_FullyLeptonic'):
            topbkg_corr_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge==5)"
            topbkg_wrog_Assig = MCcut+DNNcut+"*(Jet_partonFlavour[nbjet_sel]*"+lepton+"Charge!=5)"
                
            intree[channel].Project('hs' + channel, Variable,topbkg_corr_Assig)
            intree[channel].Project('temphs' + channel, Variable,topbkg_wrog_Assig)
            hist_ttbar_CAssig.Add(hs[channel])
            hist_ttbar_WAssig.Add(WAssihs[channel])
            #hs[channel].Print()

        elif(channel=='QCD'):
            intree[channel].Project('hs' + channel, Variable,Datacut+DNNcut)
            hist_QCD.Add(hs[channel])
            #hs[channel].Print()
        else:
            intree[channel].Project('hs' + channel, Variable,MCcut+DNNcut)
            hist_EWK.Add(hs[channel])
            #hs[channel].Print()
    
    print
    
    
         
    hist_tch_CAssig.Scale(MCSF)
    hist_tch_WAssig.Scale(MCSF)
    hist_ttbar_CAssig.Scale(MCSF)
    hist_ttbar_WAssig.Scale(MCSF)
    hist_EWK.Scale(MCSF)
    hist_QCD.Scale(QCDSF)
    
    hist_to_return = [] 

    hist_to_return.append(hist_tch_CAssig)
    hist_to_return.append(hist_tch_WAssig)
    hist_to_return.append(hist_ttbar_CAssig)
    hist_to_return.append(hist_ttbar_WAssig)
    hist_to_return.append(hist_EWK)
    hist_to_return.append(hist_QCD)

    return hist_to_return


if __name__ == "__main__":
    
    hists = get_histogram_with_DNN_cut(lep,year,Variable) 
    outfile = rt.TFile("Combine_Input_histograms.root","recreate")
    outfile.cd()
    Dir_mu = outfile.mkdir("mujets")
    Dir_mu.cd()

    hists[0].Write("top_sig_172p5")
    hists[1].Add(hists[2]); hists[1].Add(hists[3])
    hists[1].Write("top_bkg_172p5")
    hists[4].Write("EWK_bkg")
    hists[5].Write("QCD_DD")
        
    rt.gROOT.cd()
 
    outfile.cd()
    Dir_el = outfile.mkdir("eljets")
    Dir_el.cd()

    rt.gROOT.cd()

    outfile.Close()

    """c1 = rt.TCanvas('c1', '', 800, 800, 800, 800)
    rt.TGaxis.SetMaxDigits(3)
    c1.cd()
        
    pad1 = rt.TPad("pad1", "pad1",0.0,0.0,1.0,1.0)
    pad1.SetBottomMargin(0.089)
    pad1.SetTicky()
    pad1.SetTickx()
    pad1.SetRightMargin(0.143)
    pad1.Draw()
    pad1.cd()
    
    hists[0].Draw("hist")
    for hist in hists:
        hist.Draw("same;hist")

    
    legend = rt.TLegend(0.47193646, 0.65435, 0.70293552, 0.8826143) 
    legend.Clear()
    legend.SetBorderSize(1)
    legend.SetTextSize(0.04)
    legend.SetLineColor(0)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(0)
    legend.SetFillStyle(1001)
    
    legend.AddEntry(hists[0], "corr. Assi top sig", "l")
    legend.AddEntry(hists[1], "Worng Assi top sig", "l")
    legend.AddEntry(hists[2], "corr. Assi top bkg", "l")
    legend.AddEntry(hists[3], "Worng Assi top bkg", "l")
    legend.AddEntry(hists[4], "EWK bkg", "l")
    legend.AddEntry(hists[5], "QCD bkg", "l")
    
    legend.Draw("same")
    c1.Update()
    
    raw_input()"""
    
