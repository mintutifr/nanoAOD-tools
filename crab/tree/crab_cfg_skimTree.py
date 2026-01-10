from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

config.General.requestName = 'TTZ_Tree_UL2022EEpre'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
#config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']
#config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/TTZ-ZtoQQ-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
"""config.Data.lumiMask ="""

config.Data.outLFNDirBase = '/store/user/lbhatt/crab/RUN2_UL/Tree_crab/2022EEpre/MC/TTZ'

config.Data.publication = False

config.Data.outputDatasetTag = 'Tree_07_Jan26_MCUL2022EEpre_TTZ'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
