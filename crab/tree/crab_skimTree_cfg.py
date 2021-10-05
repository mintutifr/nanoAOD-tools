from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

config.General.requestName = 'Tchannel_mtop1695_Tree_2017'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
config.JobType.inputFiles = ['ElectronSF','MuonSF','clean.txt','crab_efficiency.py','crab_script.py','scaleFactor.py','../scripts/haddnano.py','keep_and_drop.txt','MainModule.py','EfficiencyModule.py']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_mtop1695_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'

#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1
#config.Data.lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt" 
#config.Data.lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/Tree_crab/SEVENTEEN/MC/dR_len_with_jet/Tchannel_mtop1695'

config.Data.publication = True

config.Data.outputDatasetTag = 'Tree_24_Jul21_MC2017_Tchannel_mtop1695'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
