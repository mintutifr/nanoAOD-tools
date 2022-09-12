from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

config.General.requestName = 'Tbarchannel_wtop1p45_Tree_UL2016'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_NanoGen_skimtree.sh'
#config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_NanoGen_skimtree.py','../../scripts/haddnano.py','clean_All_keep_GenPart.txt','Gen_mass_reconstract_SingleTop.py','Gen_mass_functions.py']
config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_antitop_4f_InclusiveDecays_wtop1p45_TuneCP5_fixWidth_13TeV-powheg-madspin-pythia8/RunIISummer20UL16wmLHENanoGEN-106X_mcRun2_asymptotic_v13-v1/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/Mc_NANOGEN_v7/Tbarchannel_wtop1p45'

config.Data.publication = True

config.Data.outputDatasetTag = 'Tree_03_Sep22_MCUL2016_Tbarchannel_wtop1p45_v7'

config.section_("Site")
config.Site.storageSite = 'T2_IN_TIFR'

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
