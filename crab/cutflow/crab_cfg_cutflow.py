from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'Run2016F_mu_cutflow2J1T1_mu_2016'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_cutflow.py','../scripts/haddnano.py','Mc_prob_cal_forBweght.py','cutflowModule.py','clean.txt']
#hadd nano will not be needed once nano tools are in cmssw
config.JobType.outputFiles = ['Cutflow_hist.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/SingleMuon/mikumar-Tree_october_Seventeen_Run2016F_mu-a73a1c2d67cfafe3e3eae6836e89c2e1/USER'

config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/cutflow_crab/SIXTEEN/Data/2J1T1_mu/Run2016F_mu'

config.Data.publication = False

config.Data.outputDatasetTag = 'cutflow_21_Nov20_Run2016F_mu'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
