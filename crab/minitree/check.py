import ROOT
Entries_total = 0.0
for tree_no in range (1,47): 
        myfile1 = ROOT.TFile.Open("root://se01.indiacms.res.in//store/user/mikumar/RUN2_UL/MiniTree_condor/SIXTEEN_preVFP_v5/Mc/2J1T1_mu/Tbarchannel/tree_"+str(tree_no)+".root","READ")
        mytree1=myfile1.Get("Events")
        myhist = ROOT.TH1F("h1","h1",100,0,1000)
        mytree1.Project("h1","PV_npvs","Xsec_wgt*LHEWeightSign*puWeight*muSF*L1PreFiringWeight_Nom*bWeight*bJetPUJetID_SF*lJetPUJetID_SF")
        integral = myhist.Integral()
        print tree_no, " -----> ",integral
        Entries_total=Entries_total+integral

print "Sum = ", Entries_total
