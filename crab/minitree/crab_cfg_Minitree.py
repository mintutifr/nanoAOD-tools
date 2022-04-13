from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'Run2017C_mu_Minitree_2J1T1_UL2017'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_Minitree.sh'
config.JobType.inputFiles = ['crab_script_Minitree.py','../../scripts/haddnano.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/SingleMuon/mikumar-Tree_october_Seventeen_Run2017C_mu-b3a1988b93a84bf68fff9ff80c388e61/USER'

config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/MiniTree_crab/SEVENTEEN/Data/check/2J1T1_mu_new/Run2017C_mu'

config.Data.publication = False

config.Data.outputDatasetTag = 'MiniTree_13_Apr22_Run2017C_mu'

config.section_("Site")
config.Site.storageSite = 'T2_IN_TIFR'
config.Site.whitelist = ['T2_IN_TIFR']

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

