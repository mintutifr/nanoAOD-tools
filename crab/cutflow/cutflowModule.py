#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from Mc_prob_cal_forBweght import *


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class cutflow(Module):
    def __init__(self,Total_Njets,BTag_Njets,Isolation,lepflavour,isMC,dataYear):
	self.writeHistFile=True
        self.Total_Njets = Total_Njets
        self.BTag_Njets = BTag_Njets
        self.Isolation = Isolation
	self.lepflavour = lepflavour
	self.isMC = isMC
	self.dataYear = dataYear
	lumi = {'2016' : 35882.5,'2017' : 41529.5,'2018' : None}
	if(self.isMC == True):
	    x_sec = 1350
            Lumi = lumi[self.dataYear]
	    NEvents = 7380341
            self.Xsec_wgt = (x_sec*Lumi)/NEvents
	self.Tight_b_tab_crite={
                	'2016' : 0.7527,
                	'2017' : 0.8001,
                	'2018' : None}
	if(self.lepflavour=="mu"):
	    self.trigger_selection={
                	'2016' : ['HLT_IsoMu24','HLT_IsoTkMu24'],
                	'2017' : ['HLT_IsoMu27'],
                	'2018' : None}
	    self.pt_Thes={
			'2016' : 26,
			'2017' : 30,
			'2018' : None}
	if(self.lepflavour=="el"):
            self.trigger_selection={
                        '2016' : ['HLT_Ele32_eta2p1_WPTight_Gsf'],
                        '2017' : ['HLT_Ele35_WPTight_Gsf','HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned'],
                        '2018' : None}
	    self.pt_Thes={
			'2016' : 35,
			'2017' : 37,
			'2018' : None}


    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

	self.Nocut_npvs=ROOT.TH1F('Nocut_npvs','Nocut_npvs', 100, 0, 1000)
       	self.trig_sel_npvs=ROOT.TH1F('trig_sel_npvs','trig_sel_npvs', 100, 0, 1000)
	self.tight_lep_sel_npvs=ROOT.TH1F('tight_lep_sel_npvs','tight_lep_sel_npvs', 100, 0, 1000)
	self.losse_lep_veto_npvs=ROOT.TH1F('losse_lep_veto_npvs','losse_lep_veto_npvs', 100, 0, 1000)
	self.sec_lep_veto_npvs=ROOT.TH1F('sec_lep_veto_npvs','sec_lep_veto_npvs',100,0,1000)
	self.jet_sel_npvs=ROOT.TH1F('jet_sel_npvs','jet_sel_npvs',100,0,1000)
	self.b_tag_jet_sel_npvs=ROOT.TH1F('b_tag_jet_sel_npvs','b_tag_jet_sel_npvs',100,0,1000)
 	self.addObject(self.Nocut_npvs)
	self.addObject(self.trig_sel_npvs)
	self.addObject(self.tight_lep_sel_npvs)
	self.addObject(self.losse_lep_veto_npvs)
	self.addObject(self.sec_lep_veto_npvs)
	self.addObject(self.jet_sel_npvs)
	self.addObject(self.b_tag_jet_sel_npvs)


    def analyze(self, event):
	try:
	     LHEWeightSign = getattr(event,'LHEWeight_originalXWGTUP')/abs(getattr(event,'LHEWeight_originalXWGTUP'))
	except:
             LHEWeightSign = 1
	if(self.isMC == True):
		PuWeight = getattr(event,'puWeight') 
	PreFireWeight = getattr(event,'L1PreFiringWeight_Nom')
	PV_npvs = getattr(event, "PV_npvs")
	if(self.isMC == True):self.Nocut_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
	else:self.Nocut_npvs.Fill(PV_npvs*PreFireWeight)

##################################
#trigger selection	--0--
###################################

	trigger=0;
 	if(self.lepflavour=="mu"):
            for value in self.trigger_selection[self.dataYear]: trigger=trigger+getattr(event,value)
	    if(trigger != 0):
	    	if(self.isMC == True):self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
		else:self.trig_sel_npvs.Fill(PV_npvs*PreFireWeight)
	    else:
	     	return True
	elif(self.lepflavour=="el"):
	    for value in self.trigger_selection[self.dataYear]: trigger=trigger+getattr(event,value)
	    if(trigger != 0):
		if(self.isMC == True):self.trig_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight) 
		else:self.trig_sel_npvs.Fill(PV_npvs*PreFireWeight)
	    else:
                return True
	#print "---------------------------------trigger selection      --0------------"
##################################
#one tight lepon selection-1-      
###################################
	muons = Collection(event, "Muon")
	electrons = Collection(event, "Electron")
	if(self.lepflavour=="mu"):
		muons_id=[]
		one_T_mu_ID = None	
		#print len(muons)
		for lep in muons:
		    #print self.Isolation, " ", lep.pt, " ", lep.eta , " ", lep.pfRelIso04_all ," " , lep.tightIdi
		    #print 'loose ID = ',lep.looseId, ' pt = ',lep.pt , ' eta = ', lep.eta, 'iso = ',lep.pfRelIso04_all #' phi =', lep.phi, ' mass = ',lep.mass
		    if((self.Isolation==1) and lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.06 and lep.tightId==1):
			muons_id.append(lep)
		    elif((self.Isolation==0) and lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.4 and lep.pfRelIso04_all>0.2 and lep.tightId==1): 
			muons_id.append(lep)
		    else: 
			continue
		if(len(muons_id)==1):
		    muSF = 0
		    if(self.isMC == True):
		         for muon in muons_id:
			    muSF=muon.SF_Iso
			    #print "muSF = ",muSF
		         self.tight_lep_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
	                 #print "muSF = ",muSF
		    else:self.tight_lep_sel_npvs.Fill(PV_npvs**PreFireWeight)
		else:
		     #print "ione tight muon selection-1- "
		     return True
	elif(self.lepflavour=="el"):
	    electron_id=[]
	    for lep in electrons:
		if((self.Isolation==True) and not(lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased==4 and not(abs(lep.EtaSC)<1.5660 and abs(lep.EtaSC)>1.4442) )): continue 
		elif((self.Isolation==False) and not(lep.pt>self.pt_Thes[self.dataYear] and abs(lep.eta)<2.1 and lep.cutBased!=4 and lep.cutBased>=1 and not(abs(lep.EtaSC)<1.5660 and abs(lep.EtaSC)>1.4442) )): continue
		if(abs(lep.EtaSC)<=1.479 and not(abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05)): continue
         	if(abs(lep.EtaSC)> 1.479 and not(abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)): continue
		electron_id.append(lep)
	    if (len(electron_id)==1):
		elSF=0
		if(self.isMC == True):
		    for electron in electron_id:
		    	if(self.Isolation==True):elSF = electron.SF_Iso 
		    	elif(self.Isolation==False):elSF = electron.SF_Veto
		    self.tight_lep_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
		if(self.isMC == False):
		    self.tight_lep_sel_npvs.Fill(PV_npvs*PreFireWeight)
  	    else:
		#print "one tight muon selection-1- "
                return True

	#print '---------------------------------one tight lep selection-1----------------'
	#print 'No. Of Electrons',len(electrons)
	    
###################################
#losse lepton veto --2--
###################################
	if(self.lepflavour=="mu"):
		muons_losse_size=0
		for lep in muons:
		    #print 'pt = %s eta = %s pfRelIso04_all = %s '%(lep.pt,lep.eta,lep.pfRelIso04_all)
		    if(lep==muons_id[0]): continue
		    if(lep.looseId==1 and lep.pt>10 and abs(lep.eta)<2.4 and lep.pfRelIso04_all<0.2): 
		    	#print 'pt = %s eta = %s pfRelIso04_all = %s '%(lep.pt,lep.eta,lep.pfRelIso04_all)
			muons_losse_size += 1
		    if(muons_losse_size>0): break
		if(muons_losse_size==0):
		    if(self.isMC == True):self.losse_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
		    if(self.isMC == False):self.losse_lep_veto_npvs.Fill(PV_npvs*PreFireWeight)
		else:
		    #print "losse muon veto --2--"	
		    return True
		#print 'muons_losse_size = ' ,muons_losse_size
	if(self.lepflavour=="el"):
	    electron_vid_size=0
	    for lep in electrons:
		if(lep==electron_id[0]): continue	
		if(abs(lep.EtaSC)<=1.479 and not(abs(lep.dz)< 0.10 and abs(lep.dxy)< 0.05)): continue
         	if(abs(lep.EtaSC)> 1.479 and not(abs(lep.dz)< 0.20 and abs(lep.dxy)< 0.10)): continue
		if(lep.cutBased>=1 and lep.pt>15 and abs(lep.eta)<2.5): electron_vid_size+=1
	    	if(electron_vid_size>0):
			#print "losse muon veto --2--"	
			break
	    if(electron_vid_size==0):
		if(self.isMC == True):self.losse_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
		if(self.isMC == False):self.losse_lep_veto_npvs.Fill(PV_npvs*PreFireWeight)
	    else:
		return True
	#print '---------------------------------------------losse lep veto --2---------------'
	#print 'No. Of Electrons = ',len(electrons)
	#for lep in electrons:
	    #print 'pt =%s eta =%s cutbased =%s EtaSC = %s dz =%s dxy =%s '%(lep.pt,lep.eta,lep.cutBased,lep.EtaSC,lep.dz,lep.dxy)

################################## 
#second lepton veto  --3--
#################################
	if(self.lepflavour=="mu"):
		electron_vid_size=0
		for lep in electrons:
		    if(lep.cutBased ==1 and lep.pt>15 and abs(lep.eta)<2.5  and (abs(lep.eta) < 1.4442 or abs(lep.eta) > 1.566)):
			 electron_vid_size += 1
		    if(electron_vid_size>0): break
		if(electron_vid_size==0):
		    if(self.isMC == True):self.sec_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
		    if(self.isMC == False):self.sec_lep_veto_npvs.Fill(PV_npvs*PreFireWeight)
		else:
		     #print "ione tight muon selection-1- "
		     return True

	if(self.lepflavour=="el"):
	     muons_losse_size=0
	     for muon in muons:
		if(muon.looseId==1 and muon.pt>10 and abs(muon.eta)<2.4 and muon.pfRelIso04_all<0.2): muons_losse_size+=1
		if(muons_losse_size>0): break
	     if(muons_losse_size==0):
             	if(self.isMC == True):self.sec_lep_veto_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
		if(self.isMC == False):self.sec_lep_veto_npvs.Fill(PV_npvs*PreFireWeight)
	     else:
		#print "second lepton veto  --3--"
             	return True
	#print 'No. Of Muons = ',len(muons)
	#for lep in muons:
	 #   print 'pt =%s eta =%s looseId =%s pfRelIso04 =%s '%(lep.pt,lep.eta,lep.looseId,lep.pfRelIso04_all)
	#for lep in electrons:
	#     print 'pt =%s eta =%s cutbased =%s '%(lep.pt,lep.eta,lep.cutBased)


	#print '--------------------------------------------------another lepton veto  --3------------'
##################################
#jet selection  --4--
##################################  
 	jet_id = []
	btagjet_id = []
	muon4v = ROOT.TLorentzVector(0.,0.,0.,0.)
	electron4v = ROOT.TLorentzVector(0.,0.,0.,0.)
	if(self.lepflavour=="mu"):
	    for muon in muons_id:
            	muon4v=muon.p4()
	if(self.lepflavour=="el"):
	    for electron in electron_id:
		electron4v = electron.p4()
        jets = Collection(event, "Jet")
	#print(len(jets))
	for jet in jets:
	    #print jet.jetId
	    lossepF=0
	    if(jet.pt>40 and abs(jet.eta)<4.7 and jet.jetId!=0):
		lossepF +=1 
		#print "jet.pt = ",jet.pt," jet.eta = ",abs(jet.eta), " jet.jetId = ",jet.jetId, "lossepF = ", lossepF
	    else: continue
	    njet4v = ROOT.TLorentzVector(0.,0.,0.,0.)	
	    njet4v = jet.p4()
	    if(self.lepflavour=="mu" and lossepF==1 and muon4v.DeltaR(njet4v)>0.4):
		jet_id.append(jet)#and muon4v.DeltaR(njet4v)>0.4):jet_id.append(jet)
		#print "jet.btagDeepB = ",jet.btagDeepB," jet.eta = ",abs(jet.eta)
		print "deltaR =",muon4v.DeltaR(njet4v)," jetdeltaRiso = ",jet.dR_Ljet_Isomu," jetdeltaRantiiso = ",jet.dR_Ljet_AntiIsomu
	    	#print "Jet Pt =%s ; Jet eta =%s ; jet ID =%s ;DeltaR =%s" % (jet.pt,jet.eta,jet.jetId,muon4v.DeltaR(njet4v)) 
	    elif(self.lepflavour=="el" and lossepF==1 and electron4v.DeltaR(njet4v)>0.4): jet_id.append(jet)
	    else: continue
	  #  print "jet_id = ",jet_id
	    if(abs(jet.eta)<2.4 and jet.btagDeepB>self.Tight_b_tab_crite[self.dataYear] ): 
		btagjet_id.append(jet)
	    #if(abs(jet.eta)<2.4): btagjet_id.append(jet)
	 	print "btagJet_id = ", btagjet_id
	if(len(jet_id)==self.Total_Njets):
           if(self.lepflavour=="mu" and self.isMC == True): self.jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF)
           elif(self.lepflavour=="el" and self.isMC == True): self.jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF)
	   elif(self.lepflavour=="mu" and self.isMC == False): self.jet_sel_npvs.Fill(PV_npvs*PreFireWeight)
	   elif(self.lepflavour=="el" and self.isMC == False): self.jet_sel_npvs.Fill(PV_npvs*PreFireWeight)
	else:
	    #print "jet selection  --4--"
	    return True
	#print '---------------------------------------------------------------jet selection  --4--'
	#print 'No. Of jets = ',len(jets)
	#for jet in jets:
	    #print 'pt =%s eta =%s jetId =%s deepCSV =%s '%(jet.pt,jet.eta,jet.jetId,jet.btagDeepB)


#################################
#b tag jet  --5--
################################## 
		
	if(len(btagjet_id)==self.BTag_Njets):
	    if(self.isMC == True):
		#print  len(btagjet_id)," ",self.BTag_Njets	
		###################################   fixed working point b weight calculation   ###################
		"""
		p_mc_central_T = 1
		p_data_central_T = 1
		for jet in btagjet_id:
		    [P_MC_term_central_T,P_Data_term_central_T] = Probability(jet.pt,jet.eta,jet.btagSF_deepcsv_T,0,0,'T',jet.btagDeepB,jet.hadronFlavour,'central',self.dataYear)
		    p_mc_central_T = p_mc_central_T*P_MC_term_central_T
		    p_data_central_T = p_data_central_T*P_Data_term_central_T
		bweight_central_T = p_data_central_T/p_mc_central_T"""

		###################################   shape variation b weight calculation   ###################
		bweight = Probability_2("Central",jet_id)	
		
		if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*muSF*bweight)
		if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs,(self.Xsec_wgt)*LHEWeightSign*PuWeight*PreFireWeight*elSF*bweight)
	    if(self.isMC == False):
		if(self.lepflavour=="mu"): self.b_tag_jet_sel_npvs.Fill(PV_npvs*PreFireWeight)
		if(self.lepflavour=="el"): self.b_tag_jet_sel_npvs.Fill(PV_npvs*PreFireWeight)
        else:
	    #print "b tag jet  --5--"
	    return True				
	print '---------------------------------------------------------------------------b tag jet  --5--'
	#print(getattr(event,'event'))

        return True
cutflowModuleConstr_2J1T1_mu_mc_2016 =  lambda : cutflow(2,1,True,"mu",True,'2016')
cutflowModuleConstr_2J1T1_mu_data_2016 =  lambda : cutflow(2,1,True,"mu",False,'2016')
cutflowModuleConstr_2J1T1_el_mc_2016 =  lambda : cutflow(2,1,True,"el",True,'2016')
cutflowModuleConstr_2J1T1_el_data_2016 =  lambda : cutflow(2,1,True,"el",False,'2016')

cutflowModuleConstr_2J1T0_mu_mc_2016 =  lambda : cutflow(2,1,False,"mu",True,'2016')
cutflowModuleConstr_2J1T0_mu_data_2016 =  lambda : cutflow(2,1,False,"mu",False,'2016')
cutflowModuleConstr_2J1T0_el_mc_2016 =  lambda : cutflow(2,1,False,"el",True,'2016')
cutflowModuleConstr_2J1T0_el_data_2016 =  lambda : cutflow(2,1,False,"el",False,'2016')

cutflowModuleConstr_2J1T1_mu_mc_2017 =  lambda : cutflow(2,1,True,"mu",True,'2017')
cutflowModuleConstr_2J1T1_mu_data_2017 =  lambda : cutflow(2,1,True,"mu",False,'2017')
cutflowModuleConstr_2J1T1_el_mc_2017 =  lambda : cutflow(2,1,True,"el",True,'2017')
cutflowModuleConstr_2J1T1_el_data_2017 =  lambda : cutflow(2,1,True,"el",False,'2017')

cutflowModuleConstr_2J1T0_mu_mc_2017 =  lambda : cutflow(2,1,False,"mu",True,'2017')
cutflowModuleConstr_2J1T0_mu_data_2017 =  lambda : cutflow(2,1,False,"mu",False,'2017')
cutflowModuleConstr_2J1T0_el_mc_2017 =  lambda : cutflow(2,1,False,"el",True,'2017')
cutflowModuleConstr_2J1T0_el_data_2017 =  lambda : cutflow(2,1,False,"el",False,'2017')

cutflowModuleConstr_2J0T1_mu_mc_2016 =  lambda : cutflow(2,0,True,"mu",True,'2016')
cutflowModuleConstr_2J0T0_mu_mc_2016 =  lambda : cutflow(2,0,False,"mu",True,'2016')
