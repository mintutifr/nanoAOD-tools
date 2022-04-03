#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

#jecredo option has been removed check why------> Doest matter because redo option was for fat jets not for AK4 jets 

#createJMECorrector(isMC=True, dataYear=2016,runPeriod="B",jesUncert="Total",jetType="AK4PFchs",noGroom=False,metBranchName="MET",applySmearing=True, isFastSim=False, applyHEMfix=False,splitJER=False, saveMETUncs=['T1', 'T1Smear']
jmeCorrections2016_MC_AK4CHS = createJMECorrector(True, "UL2016_preVFP", "", "All", "AK4PFchs", False,"MET")   #2016 MC AK4 CHS 
jmeCorrections2016_MC_AK4CHS = createJMECorrector(True, "UL2016", "", "All", "AK4PFchs", False,"MET")   #2016 MC AK4 CHS
jmeCorrections2017_MC_AK4CHS = createJMECorrector(True, "UL2017", "", "All", "AK4PFchs", False,"MET")   #2017 MC AK4 CHS
jmeCorrections2018_MC_AK4CHS = createJMECorrector(True, "UL2018", "", "All", "AK4PFchs", False,"MET")   #2018 MC AK4 CHS

#jecTag_ = jecTagsDATA[dataYear + runPeriod]

jmeCorrectionsRun2016VFPB_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "B", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPC_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "C", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPD_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "D", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPE_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "E", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPF_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "F", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPG_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "G", "All", "AK4PFchs")
jmeCorrectionsRun2016VFPH_DATA_AK4CHS = createJMECorrector(False, "UL2016_preVFP", "H", "All", "AK4PFchs")


jmeCorrectionsRun2016B_DATA_AK4CHS = createJMECorrector(False, "UL2016", "B", "All", "AK4PFchs")
jmeCorrectionsRun2016C_DATA_AK4CHS = createJMECorrector(False, "UL2016", "C", "All", "AK4PFchs")
jmeCorrectionsRun2016D_DATA_AK4CHS = createJMECorrector(False, "UL2016", "D", "All", "AK4PFchs")
jmeCorrectionsRun2016E_DATA_AK4CHS = createJMECorrector(False, "UL2016", "E", "All", "AK4PFchs")
jmeCorrectionsRun2016F_DATA_AK4CHS = createJMECorrector(False, "UL2016", "F", "All", "AK4PFchs")
jmeCorrectionsRun2016G_DATA_AK4CHS = createJMECorrector(False, "UL2016", "G", "All", "AK4PFchs")
jmeCorrectionsRun2016H_DATA_AK4CHS = createJMECorrector(False, "UL2016", "H", "All", "AK4PFchs")


jmeCorrectionsRun2017B_DATA_AK4CHS = createJMECorrector(False, "UL2017", "B", "All", "AK4PFchs")
jmeCorrectionsRun2017C_DATA_AK4CHS = createJMECorrector(False, "UL2017", "C", "All", "AK4PFchs")
jmeCorrectionsRun2017D_DATA_AK4CHS = createJMECorrector(False, "UL2017", "D", "All", "AK4PFchs")
jmeCorrectionsRun2017E_DATA_AK4CHS = createJMECorrector(False, "UL2017", "E", "All", "AK4PFchs")
jmeCorrectionsRun2017F_DATA_AK4CHS = createJMECorrector(False, "UL2017", "F", "All", "AK4PFchs")

