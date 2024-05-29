import sys
import ROOT as rt
import numpy as np
import argparse as arg
import math

#print(args)
from Histogram_discribtions import get_histogram_distciption
from Overflow_N_Underflowbin import DrawOverflow_N_DrawUnderflow 

def get_histogram_with_DNN_cut(
                                lep="mu",
                                year="UL2017",
                                Variable="lntopMass",
                                channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L'],
                                MCcut = "Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF*(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                QCDcut = "(dR_bJet_lJet>0.4)*(mtwMass>50)*mtw_weight_50GeVCut",
                                Datacut = "(dR_bJet_lJet>0.4)*(mtwMass>50)",
                                DNNcut="(t_ch_CAsi>=0.7)",
                                Fpaths_DNN_score = {}, 
                                Fpaths_ori_with_weight = {}):

    print(type(DNNcut))
    #DNNcut="*(t_ch_CAsi>=0.3)*(t_ch_CAsi"+DNNcut+")"
    DNNcut="*"+DNNcut
    if(lep=="mu"):
            lepton = "Muon"
    elif(lep=="el"):
            lepton = "Electron"

    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    print(X_axies," ",Y_axies," ",lest_bin," ",max_bin," ",Num_bin)

    print
    print "############################   analising the event with the DNN cut applid ", DNNcut, "  ##################"
    print "lepton = ",lep
    print "Variable = ",Variable
    print
    # Initializing lists for histogram, TFile, TTree of Iso
    histo_corr_Array = []
    histo_wron_Array = []
    #intree = []
    rt.gROOT.cd()

    print Variable
    print "bining: ",Num_bin,", ",lest_bin,", ", max_bin

    if(Variable=="t_ch_CAsi"):
        BINS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0]
        print("redefine assymatic histogram bins ", BINS)
        histo_corr = rt.TH1F('histo_corr', Variable, len(BINS)-1,np.array(BINS))
        histo_wron = rt.TH1F('histo_wron', Variable, len(BINS)-1,np.array(BINS))
    else:
        histo_corr = rt.TH1F('histo_corr', Variable, Num_bin,lest_bin,max_bin)
        histo_wron = rt.TH1F('histo_wron', Variable, Num_bin,lest_bin,max_bin)

#histo_corr.Sumw2()
    MCcut_corr_Assig = MCcut+DNNcut+"*(bjet_partonFlavour*"+lepton+"Charge==5)"
    MCcut_wron_Assig = MCcut+DNNcut+"*(bjet_partonFlavour*"+lepton+"Charge!=5)"
    for channel in channels:
            print channel, "  ", Fpaths_ori_with_weight[channel]
            print channel, "  ", Fpaths_DNN_score[channel]
            histo_corr.Reset()
            histo_wron.Reset()
            
            #print filenamei
            MCFile = rt.TFile.Open(Fpaths_ori_with_weight[channel],'Read')	
            intree = MCFile.Get('Events')
            intree.AddFriend ("Events",Fpaths_DNN_score[channel])
        #intree[-1].Print()
            rt.gROOT.cd()
            print(MCcut_corr_Assig)
            intree.Project('histo_corr', Variable, MCcut_corr_Assig)
            intree.Project('histo_wron', Variable, MCcut_wron_Assig)
           
            #rt.gROOT.cd()

            #histo_corr = DrawOverflow_N_DrawUnderflow(histo_corr)
            #histo_wron = DrawOverflow_N_DrawUnderflow(histo_wron) 

        
            rt.gROOT.cd()
            histo_corr_Array.append(histo_corr.Clone())
            histo_wron_Array.append(histo_wron.Clone())
            histo_corr_Array[-1].SetName(channel)
            histo_wron_Array[-1].SetName(channel)
            histo_corr.Print()
            histo_wron.Print()
            
            del intree

    histo_corr_Array[0].GetXaxis().SetTitle(X_axies)
    histo_wron_Array[0].GetXaxis().SetTitle(X_axies)

    return histo_corr_Array,histo_wron_Array

if __name__ == '__main__':
   
        parser = arg.ArgumentParser(description='inputs discription')
        parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
        parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
        parser.add_argument('-v', '--var  ', dest='var', type=str, nargs=1, help="var [ lntopMass topMass t_ch_CAsi]")

        args = parser.parse_args()

        if (args.year == None or args.lepton == None):
                print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
                sys.exit (1)

        if args.year[0] not in ['UL2016preVFP', 'UL2016postVFP','UL2017','UL2018']:
                print('Error: Incorrect choice of year, use -h for help')
                exit()

        if args.lepton[0] not in ['el','mu']:
                print('Error: Incorrect choice of lepton, use -h for help')
                exit()

        lep = args.lepton[0]
        year= args.year[0]
        Variable = args.var[0]

        channels = ['Tchannel']#, 'Tbarchannel', 'tw_top', 'tw_antitop', 'Schannel',
           #'ttbar', 'WToLNu_0J', 'WToLNu_1J', 'WToLNu_2J', 'DYJetsToLL',
           #'WWTo1L1Nu2Q', 'WWTo2L2Nu', 'WZTo1L1Nu2Q', 'WZTo2L2Q', 'ZZTo2L2Q',
           #'QCD']
        
        for channel in channels:
           Fpaths_DNN_score[channel] = applydir+year+'_'+channel+'_Apply_all_'+lep+'.root' # prepare dict for the in put files
           if(year=="UL2016preVFP"): 
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_preVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2016postVFP"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SIXTEEN_postVFP/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2017"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"
           elif(year=="UL2018"):
               Fpaths_ori_with_weight[channel] = "/grid_mnt/t3storage3/mikumar/UL_Run2/EIGHTEEN/minitree/Mc/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root"    

        applydir = 'DNN_output_without_mtwCut/Apply_all/' 
        hists_corr,hists_wron = get_histogram_with_DNN_cut(lep,year,Variable)
        print(len(hists))
        for hist in hists:
             hist.Print()


