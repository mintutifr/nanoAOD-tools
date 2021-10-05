#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *

#jecredo option has been removed check why------> Doest matter because redo option was for fat jets not for AK4 jets 

jmeCorrections2016_MC_AK4CHS = createJMECorrector(True, "2016", "", "All", "AK4PFchs", False)   #2016 MC AK4 CHS
jmeCorrections2017_MC_AK4CHS = createJMECorrector(True, "2017", "", "All", "AK4PFchs", False)   #2017 MC AK4 CHS
jmeCorrections2018_MC_AK4CHS = createJMECorrector(True, "2018", "", "All", "AK4PFchs", False)   #2018 MC AK4 CHS

jmeCorrectionsRun2016B_DATA_AK4CHS = createJMECorrector(False, "2016", "B", "All", "AK4PFchs")
jmeCorrectionsRun2016C_DATA_AK4CHS = createJMECorrector(False, "2016", "C", "All", "AK4PFchs")
jmeCorrectionsRun2016D_DATA_AK4CHS = createJMECorrector(False, "2016", "D", "All", "AK4PFchs")
jmeCorrectionsRun2016E_DATA_AK4CHS = createJMECorrector(False, "2016", "E", "All", "AK4PFchs")
jmeCorrectionsRun2016F_DATA_AK4CHS = createJMECorrector(False, "2016", "F", "All", "AK4PFchs")
jmeCorrectionsRun2016G_DATA_AK4CHS = createJMECorrector(False, "2016", "G", "All", "AK4PFchs")
jmeCorrectionsRun2016H_DATA_AK4CHS = createJMECorrector(False, "2016", "H", "All", "AK4PFchs")

jmeCorrectionsRun2017B_DATA_AK4CHS = createJMECorrector(False, "2017", "B", "All", "AK4PFchs")
jmeCorrectionsRun2017C_DATA_AK4CHS = createJMECorrector(False, "2017", "C", "All", "AK4PFchs")
jmeCorrectionsRun2017D_DATA_AK4CHS = createJMECorrector(False, "2017", "D", "All", "AK4PFchs")
jmeCorrectionsRun2017E_DATA_AK4CHS = createJMECorrector(False, "2017", "E", "All", "AK4PFchs")
jmeCorrectionsRun2017F_DATA_AK4CHS = createJMECorrector(False, "2017", "F", "All", "AK4PFchs")

