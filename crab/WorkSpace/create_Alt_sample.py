import ROOT as rt
import numpy as np
#import scipy.integrate as sp
import argparse as arg
import math
import sys 

from Histogram_discribtions import get_histogram_distciption 

def propagate_rate_uncertainity(hist, uncert):
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        if hist.GetBinContent(i) != 0:
            hist.SetBinError(i, hist.GetBinContent(i) * uncert * 0.01)

def alt_hypotheis_sample(lepton,Variable,MCcut,DNNcut_str,weight,weight_file,EvtWeight_Fpaths_Iso,Fpaths_DNN_apply,top_sig_DNNfitrescale,top_bkg_DNNfitrescale,top_sig_cons,top_bkg_cons):
    if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
    Variable,X_axies,Y_axies,lest_bin,max_bin,Num_bin = get_histogram_distciption(Variable)
    if(Variable=="lntopMass"): Variable= "TMath::Log(topMass)"
    channels_alt = ['Tchannel','Tbarchannel','tw_antitop', 'tw_top','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']
    
    
    
    Arr_Hist_Alt_with_genweight = []
    rt.gROOT.cd()
    histo_corr = rt.TH1F('histo_corr', Variable, Num_bin,lest_bin,max_bin)
    histo_corr_with_genweight = rt.TH1F('histo_corr_with_genweight', Variable, Num_bin,lest_bin,max_bin)
        
    Alt_sample_cut = MCcut+DNNcut_str+"*(bjet_partonFlavour*"+lepton+"Charge==5)"
    
    print(Alt_sample_cut)
    for Channel_alt in channels_alt:
        histo_corr.Reset()
        histo_corr_with_genweight.Reset()
        print(weight,Channel_alt)
        file = rt.TFile(weight_file[Channel_alt],"READ")
        tree = file.Get("Events")
        tree.AddFriend ("Events",EvtWeight_Fpaths_Iso[Channel_alt])
        tree.AddFriend ("Events",Fpaths_DNN_apply[Channel_alt])
        rt.gROOT.cd()
        tree.Project("histo_corr", Variable,Alt_sample_cut)
        histo_corr.Print()
        tree.Project("histo_corr_with_genweight", Variable,Alt_sample_cut+"*"+weight)
        histo_corr_with_genweight.Print()
        #weight apllited from ratio chenge the over all integra --> normalise the new histogram to the w/0 weight
        histo_corr_with_genweight.Scale(histo_corr.Integral()/histo_corr_with_genweight.Integral())
        # rescale to the normalization get from the DNN fits       
        """if(Channel_alt in ['Tchannel','Tbarchannel']):
            propagate_rate_uncertainity(histo_corr_with_genweight, top_sig_cons)
            histo_corr_with_genweight.Scale(top_sig_DNNfitrescale)
        else:
            propagate_rate_uncertainity(histo_corr_with_genweight, top_bkg_cons)
            histo_corr_with_genweight.Scale(top_bkg_DNNfitrescale)"""

        Arr_Hist_Alt_with_genweight.append(histo_corr_with_genweight.Clone())
        Arr_Hist_Alt_with_genweight[-1].SetName(Channel_alt)
        #Hist_Alt[-1].Print()
        #print(Hist_Alt)
    
    
    histo_corr_with_genweight.Reset()
    histo_corr_with_genweight_sig = Arr_Hist_Alt_with_genweight[0].Clone()
    histo_corr_with_genweight_sig.Add(Arr_Hist_Alt_with_genweight[1])
    
    histo_corr_with_genweight = Arr_Hist_Alt_with_genweight[2].Clone()
    for hist in Arr_Hist_Alt_with_genweight[3:]:
        histo_corr_with_genweight.Add(hist)

    # rescale to the normalization get from the DNN fits
    histo_corr_with_genweight_sig.Scale(top_sig_DNNfitrescale)
    propagate_rate_uncertainity(histo_corr_with_genweight_sig, top_sig_cons)
    histo_corr_with_genweight.Scale(top_bkg_DNNfitrescale)
    propagate_rate_uncertainity(histo_corr_with_genweight, top_bkg_cons)
    
    histo_corr_with_genweight.Add(histo_corr_with_genweight_sig)
    
    histo_corr_with_genweight.SetName("hist_"+weight)
    
    del  Arr_Hist_Alt_with_genweight
    
    return histo_corr_with_genweight
    
