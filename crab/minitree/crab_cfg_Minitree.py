from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'Tbarchannel_Minitree_2J1T1_mu_UL2016preVFP'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_Minitree.sh'
config.JobType.inputFiles = ['ElectronSF','MuonSF','scaleFactor.py','jme.py','crab_script_Minitree.py','../../scripts/haddnano.py','Mc_prob_cal_forBweght.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt','KinFit.C']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/mikumar-Tree_22_Apr22_MCUL2016preVFP_Tbarchannel_check-8957b29c601d60219f5188b9be2eb225/USER'

config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2_UL/MiniTree_crab/SIXTEEN/MC/2J1T1_mu/Tbarchannel'

config.Data.publication = False

config.Data.outputDatasetTag = 'MiniTree_28_Apr22_MCUL2016preVFP_Tbarchannel_2J1T1'

config.section_("Site")
config.Site.storageSite = 'T2_IN_TIFR'
#config.Site.whitelist = ['T2_IN_TIFR']

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

