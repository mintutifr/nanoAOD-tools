from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config

config = Configuration()

config.section_("General")

config.General.requestName = 'DYto2L-2Jets_MLL-50_Tree_UL2022EEpre'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_skimTree.sh'
#config.JobType.maxMemoryMB = 4000
config.JobType.inputFiles = ['crab_script_skimTree.py','../../scripts/haddnano.py','keep_and_drop.txt','MainModule.py']
#config.JobType.sendPythonFolder=True
config.section_("Data")

config.Data.inputDataset = '/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM'

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.allowNonValidInputDataset = True

"""config.Data.lumiMask ="""

config.Data.outLFNDirBase = '/store/user/lbhatt/crab/ee_lok_old/RUN2_UL/Tree_crab/2022EEpre/MC/DYto2L-2Jets_MLL-50'

config.Data.publication = False

config.Data.outputDatasetTag = 'Tree_08_Feb26_MCUL2022EEpre_DYto2L-2Jets_MLL-50'

config.section_("Site")
config.Site.storageSite = 'T3_CH_CERNBOX'
