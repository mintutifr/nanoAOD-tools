from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
from Propagate_rate_Uncertainity import propagate_rate_uncertainity
def get_Weight_sys_top(lep,year,Variable,channels_weight_sys,MCcut,DNNcut,hist_sys_name,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,top_sig_cons,top_bkg_cons,Fpaths_sys_samples=None):
    QCDcut=""
    Datacut=""
    if(Fpaths_sys_samples==None):
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels = channels_weight_sys,
            MCcut = MCcut ,
            QCDcut = QCDcut, 
            Datacut = Datacut, 
            DNNcut = DNNcut,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )
        if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
    else:
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels = channels_weight_sys,
            MCcut = MCcut ,
            QCDcut = QCDcut, 
            Datacut = Datacut, 
            DNNcut = DNNcut,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )
    hist_corr_assig_weight_sys = {}
    hist_wron_assig_weight_sys = {}
    for channel_no,channel in enumerate(channels_weight_sys):
        hist_corr_assig_weight_sys[channel] = hists_corr_weight_sys[channel_no].Clone()
        hist_wron_assig_weight_sys[channel] = hists_wron_weight_sys[channel_no].Clone()
    del hists_corr_weight_sys
    del hists_wron_weight_sys

    top_sig_weight_sys = hist_corr_assig_weight_sys["Tchannel"].Clone(); top_sig_weight_sys.Add(hist_corr_assig_weight_sys["Tbarchannel"]);

    top_bkg_weight_sys = hist_wron_assig_weight_sys["Tchannel"].Clone(); top_bkg_weight_sys.Add(hist_wron_assig_weight_sys["Tbarchannel"]);

    propagate_rate_uncertainity(top_sig_weight_sys, top_sig_cons)
    propagate_rate_uncertainity(top_bkg_weight_sys, top_sig_cons)

    top_bkg_weight_sys_corr = hist_corr_assig_weight_sys['tw_top'].Clone();
    top_bkg_weight_sys_wron = hist_wron_assig_weight_sys['tw_top'].Clone();
    for channel in ['tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']:
        top_bkg_weight_sys_corr.Add(hist_corr_assig_weight_sys[channel])
        top_bkg_weight_sys_wron.Add(hist_wron_assig_weight_sys[channel])

    propagate_rate_uncertainity(top_bkg_weight_sys_corr, top_bkg_cons)
    propagate_rate_uncertainity(top_bkg_weight_sys_wron, top_bkg_cons)

    top_sig_weight_sys.Add(top_bkg_weight_sys_corr)
    top_bkg_weight_sys.Add(top_bkg_weight_sys_wron)

    top_sig_weight_sys.Print()
    top_bkg_weight_sys.Print()

    return top_sig_weight_sys,top_bkg_weight_sys