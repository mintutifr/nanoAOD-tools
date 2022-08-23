#!/usr/bin/env python
import os, sys
import ROOT 
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *
class NanoGenModule(Module):
    def __init__(self,datayear):
	self.writeHistFile=True
	self.datayear = datayear
    #def beginJob(self,histFile=None,histDirName=None):
	#Module.beginJob(self,histFile,histDirName)
	#self.pt_hist = ROOT.TH1D("pt_hist","pt_hist",20,0.0,400)
	#self.eta_hist = ROOT.TH1D("eta_hist","eta_hist",20,0.0,5.0)
	#self.top_mass_hist = ROOT.TH1D("top_mass","top_mass",52,166.0,179.0)
	#self.addObject(self.pt_hist)
	#self.addObject(self.eta_hist)
	#self.addObject(self.top_mass_hist)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("top_mass_gen", "F")
        self.out.branch("top_mass_gen_reco", "F")
        self.out.branch("top_pt_gen", "F")
        self.out.branch("top_pt_gen_reco", "F")
        self.out.branch("top_eta_gen", "F")
        self.out.branch("top_eta_gen_reco", "F")
        self.out.branch("top_phi_gen", "F")
        self.out.branch("top_phi_gen_reco", "F")
	self.out.branch("tau_to_el_flag", "F")
	self.out.branch("tau_to_mu_flag", "F")
        self.out.branch("el_flag", "F")
        self.out.branch("mu_flag", "F")

        self.out.branch("lepton_pt_gen", "F")
        self.out.branch("lepton_eta_gen", "F")
        self.out.branch("lepton_phi_gen", "F")

        self.out.branch("neutrino_pt_gen", "F")
        self.out.branch("neutrino_eta_gen", "F")
        self.out.branch("neutrino_phi_gen", "F")
        self.out.branch("neutrino_el_flag", "F")
        self.out.branch("neutrino_mu_flag", "F")

        self.out.branch("W_mass_gen", "F")
        self.out.branch("W_mass_gen_reco", "F")
        self.out.branch("W_pt_gen", "F")
        self.out.branch("W_pt_gen_reco", "F")
        self.out.branch("W_eta_gen", "F")
        self.out.branch("W_eta_gen_reco", "F")
        self.out.branch("W_phi_gen", "F")
        self.out.branch("W_phi_gen_reco", "F")
        self.out.branch("W_to_el_flag", "F")
        self.out.branch("W_to_mu_flag", "F")


        self.out.branch("bjet_pt_gen", "F")
        self.out.branch("bjet_eta_gen", "F")
        self.out.branch("bjet_phi_gen", "F")
        self.out.branch("bjet_el_flag", "F")
        self.out.branch("bjet_mu_flag", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
	Genparts = Collection(event,"GenPart")
	top_from_bquark = []
	top_from_lepton = []
	top_from_nuetrino = []
	b_quark_id = None
	lepton_id = None
	nuetrino_id = None
    	tau_to_el_flag = False
	tau_to_mu_flag = False
        el_flag = False
        mu_flag = False
        neutrino_el_flag = False
        neutrino_mu_flag = False

        lepton4v_gen = ROOT.TLorentzVector()
        Nu4v_gen = ROOT.TLorentzVector()
        bJet4v_gen = ROOT.TLorentzVector()
        w4v_gen_reco = ROOT.TLorentzVector()
        top4v_gen_reco = ROOT.TLorentzVector()

	for genpart in Genparts:
	    #if((abs(genpart.pdgId)==5)):
	    #tau_to_el_flag = False
	    #tau_to_mu_flag = False
	    if((abs(genpart.pdgId)==11 or abs(genpart.pdgId)==13) or abs(genpart.pdgId)==5 or (abs(genpart.pdgId)==12 or abs(genpart.pdgId)==14)):
                motheridx =  genpart.genPartIdxMother
                PDG = genpart.pdgId
                final_state_GenPart_Flag = Binary_flags(genpart.statusFlags)
                motherPDG,Gmotheridx,GmotherPDG = findMother(motheridx,Genparts)
	 	#print(PDG,motheridx,motherPDG,Gmotheridx,GmotherPDG)	
	 	#print(PDG,motherPDG,GmotherPDG)
	 	#if((abs(GmotherPDG)==11 or abs(GmotherPDG)==13  or abs(GmotherPDG)==24)):
	 		#print "%s  flag : %s : "%(genpart.pdgId,genpart.statusFlags),
                #PrintTrueflags(Binary_flags(genpart.statusFlags))
	 	#print
	 		#print(motherPDG,Gmotheridx,GmotherPDG)
                if(abs(PDG)==5):
                    #print 
	 	    #print abs(PDG)," -> ",
                    bJet4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,4.18)
	 	    if(abs(motherPDG)!=6):
	 	        #print abs(motherPDG)," -> ",
	 	        #printonce = False
	 	    	while (abs(GmotherPDG)!=6):
                             if(motherPDG == GmotherPDG or GmotherPDG ==-1 or motherPDG ==-1 or Gmotheridx==-1): # motherPDG == GmotherPDG this can make sure that we this is the case then we will find the Gmother again in gen part loop  
                                #print("break while loop @ motherPDG = %s, GmotherPDG = %s Gmotheridx = %s" % (motherPDG, GmotherPDG,Gmotheridx))
                                break
                             #if(printonce==False): 
                                #print abs(GmotherPDG)," --> ",
                                #printonce = True
	                     PDG = motherPDG
	 	 	     motheridx = Gmotheridx
	 	 	     motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts)
	 	 	     #print abs(GmotherPDG)," ---> ",
	 	 	     #print("-----> ",motherPDG,Gmotheridx,GmotherPDG)
	 	    ## ----- it is possible the b quark (5) ahs it mother as top (6)
	            if(abs(motherPDG)==6):
	 	 	#print abs(motherPDG)," --> ",   
	 	 	top_from_bquark.append(motheridx)
                        flag_for_b = final_state_GenPart_Flag
	 	    elif(abs(motherPDG)==abs(PDG) and abs(GmotherPDG)==6 and len(top_from_bquark)!=0):
	 	 	#print abs(GmotherPDG)," ---> ",
	 	 	if(top_from_bquark[0]!=abs(Gmotheridx)):
	 	 	    top_from_bquark.append(Gmotheridx)
                            flag_for_b = final_state_GenPart_Flag
	 	 	    #print "Gmother is top ; len(top_from_bquark) was !=0"		
	 	    elif(abs(motherPDG)==abs(PDG) and abs(GmotherPDG)==6 and len(top_from_bquark)==0):
	 	 	#print abs(GmotherPDG)," ----> ",
	 	 	top_from_bquark.append(Gmotheridx)
                        flag_for_b = final_state_GenPart_Flag
	 	        #print "top_from_bquark : ",top_from_bquark
                
	 	elif((abs(PDG)==11 or abs(PDG)==13) and (isflagTrue(final_state_GenPart_Flag,"fromHardProcess")==True or isflagTrue(final_state_GenPart_Flag,"isDirectHardProcessTauDecayProduct")==True)):
	 	    #lepton_id = genpart.genPartIdx
                    #print
                    #print PDG," -> ", motherPDG," -> ",
                    #print_once = FalseElectron
                    if(abs(PDG)==13): 
                        lepton4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.1056583745)
                        mu_flag = True
                    if(abs(PDG)==11): 
                        lepton4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.0005109989461)
                        el_flag = True
	 	    if( abs(motherPDG)==24 or abs(motherPDG)==11 or abs(motherPDG)==13 or abs(motherPDG)==15):	
	 	    	while ((motherPDG == GmotherPDG and GmotherPDG !=-1 and motherPDG !=-1 and Gmotheridx!=-1 and abs(GmotherPDG)!=6) or ( (abs(motherPDG)==24 or abs(motherPDG)==15) and abs(GmotherPDG)!=6 and GmotherPDG !=-1)):
                             #if(print_once==False):
                                #print GmotherPDG," --> ",
                                #print_once=True
	 	 	     if(abs(motherPDG)==15 and abs(PDG)==11 ): tau_to_el_flag = True
	 	 	     if(abs(motherPDG)==15 and abs(PDG)==13 ): tau_to_mu_flag = True
                                
	 	 	     PDG = motherPDG
	 	 	     motheridx = Gmotheridx
	 	 	     motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts)
	 	 	     #print GmotherPDG," ---> ",
	 	 	     #print("-----> ",motherPDG,Gmotheridx,GmotherPDG)	
                        #print
	 	    ## ---- it is not posible to be top as mother because in case of lepton we find w(24) as mother atleast and top(6) as Grandmother 
	 	        if(abs(GmotherPDG)==6): # we dont want to add the top quarks which give lepton in final state which leptons mother is not W boson
                            #PrintTrueflags(final_state_GenPart_Flag)
                            #print(isflagTrue(final_state_GenPart_Flag,"fromHardProcess"))
                            top_from_lepton.append(Gmotheridx)
                            #print "top_from_lepton : ",top_from_lepton
                                
	 	elif((abs(PDG)==12 or abs(PDG)==14) and (isflagTrue(final_state_GenPart_Flag,"fromHardProcess")==True or isflagTrue(final_state_GenPart_Flag,"isDirectHardProcessTauDecayProduct")==True)):                                                  
                    #nuetrino_id = genpart.genPartIdx
                    #print
                    #print PDG," -> ", motherPDG," -> ",
                    #print_once = False
                    Nu4v_gen.SetPtEtaPhiM(genpart.pt,genpart.eta,genpart.phi,0.0)
                    neutrino_pt_gen = genpart.pt
                    neutrino_eta_gen = genpart.eta
                    neutrino_phi_gen = genpart.phi
                    neutrino_el_flag = True if(abs(PDG)==12)  else False
                    neutrino_mu_flag = True if(abs(PDG)==14)  else False

                    if( abs(motherPDG)==24  or abs(motherPDG)==15):
                        while ((motherPDG == GmotherPDG and GmotherPDG !=-1 and motherPDG !=-1 and Gmotheridx!=-1 and abs(GmotherPDG)!=6) or ( (abs(motherPDG)==24 or abs(motherPDG)==15) and abs(GmotherPDG)!=6 and GmotherPDG !=-1)):
                             #if(print_once==False):
                                #print GmotherPDG," --> ",
                                #print_once=True
                             PDG = motherPDG
                             motheridx = Gmotheridx
                             if(abs(PDG) == 24): WMotheridx = motheridx
                             motherPDG,Gmotheridx,GmotherPDG = findMother(Gmotheridx,Genparts)
                             #print GmotherPDG," ---> ",   
                             #print("-----> ",motherPDG,Gmotheridx,GmotherPDG)
                        #print   
                    ## ---- it is not posible to be top as mother because in case of lepton we find w(24) as mother atleast and top(6) as Grandmother 
                        if(abs(GmotherPDG)==6): #we dont want to add the top quarks which give lepton in final state which leptons mother is not W boson
                             #print(isflagTrue(final_state_GenPart_Flag,"fromHardProcess"))
                             #PrintTrueflags(final_state_GenPart_Flag)
                             top_from_nuetrino.append(Gmotheridx)
                             #print "Gmother is top "  
                             #print "top_from_nuetrino : ",top_from_nuetrino
	#if(len(top_from_lepton)!=1 and len(top_from_bquark)!=1 and len(top_from_nuetrino)!=1):
	    #print "top_from_lepton : %s top_from_bquark : %s event = %s"%(top_from_lepton,top_from_bquark,getattr(event,'event'))

	if(len(top_from_lepton)==1 and len(top_from_bquark)==1): 
	    if(top_from_lepton[0]==top_from_bquark[0] and top_from_lepton[0]==top_from_nuetrino[0]):
	 	#print "top found with index = ",top_from_lepton[0]
                w4v_gen_reco = lepton4v_gen + Nu4v_gen         
                top4v_gen_reco = w4v_gen_reco + bJet4v_gen

                self.out.fillBranch("W_mass_gen_reco", w4v_gen_reco.M())
                self.out.fillBranch("W_pt_gen_reco", w4v_gen_reco.Pt())
                self.out.fillBranch("W_eta_gen_reco", w4v_gen_reco.Eta())
                self.out.fillBranch("W_phi_gen_reco", w4v_gen_reco.Phi())

                self.out.fillBranch("top_mass_gen_reco", top4v_gen_reco.M())
                self.out.fillBranch("top_pt_gen_reco", top4v_gen_reco.Pt())
                self.out.fillBranch("top_eta_gen_reco", top4v_gen_reco.Eta())
                self.out.fillBranch("top_phi_gen_reco", top4v_gen_reco.Phi())

	 	ID=0
	 	for genpart in Genparts:
                    if((abs(genpart.pdgId)==24 and abs(genpart.genPartIdxMother)==WMotheridx) ):
                        self.out.fillBranch("W_mass_gen", genpart.mass)
                        self.out.fillBranch("W_pt_gen", genpart.pt)
                        self.out.fillBranch("W_eta_gen", genpart.eta)
                        self.out.fillBranch("W_phi_gen", genpart.phi)

	 	    if(ID==top_from_lepton[0]):
                        #print genpart.statusFlags
                        #PrintTrueflags(Binary_flags(genpart.statusFlags))
	 	 	if(tau_to_el_flag):self.out.fillBranch("tau_to_el_flag", 1.0)
	       	       	else:self.out.fillBranch("tau_to_el_flag", 0.0)
	 	 	if(tau_to_mu_flag):self.out.fillBranch("tau_to_mu_flag", 1.0)
                        else:self.out.fillBranch("tau_to_mu_flag", 0.0)
                        if(el_flag):self.out.fillBranch("el_flag", 1.0)
                        else:self.out.fillBranch("el_flag", 0.0)
                        if(mu_flag):self.out.fillBranch("mu_flag", 1.0)
                        else:self.out.fillBranch("mu_flag", 0.0)
	 	 	#self.top_mass_hist.Fill(genpart.mass)
	 	 	self.out.fillBranch("top_mass_gen", genpart.mass)
                        self.out.fillBranch("top_pt_gen", genpart.pt)
                        self.out.fillBranch("top_eta_gen", genpart.eta)
                        self.out.fillBranch("top_phi_gen", genpart.phi)

                        self.out.fillBranch("neutrino_pt_gen",neutrino_pt_gen)
                        self.out.fillBranch("neutrino_eta_gen",neutrino_eta_gen)
                        self.out.fillBranch("neutrino_phi_gen",neutrino_phi_gen)
                        self.out.fillBranch("neutrino_el_flag", neutrino_el_flag)
                        self.out.fillBranch("neutrino_mu_flag", neutrino_mu_flag)

                        self.out.fillBranch("lepton_pt_gen",  genpart.pt)
                        self.out.fillBranch("lepton_eta_gen",  genpart.eta)
                        self.out.fillBranch("lepton_phi_gen", genpart.phi)
                        

                        #print "Genpart top mass : %s pt : %s eta : %s phi : %s" %(genpart.mass,genpart.pt,genpart.eta,genpart.phi)
	 	        #print ("top mass filed")	
	 	 	break 
	 	    ID = ID+1
            else:
                print "top_from_lepton : ",top_from_lepton," top_from_bquark : ",top_from_bquark," top_from_nuetrino : ",top_from_nuetrino
                self.out.fillBranch("W_mass_gen", -1000)
                self.out.fillBranch("W_pt_gen",-1000)
                self.out.fillBranch("W_eta_gen", -1000)
                self.out.fillBranch("W_phi_gen", -10000)
                self.out.fillBranch("tau_to_el_flag", -2.0)
                self.out.fillBranch("tau_to_mu_flag", -2.0)
                self.out.fillBranch("el_flag", -2.0)
                self.out.fillBranch("mu_flag", -2.0)
                self.out.fillBranch("top_mass_gen", -1000)
                self.out.fillBranch("top_pt_gen", -1000)
                self.out.fillBranch("top_eta_gen", -1000)
                self.out.fillBranch("top_phi_gen", -1000)
                self.out.fillBranch("top_mass_gen_reco", -1000)
                self.out.fillBranch("top_pt_gen_reco", -1000)
                self.out.fillBranch("top_eta_gen_reco", -1000)
                self.out.fillBranch("top_phi_gen_reco", -1000)
                self.out.fillBranch("neutrino_pt_gen",-1000)
                self.out.fillBranch("neutrino_eta_gen",-1000)
                self.out.fillBranch("neutrino_phi_gen",-1000)
                self.out.fillBranch("lepton_pt_gen",  -1000)
                self.out.fillBranch("lepton_eta_gen",  -1000)
                self.out.fillBranch("lepton_phi_gen", -1000)
	else:
	    #print "top_from_lepton : %s top_from_bquark : %s top_from_nuetrino : %s event = %s"%(top_from_lepton,top_from_bquark,top_from_nuetrino,getattr(event,'event'))
            #PrintTrueflags(flag_for_b)
            self.out.fillBranch("W_mass_gen", -999)
            self.out.fillBranch("W_pt_gen",-999)
            self.out.fillBranch("W_eta_gen", -999)
            self.out.fillBranch("W_phi_gen", -999)

            self.out.fillBranch("tau_to_el_flag", -1.0)
            self.out.fillBranch("tau_to_mu_flag", -1.0)
            self.out.fillBranch("top_mass_gen", -999)
            self.out.fillBranch("top_pt_gen", -999)
            self.out.fillBranch("top_eta_gen", -999)
            self.out.fillBranch("top_phi_gen", -999)
            self.out.fillBranch("top_mass_gen_reco", -999)
            self.out.fillBranch("top_pt_gen_reco", -999)
            self.out.fillBranch("top_eta_gen_reco", -999)
            self.out.fillBranch("top_phi_gen_reco", -999)

            self.out.fillBranch("neutrino_pt_gen",-999)
            self.out.fillBranch("neutrino_eta_gen",-999)
            self.out.fillBranch("neutrino_phi_gen",-999)
           
            self.out.fillBranch("lepton_pt_gen",  -999)
            self.out.fillBranch("lepton_eta_gen",  -999)
            self.out.fillBranch("lepton_phi_gen", -999)

	#    
	#print("----------------------------------")
             #return True
        return True

NanoGenConstr_UL2016 = lambda : NanoGenModule('UL2016')
