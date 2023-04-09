from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

config.General.requestName = 'Run2017B_mu_Tree_UL2017'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']
config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/SingleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD'

config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 150
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/Tree_crab/SEVENTEEN/Data_mu/Run2017B_mu'

#config.Data.publication = True

config.Data.outputDatasetTag = 'Tree_09_Apr23_Run2017B_mu'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
