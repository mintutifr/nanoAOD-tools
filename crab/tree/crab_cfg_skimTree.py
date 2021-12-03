from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

config.General.requestName = 'Run2016H_mu_Tree'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
config.JobType.inputFiles = ['ElectronSF','MuonSF','crab_script_skimTree.py','scaleFactor.py','btv.py','jme.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py','Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt','Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'

#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 150
#config.Data.totalUnits = 1
config.Data.lumiMask = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/Tree_crab/SIXTEEN/Data_mu_new/Run2016H_mu'

config.Data.publication = True

config.Data.outputDatasetTag = 'Tree_03_Dec21_Run2016H_mu'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
