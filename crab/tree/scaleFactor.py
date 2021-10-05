#!/usr/bin/env python
import os, sys
import ROOT

def elScaleFactor(pt, scEta, lead_Jet_pt, wp, syst,ID_Tight_fSFName,Trigger_Tight_fSFName,loose_fSFName,dataYear):

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

	    if(dataYear=='2017' and SF=="Trigger"):
		if(abs(lead_Jet_pt) > hSFIso[aa].GetYaxis().GetXmax()): lead_Jet_pt = hSFIso[aa].GetYaxis().GetXmax() - 0.01
	    else:
                if(scEta > hSFIso[aa].GetXaxis().GetXmax()): scEta = hSFIso[aa].GetXaxis().GetXmax() - 0.01
                if(scEta < hSFIso[aa].GetXaxis().GetXmin()): scEta = hSFIso[aa].GetXaxis().GetXmin() + 0.01

	    #print "scEta = ",scEta
	    if(dataYear=='2017' and SF=="Trigger"):
		if(pt > hSFIso[aa].GetXaxis().GetXmax()): pt = hSFIso[aa].GetXaxis().GetXmax() - 1.0
            else:
		if(pt > hSFIso[aa].GetYaxis().GetXmax()): pt = hSFIso[aa].GetYaxis().GetXmax() - 1.0

	    if(dataYear=='2017' and SF=="Trigger"):
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
        
    else:
	fSFName=loose_fSFName
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
    
    return elSF
def muonScaleFactor(filepath,pt,eta,iso,lumiTotal,syst,dataYear):
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
   
    if(dataYear=='2016'):
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
    if(dataYear=='2016'):
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
                fSFName=filepath+Period+"_"+SF+"_SF_0p06.root"
		#print  sf , " " ,fsfname , dirname , "/pt_abseta_ratio"
		#print  "hSF[",aa,"][",bb,"]"
                fSF[aa][bb]=ROOT.TFile.Open(fSFName,"Read")
                hSF[aa][bb]=fSF[aa][bb].Get(dirName+"/pt_abseta_ratio")
	if(iso>=0.2):
            if(dataYear=='2016'):dirName="MC_NUM_TightID_DEN_genTracks_PAR_pt_eta"
            for bb in range(0,len(period)):
                Period=period[bb]
		#print Period
                if(dataYear=='2016'):fSFName=filepath+Period+"_"+SF+".root"
		#print fSFName
		#print  "hSF[",aa,"][",bb,"]"
		if(dataYear=='2017'):fSFName=filepath+Period+"_SF_"+SF+".root"
                fSF[aa][bb]=ROOT.TFile.Open(fSFName,"Read")
		#print  SF , " " ,fSFName , dirName , "/pt_abseta_ratio"
                if(dataYear=='2016'):hSF[aa][bb]=fSF[aa][bb].Get(dirName+"/pt_abseta_ratio")
		if(dataYear=='2017'):hSF[aa][bb]=fSF[aa][bb].Get("NUM_TightID_DEN_genTracks")
    #print "-----------------------------------" 	         	
#Scale factor collection   
    for aa in range(0,len(sf)):

        SF=sf[aa]
        if(iso >=0.2 and SF!="ID"): continue
        for bb in range(0,len(period)):
            Period=period[bb]
            if(pt >= hSF[aa][bb].GetXaxis().GetXmax()): pt = hSF[aa][bb].GetXaxis().GetXmax() - 1.0
	    #print "SF = ", SF
	    #print "Period = ", Period
	    #print "pt = ",pt
	    #print "eta = ",eta
	    #print "hSF[",aa,"][",bb,"]"
            binX[aa][bb]=hSF[aa][bb].GetXaxis().FindBin(pt)
	    binY[aa][bb]=hSF[aa][bb].GetYaxis().FindBin(eta)
	    #print "histogram = ", hSF[aa][bb].GetName()
	    #print "binpt[",aa,"][",bb,"] = ",hSF[aa][bb].GetXaxis().FindBin(pt)
	    #print "bineta[",aa,"][",bb,"] = ",hSF[aa][bb].GetYaxis().FindBin(eta)
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

ID_Tight_el_fSFName = {	'2016' : 'ElectronSF/2016/ElectronSF_tightID.root',
		       	'2017' : 'ElectronSF/2017/2017_ElectronTight.root',
		 	'2018' : 'filepath'}

Trigger_Tight_el_fSFName = {'2016' : 'ElectronSF/2016/SF_HLT_Ele32_eta2p1.root',
			    '2017' : 'ElectronSF/2017/HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_OR_HLT_Ele35_WPTight_Gsf.root',
                            '2018' : 'filepath' }	

veto_el_fSFName	=      {'2016' : 'ElectronSF/2016/ElectronSF_vetoID.root',
                  	'2017' : 'ElectronSF/2017/2017_ElectronWPVeto_Fall17V2.root',
                  	'2018' : 'filepath'}

def create_elSF(dataYear,pt_, scEta_, lead_Jet_pt_, wp_, syst_):
    dataYear = str(dataYear)
    ID_Tight_el_fSFName_ = ID_Tight_el_fSFName[dataYear]
    Trigger_Tight_el_fSFName_ = Trigger_Tight_el_fSFName[dataYear]
    veto_el_fSFName_ = veto_el_fSFName[dataYear]
    elSF = elScaleFactor(pt_, scEta_, lead_Jet_pt_, wp_, syst_,ID_Tight_el_fSFName_,Trigger_Tight_el_fSFName_,veto_el_fSFName_,dataYear)
    return elSF	

mu_fpath = {'2016' : 'MuonSF/2016/EfficienciesAndSF_',
            '2017' : 'MuonSF/2017/EfficienciesAndSF_',
            '2018' : 'filepath'}


def create_muSF(dataYear,pt_,eta_,iso_,lumiTotal_,syst_):
	dataYear = str(dataYear)
        sf_fpath= mu_fpath[dataYear]
	#print sf_fpath
	muSF = muonScaleFactor(sf_fpath,pt_,eta_,iso_,lumiTotal_,syst_,dataYear) 
        return muSF	
#print "-------------------------------------------------------"
#print create_elSF('2017',300,None,50,'Tight','noSyst')
#create_muSF('2016',21.1176013947,0.6142578125,0.3,3485,'noSyst')
#print create_muSF('2016',50.1176013947,0.6142578125,0.03,3485,'noSyst')
#print "-------------------------------------------------------"			
