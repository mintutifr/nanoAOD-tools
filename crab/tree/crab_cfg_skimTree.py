from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

config.General.requestName = 'Tchannel_Tree_UL2016preVFP'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py','btv.py']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 10
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/Tchannel'

config.Data.publication = True

config.Data.outputDatasetTag = 'Tree_27_Apr22_MCUL2016preVFP_Tchannel_check'

config.section_("Site")
config.Site.storageSite = 'T2_IN_TIFR'

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
