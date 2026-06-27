from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

config.General.requestName = 'Run2024H_Muon1_Tree_2024'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
#config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']
#config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/Muon1/Run2024H-MINIv6NANOv15-v2/NANOAOD'

config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 150
config.Data.allowNonValidInputDataset = True

config.Data.lumiMask = 'Golden2024H.json'

config.Data.outLFNDirBase = '/store/user/lbhatt/crab/DataAA_mu/Run2024H_Muon1'

config.Data.publication = False

config.Data.outputDatasetTag = 'Tree_26_Jun26_Run2024H_Muon1'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
