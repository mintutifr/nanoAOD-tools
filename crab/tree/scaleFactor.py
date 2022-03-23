#!/usr/bin/env python
import os, sys
import ROOT

def elScaleFactor(pt, scEta, lead_Jet_pt, wp, syst,ID_Tight_fSFName,Trigger_Tight_fSFName,veto_fSFName,dataYear):

    ROOT.gStyle.SetOptStat(0)
    elSF=1.0
    SF = ROOT.TString("") 

    if(wp == "Tight"):
	#print "wp = ",wp
        Xbin=[] 
	Ybin=[]
        hSFIso=[]
        fSFIso=[]
        sf=["ID","Trigger"]

        for aa in range(0,len(sf)):
            SF=sf[aa]
	    #print "SF = ",SF
            if(SF=="ID"): fSFName=ID_Tight_fSFName
            else: fSFName=Trigger_Tight_fSFName
            fSFIso.append(ROOT.TFile(fSFName,"Read"))
     		 
            if(SF=="ID"): hSFIso.append(fSFIso[aa].Get("EGamma_SF2D"))
            else: hSFIso.append(fSFIso[aa].Get("SF"))

	    if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"): #2017 has cross trigger with jet
		if(abs(lead_Jet_pt) > hSFIso[aa].GetYaxis().GetXmax()): lead_Jet_pt = hSFIso[aa].GetYaxis().GetXmax() - 0.01
	    else:
                if(scEta > hSFIso[aa].GetXaxis().GetXmax()): scEta = hSFIso[aa].GetXaxis().GetXmax() - 0.01
                if(scEta < hSFIso[aa].GetXaxis().GetXmin()): scEta = hSFIso[aa].GetXaxis().GetXmin() + 0.01

	    #print "scEta = ",scEta
	    if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"):
		if(pt > hSFIso[aa].GetXaxis().GetXmax()): pt = hSFIso[aa].GetXaxis().GetXmax() - 1.0
            else:
		if(pt > hSFIso[aa].GetYaxis().GetXmax()): pt = hSFIso[aa].GetYaxis().GetXmax() - 1.0

	    if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"):
		Xbin.append(hSFIso[aa].GetXaxis().FindBin(pt))
		Ybin.append(hSFIso[aa].GetYaxis().FindBin(abs(lead_Jet_pt)))
            else: 
		Xbin.append(hSFIso[aa].GetXaxis().FindBin(scEta)) 
	    	Ybin.append(hSFIso[aa].GetYaxis().FindBin(pt))
	#print "%s;%s;%s;%s;%s;%s" %(wp,syst,Xbin[0],Ybin[0],Xbin[1],Ybin[1])#"%s;%s;%s;%s;%s;%s" % (wp,syst,Xbin[0],Ybin[0],Xbin[1],Ybin[1]) 
	if(syst=="noSyst"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
        if(syst=="IDUp"): 
	    elSF = (hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) + hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0])) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
	    #print "%s;%s;%s;%s;%s;%s;%s%s"%(Xbin[0],Ybin[0],Xbin[1],Ybin[1],hSFIso[0].GetBinContent(Xbin[0],Ybin[0]),hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0]),hSFIso[1].GetBinContent(Xbin[1],Ybin[1]),elSF)
        if(syst=="IDDown"): elSF = ( hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) - hSFIso[0].GetBinErrorLow(Xbin[0],Ybin[0]) ) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
        if(syst=="TrigUp"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * ( hSFIso[1].GetBinContent(Xbin[1],Ybin[1]) + hSFIso[1].GetBinErrorUp(Xbin[1],Ybin[1]) )
        if(syst=="TrigDown"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * ( hSFIso[1].GetBinContent(Xbin[1],Ybin[1]) - hSFIso[1].GetBinErrorLow(Xbin[1],Ybin[1]) )
	#print "%s;%s;%s" % (syst,round(hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0]),8),round(hSFIso[1].GetBinErrorUp(Xbin[1],Ybin[1]),8))
        for aa in range(0,len(sf)):
            hSFIso[aa].Delete()
	    fSFIso[aa].Delete()
        
    elif(wp == "Veto"):
	fSFName=veto_fSFName
        fSFSB=ROOT.TFile.Open(fSFName,"Read")
        hSFSB=fSFSB.Get("EGamma_SF2D")

        if(scEta > hSFSB.GetXaxis().GetXmax()): scEta = hSFSB.GetXaxis().GetXmax() - 0.01
        if(scEta < hSFSB.GetXaxis().GetXmin()): scEta = hSFSB.GetXaxis().GetXmin() + 0.01
        if(pt > hSFSB.GetYaxis().GetXmax()): pt = hSFSB.GetYaxis().GetXmax() - 1.0
	#print "scEta = ",scEta
        binX=hSFSB.GetXaxis().FindBin(scEta)
	binY=hSFSB.GetYaxis().FindBin(pt)
	#print "Xbin = %s ; Ybin = %s" % (binX,binY)i
	#print hSFSB.GetBinError(binX,binY) ,';',hSFSB.GetBinErrorUp(binX,binY), ';', hSFSB.GetBinErrorLow(binX,binY)
        if(syst=="noSyst"): elSF = hSFSB.GetBinContent(binX,binY)
        if(syst=="IDUp"): elSF =  hSFSB.GetBinContent(binX,binY) + hSFSB.GetBinErrorUp(binX,binY)
        if(syst=="IDDown"): elSF = hSFSB.GetBinContent(binX,binY) - hSFSB.GetBinErrorLow(binX,binY)
        if(syst=="TrigUp" or syst=="TrigDown"): elSF=1.0
	#print "hSFSB.GetBinContent(binX,binY) = %s " % (hSFSB.GetBinContent(binX,binY))
        hSFSB.Delete() 
	fSFSB.Delete()
    else:
	elSF = -999
	print("WP is nither 'Tight' nor 'Veto'")    
    return elSF
def muonScaleFactor(files,pt,eta,iso,lumiTotal,syst,dataYear):
    eta = abs(eta)
    if(iso >0.06 and iso<0.2): return -999
    ROOT.gStyle.SetOptStat(0)
    muSF=1.0
    idSF=[] 
    idSFErrUp=[]
    idSFErrDown=[]
    isoSF=[] 
    isoSFErrUp=[] 
    isoSFErrDown=[] 
    trigSF=[] 
    trigSFErrUp=[]
    trigSFErrDown=[]

    if(eta >= 2.4): eta = 2.39
    if(eta <=0.0): eta = 0.01
   
    if(dataYear=='2016' or dataYear=='UL2016'):
    	binX=[[0,0],[0,0],[0,0]] 
    	binY=[[0,0],[0,0],[0,0]]
    if(dataYear=='2017'):
        binX=[[0,0,0],[0,0,0],[0,0,0]]
        binY=[[0,0,0],[0,0,0],[0,0,0]]
    lumi=[];
    if(dataYear=='2016'):
    	lumi.append((19.636*1000.0)/lumiTotal) 
    	lumi.append((16.219*1000.0)/lumiTotal)
    if(dataYear=='2017'):
        lumi.append((14.42*1000.0)/lumiTotal)
        lumi.append((13.56*1000.0)/lumiTotal)
	lumi.append((13.54*1000.0)/lumiTotal)

    period=[]
    if(dataYear=='2016'):
	period.append("BCDEF")
    	period.append("GH")
    if(dataYear=='UL2016'):
	period.append("HIPM_") #BCDEF
	period.append("") #GH
    if(dataYear=='2017'):
        period.append("BC")
        period.append("DE")
	period.append("F")

    sf=[]
    sf.append("ID")
    sf.append("ISO")
    if(dataYear=='2016'):sf.append("Trigger")
    if(dataYear=='2017'): sf.append("TRI")

    #TString fSFName, SF, Period, dirName;
    if(dataYear=='2016' or dataYear=='UL2016'):
    	fSF=[[0,0],[0,0],[0,0]]
    	hSF=[[0,0],[0,0],[0,0]]
    if(dataYear=='2017'):
        fSF=[[0,0,0],[0,0,0],[0,0,0]]
        hSF=[[0,0,0],[0,0,0],[0,0,0]]

#Histogram collection
    for aa in range(0,len(sf)):

        SF=sf[aa]
        if(iso >=0.2 and SF!="ID"): continue
	#print SF
        if(iso <=0.06):
            if(SF=="ID"): dirName="Tight2012_zIPCut_NUM_TightID_DEN_genTracks_PAR_pteta"
            if(SF=="ISO"): dirName="TightIso4_NUM_TightRelIso_DEN_TightIDandIPCut_PAR_pteta"
            if(SF=="Trigger"): dirName="IsoMu24_OR_IsoTkMu24_from_Tight2012_and_dBeta_0p06_pteta"
	    if(SF=='TRI'):dirName="IsoMu27_from_Tight2012_and_dBeta_0p06_pteta"

            for bb in range(0,len(period)):
                Period=period[bb]
		#print Period
		fSFName=filter(lambda x: Period+"_"+SF+"_SF_0p06.root" in x,files)[0] #filter function gave a list which has 1 file name always i.e [0]
                #fSFName=filepath+Period+"_"+SF+"_SF_0p06.root"
		#print  sf , " " ,fsfname , dirname , "/pt_abseta_ratio"
		#print  "hSF[",aa,"][",bb,"]"
                fSF[aa][bb]=ROOT.TFile.Open(fSFName,"Read")
                hSF[aa][bb]=fSF[aa][bb].Get(dirName+"/pt_abseta_ratio")
	if(iso>=0.2):
            if(dataYear=='2016'):dirName="MC_NUM_TightID_DEN_genTracks_PAR_pt_eta"

            for bb in range(0,len(period)):
                Period=period[bb]
		#print Period
                if(dataYear=='2016'):fSFName=filter(lambda x: Period+"_"+SF+".root" in x,files)[0] #filter function gave a list which has 1 file name always i.e [0]
                if(dataYear=='UL2016'):fSFName=filter(lambda x: "UL_"+Period+SF+".root" in x,files)[0] #filter function gave a list which has 1 file name always i.e [0]
		#if(dataYear=='2016'):fSFName=filepath+Period+"_"+SF+".root"
		#print  "hSF[",aa,"][",bb,"]"
		if(dataYear=='2017'):fSFName=filter(lambda x: Period+"_SF_"+SF+".root" in x,files)[0] #filter function gave a list which has 1 file name always i.e [0]
		#if(dataYear=='2017'):fSFName=filepath+Period+"_SF_"+SF+".root"
		print fSFName
		fSF[aa][bb]=ROOT.TFile.Open(fSFName,"Read")
		#print  SF , " " ,fSFName , dirName , "/pt_abseta_ratio"
                if(dataYear=='2016'):hSF[aa][bb]=fSF[aa][bb].Get(dirName+"/pt_abseta_ratio")
		if(dataYear=='UL2016'):hSF[aa][bb]=fSF[aa][bb].Get("NUM_TightID_DEN_TrackerMuons_abseta_pt")
		if(dataYear=='2017'):hSF[aa][bb]=fSF[aa][bb].Get("NUM_TightID_DEN_genTracks")
    #print "-----------------------------------" 	         	
#Scale factor collection   
    for aa in range(0,len(sf)):

        SF=sf[aa]
        if(iso >=0.2 and SF!="ID"): continue
        for bb in range(0,len(period)):
            Period=period[bb]
	    if(dataYear=='UL2016'):
            	if(pt >= hSF[aa][bb].GetYaxis().GetXmax()): pt = hSF[aa][bb].GetYaxis().GetXmax() - 1.0
	    else:
		 if(pt >= hSF[aa][bb].GetXaxis().GetXmax()): pt = hSF[aa][bb].GetrXaxis().GetXmax() - 1.0
	    #print "SF = ", SF
	    #print "Period = ", Period
	    #print "pt = ",pt
	    #print "eta = ",eta
	    #print "hSF[",aa,"][",bb,"]"
	    if(dataYear=='UL2016'):
            	binX[aa][bb]=hSF[aa][bb].GetYaxis().FindBin(pt)
	    	binY[aa][bb]=hSF[aa][bb].GetXaxis().FindBin(eta)
	    else:
		binX[aa][bb]=hSF[aa][bb].GetXaxis().FindBin(pt)
                binY[aa][bb]=hSF[aa][bb].GetYaxis().FindBin(eta)
	    #print "histogram = ", hSF[aa][bb].GetName()
	    print "binpt[",aa,"][",bb,"] for pt (", pt,") = ",hSF[aa][bb].GetYaxis().FindBin(pt)
	    print "bineta[",aa,"][",bb,"] for eta (",eta,") = ",hSF[aa][bb].GetXaxis().FindBin(eta)
            if(SF=="ID"):
		#print "hSF[",aa,"][",bb,"] = ", hSF[aa][bb].GetBinContent(binX[aa][bb],binY[aa][bb])
                idSF.append(hSF[aa][bb].GetBinContent(binX[aa][bb],binY[aa][bb]))
                idSFErrUp.append(hSF[aa][bb].GetBinErrorUp(binX[aa][bb],binY[aa][bb]))
                idSFErrDown.append(hSF[aa][bb].GetBinErrorLow(binX[aa][bb],binY[aa][bb]))
            if(SF=="ISO"):
                isoSF.append(hSF[aa][bb].GetBinContent(binX[aa][bb],binY[aa][bb]))
                isoSFErrUp.append(hSF[aa][bb].GetBinErrorUp(binX[aa][bb],binY[aa][bb]))
                isoSFErrDown.append(hSF[aa][bb].GetBinErrorLow(binX[aa][bb],binY[aa][bb]))

            if(SF=="Trigger" or SF=="TRI"):
                trigSF.append(hSF[aa][bb].GetBinContent(binX[aa][bb],binY[aa][bb]))
                trigSFErrUp.append(hSF[aa][bb].GetBinErrorUp(binX[aa][bb],binY[aa][bb]))
                trigSFErrDown.append(hSF[aa][bb].GetBinErrorLow(binX[aa][bb],binY[aa][bb]))
    #print "idSF = ",idSF
    #print "isoSF = ",isoSF
    #print "trigSF = ", trigSF
    #print "lumi = ",lumi
#Scale factor Evaluation

    if(iso >= 0.2 and dataYear=='2016'):
	#print "idSF[0] = ", idSF[0], "idSF[1] = ", idSF[1] 
        if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  + idSF[1]*lumi[1] 
        if(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  + (idSF[1] + idSFErrUp[1])*lumi[1]
        if(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  + (idSF[1] - idSFErrDown[1])*lumi[1]
        if(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0
    if(iso >= 0.2 and dataYear=='2017'):
        if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  + idSF[1]*lumi[1] + idSF[2]*lumi[2] 
        if(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  + (idSF[1] + idSFErrUp[1])*lumi[1] + (idSF[2] + idSFErrUp[2])*lumi[2]
        if(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  + (idSF[1] - idSFErrDown[1])*lumi[1] + (idSF[2] - idSFErrDown[2])*lumi[2]
        if(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0

    if(iso <=0.06 and dataYear=='2016'):
        if(syst=="noSyst"): muSF =  idSF[0]*isoSF[0]*trigSF[0]*lumi[0] + idSF[1]*isoSF[1]*trigSF[1]*lumi[1]
        if(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] + idSFErrUp[1])*isoSF[1]*trigSF[1]*lumi[1]
        if(syst=="IDDown"): muSF = (idSF[0] - idSFErrDown[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] - idSFErrDown[1])*isoSF[1]*trigSF[1]*lumi[1]
        if(syst=="IsoUp"): muSF = idSF[0]*(isoSF[0] + isoSFErrUp[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] + isoSFErrUp[1])*trigSF[1]*lumi[1]
        if(syst=="IsoDown"): muSF= idSF[0]*(isoSF[0] - isoSFErrDown[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] - isoSFErrDown[1])*trigSF[1]*lumi[1]
        if(syst=="TrigUp"): muSF= idSF[0]*isoSF[0]*(trigSF[0] + trigSFErrUp[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] + trigSFErrUp[1])*lumi[1]
        if(syst=="TrigDown"): muSF= idSF[0]*isoSF[0]*(trigSF[0] - trigSFErrDown[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] - trigSFErrDown[1])*lumi[1]

    if(iso <=0.06 and dataYear=='2017'):
        if(syst=="noSyst"): muSF =  idSF[0]*isoSF[0]*trigSF[0]*lumi[0] + idSF[1]*isoSF[1]*trigSF[1]*lumi[1]+idSF[2]*isoSF[2]*trigSF[2]*lumi[2]
        if(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] + idSFErrUp[1])*isoSF[1]*trigSF[1]*lumi[1]+(idSF[2] + idSFErrUp[2])*isoSF[2]*trigSF[2]*lumi[2]
        if(syst=="IDDown"): muSF = (idSF[0] - idSFErrDown[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] - idSFErrDown[1])*isoSF[1]*trigSF[1]*lumi[1]+(idSF[2] - idSFErrDown[2])*isoSF[2]*trigSF[2]*lumi[2]
        if(syst=="IsoUp"): muSF = idSF[0]*(isoSF[0] + isoSFErrUp[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] + isoSFErrUp[1])*trigSF[1]*lumi[1]+idSF[2]*(isoSF[2] + isoSFErrUp[2])*trigSF[2]*lumi[2]
        if(syst=="IsoDown"): muSF= idSF[0]*(isoSF[0] - isoSFErrDown[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] - isoSFErrDown[1])*trigSF[1]*lumi[1]+idSF[2]*(isoSF[2] - isoSFErrDown[2])*trigSF[2]*lumi[2]
        if(syst=="TrigUp"): muSF= idSF[0]*isoSF[0]*(trigSF[0] + trigSFErrUp[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] + trigSFErrUp[1])*lumi[1]+idSF[2]*isoSF[2]*(trigSF[2] + trigSFErrUp[2])*lumi[2]
        if(syst=="TrigDown"): muSF= idSF[0]*isoSF[0]*(trigSF[0] - trigSFErrDown[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] - trigSFErrDown[1])*lumi[1]+idSF[2]*isoSF[2]*(trigSF[2] - trigSFErrDown[2])*lumi[2]
    for aa in range(0,len(sf)):
        if(iso >=0.2 and aa!=0): continue
        for bb in range(0,len(period)):
            hSF[aa][bb].Delete()
            fSF[aa][bb].Delete()
    
    return muSF; 
    #canvas = ROOT.TCanvas(" canvas ")
    #canvas.cd()
    #print hSF[0][0].GetName()
    #hSF[0][0].Draw("colz")
    #canvas.Print("plots.pdf")

el_InFiles = {
		'2016':{
			'TightID': 'ElectronSF/2016postVFP/ElectronSF_tightID.root',
			'vetoID' : 'ElectronSF/2016postVFP/ElectronSF_vetoID.root',
			'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root'
		},

		'2017':{
			'TightID': 'ElectronSF/2017/2017_ElectronTight.root',
			'vetoID' : 'ElectronSF/2017/2017_ElectronWPVeto_Fall17V2.root',
			'TRI'    : 'ElectronSF/2017/HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_OR_HLT_Ele35_WPTight_Gsf.root' 
		},
		'UL2016preVFP':{
			'TightID': 'ElectronSF/2016preVFP/UL/egammaEffi.txt_Ele_Tight_preVFP_EGM2D.root',
			'vetoID' : 'ElectronSF/2016preVFP/UL/egammaEffi.txt_Ele_Veto_preVFP_EGM2D.root',
			'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root' #need to update
		},
		'UL2016postVFP':{
			'TightID': 'ElectronSF/2016postVFP/UL/egammaEffi.txt_Ele_Tight_postVFP_EGM2D.root',
			'vetoID' : 'ElectronSF/2016postVFP/UL/egammaEffi.txt_Ele_Veto_postVFP_EGM2D.root',
			'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root'  #need to update
		},
		'UL2017':{
                        'TightID': 'ElectronSF/2017/UL/egammaEffi.txt_EGM2D_Tight_UL17.root',
                        'vetoID' : 'ElectronSF/2017/UL/egammaEffi.txt_EGM2D_Veto_UL17.root',
                        'TRI'    : 'ElectronSF/2017/HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_OR_HLT_Ele35_WPTight_Gsf.root' #need to update
                },
		'UL2018':{
                        'TightID': 'ElectronSF/2018/UL/egammaEffi.txt_Ele_Tight_EGM2D.root',
                        'vetoID' : 'ElectronSF/2018/UL/egammaEffi.txt_Ele_Veto_EGM2D.root',
                        'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root' # need to update
                },
	     }
def create_elSF(dataYear,pt_, scEta_, lead_Jet_pt_, wp_, syst_):
    dataYear = str(dataYear)
    ID_Tight_el_fSFName_ = el_InFiles[dataYear]['TightID']
    Trigger_Tight_el_fSFName_ = el_InFiles[dataYear]['TRI']
    veto_el_fSFName_ = el_InFiles[dataYear]['vetoID']
    elSF = elScaleFactor(pt_, scEta_, lead_Jet_pt_, wp_, syst_,ID_Tight_el_fSFName_,Trigger_Tight_el_fSFName_,veto_el_fSFName_,dataYear)
    return elSF	

mu_InFiles = {'2016' : [
			'MuonSF/2016/EfficienciesAndSF_BCDEF_ID_SF_0p06.root',
			'MuonSF/2016/EfficienciesAndSF_GH_ID_SF_0p06.root',

			'MuonSF/2016/EfficienciesAndSF_BCDEF_ID.root',
			'MuonSF/2016/EfficienciesAndSF_GH_ID.root',

			'MuonSF/2016/EfficienciesAndSF_BCDEF_ISO_SF_0p06.root',
			'MuonSF/2016/EfficienciesAndSF_GH_ISO_SF_0p06.root',

			'MuonSF/2016/EfficienciesAndSF_BCDEF_Iso.root',
			'MuonSF/2016/EfficienciesAndSF_GH_Iso.root',

			'MuonSF/2016/EfficienciesAndSF_BCDEF_Trigger_SF_0p06.root',
			'MuonSF/2016/EfficienciesAndSF_GH_Trigger_SF_0p06.root',
		       ],
              '2017' : [
			'MuonSF/2017/EfficienciesAndSF_BC_ID_SF_0p06.root',   
			'MuonSF/2017/EfficienciesAndSF_DE_ID_SF_0p06.root',
			'MuonSF/2017/EfficienciesAndSF_F_ID_SF_0p06.root',
 
			'MuonSF/2017/EfficienciesAndSF_BC_SF_ID.root',
			'MuonSF/2017/EfficienciesAndSF_DE_SF_ID.root',
			'MuonSF/2017/EfficienciesAndSF_F_SF_ID.root',

			'MuonSF/2017/EfficienciesAndSF_BC_ISO_SF_0p06.root',
			'MuonSF/2017/EfficienciesAndSF_DE_ISO_SF_0p06.root',  
			'MuonSF/2017/EfficienciesAndSF_F_ISO_SF_0p06.root',

			'MuonSF/2017/EfficienciesAndSF_BC_SF_ISO.root',
			'MuonSF/2017/EfficienciesAndSF_DE_SF_ISO.root',
			'MuonSF/2017/EfficienciesAndSF_F_SF_ISO.root',

			'MuonSF/2017/EfficienciesAndSF_BC_TRI_SF_0p06.root',
			'MuonSF/2017/EfficienciesAndSF_F_TRI_SF_0p06.root'
			'MuonSF/2017/EfficienciesAndSF_DE_TRI_SF_0p06.root',
		       ],
              '2018' : 'filepath',

	      'UL2016':[
			'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root',
			'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root',

			'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ISO.root',
			'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root',
			'MuonSF/2016/UL/',
			]

}
def create_muSF(dataYear,pt_,eta_,iso_,lumiTotal_,syst_):
	dataYear = str(dataYear)
        sf_InFiles= mu_InFiles[dataYear]
	#print sf_InFiles
	muSF = muonScaleFactor(sf_InFiles,pt_,eta_,iso_,lumiTotal_,syst_,dataYear) 
        return muSF	
#print "-------------------------------------------------------"
#print create_elSF('UL2018',300,1.3,50,'Tight','noSyst')
#print create_elSF('UL2018',300,1.3,50,'Veto','noSyst')
#create_muSF('2016',21.1176013947,0.6142578125,0.3,3485,'noSyst')
#print create_muSF('UL2016',60.1176013947,1.0142578125,0.3,3485,'noSyst')
#print "-------------------------------------------------------"			
