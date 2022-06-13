#!/usr/bin/env python
import os, sys
import ROOT
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from Gen_mass_functions import *
class EfficiencyModule(Module):
    def __init__(self,datayear,jetSelection):
        self.jetSel = jetSelection
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
	self.out.branch("tau_to_el_flag", "F")
	self.out.branch("tau_to_mu_flag", "F")
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
                    #print_once = False
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
                    if( abs(motherPDG)==24  or abs(motherPDG)==15):
                        while ((motherPDG == GmotherPDG and GmotherPDG !=-1 and motherPDG !=-1 and Gmotheridx!=-1 and abs(GmotherPDG)!=6) or ( (abs(motherPDG)==24 or abs(motherPDG)==15) and abs(GmotherPDG)!=6 and GmotherPDG !=-1)):
                             #if(print_once==False):
                                #print GmotherPDG," --> ",
                                #print_once=True
                             PDG = motherPDG
                             motheridx = Gmotheridx
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
                
	 	ID=0
	 	for genpart in Genparts:
	 	    if(ID==top_from_lepton[0]):
                        #print genpart.statusFlags
                        #PrintTrueflags(Binary_flags(genpart.statusFlags))
	 	 	if(tau_to_el_flag):self.out.fillBranch("tau_to_el_flag", 1.0)
	       	       	else:self.out.fillBranch("tau_to_el_flag", 0.0)
	 	 	if(tau_to_mu_flag):self.out.fillBranch("tau_to_mu_flag", 1.0)
                        else:self.out.fillBranch("tau_to_mu_flag", 0.0)
	 	 	top_mass_gen = genpart.mass
	 	 	#self.top_mass_hist.Fill(genpart.mass)
	 	 	self.out.fillBranch("top_mass_gen", top_mass_gen)
	 	        #print ("top mass filed")	
	 	 	break 
	 	    ID = ID+1
            else:
                print "top_from_lepton : ",top_from_lepton," top_from_bquark : ",top_from_bquark," top_from_nuetrino : ",top_from_nuetrino
	else:
	    print "top_from_lepton : %s top_from_bquark : %s top_from_nuetrino : %s event = %s"%(top_from_lepton,top_from_bquark,top_from_nuetrino,getattr(event,'event'))
            #PrintTrueflags(flag_for_b)
            self.out.fillBranch("top_mass_gen", -999)
	#    
	#print("----------------------------------")
        return True

EfficiencyConstr_2016 = lambda : EfficiencyModule('2016',jetSelection= lambda j : j.pt > 20)
EfficiencyConstr_2017 = lambda : EfficiencyModule('2017',jetSelection= lambda j : j.pt > 20)

treecut="Entry$<1000"#"event==17066074"#"Entry$<1000"#event==9004381"#6644553"# Entry$<1000 "
#inputFiles=["/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"]
inputFiles=[	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tbarchannel_2J1T1_el.root",
	 	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc_dR/2J1T1/final/Minitree_Tchannel_2J1T1_el.root",
	 	"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tbarchannel_2J1T1_mu.root",
	 	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_Tchannel_2J1T1_mu.root"
 	 	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_ttbar_2J1T1_mu.root",
	 	#"/grid_mnt/t3storage3/mikumar/Run2/SIXTEEN/minitree/Mc/2J1T1/final/Minitree_ttbar_2J1T1_el.root",
         
	   ]
                
p=PostProcessor( ".",
                inputFiles,
                #treecut,
                modules=[EfficiencyConstr_2017()],
                outputbranchsel="clean_All_keep_GenPart.txt",
                provenance=True,
                fwkJobReport=True,
                jsonInput=runsAndLumis())
                #noOut=False,
                #histFileName="top_mass_reconstracted.root",
                #histDirName="Histograms")
p.run()

print "DONE"