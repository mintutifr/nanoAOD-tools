from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")

#2016 MC
config.General.requestName = 'QCD_Pt-300toInf_EMEnriched_Minitree_2J1T0_el_2016'

config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_Minitree.sh'
config.JobType.inputFiles = ['crab_Minitree.py','../scripts/haddnano.py','Mc_prob_cal_forBweght.py','foxwol_n_fourmomentumSolver.py','MinitreeModule.py','cut_strings.py','keep_and_drop_mu_Minitree.txt','keep_and_drop_el_Minitree.txt']
#hadd nano will not be needed once nano tools are in cmssw
#config.JobType.outputFiles = ['B_DeepCSV_Efficiency.root']
config.JobType.sendPythonFolder	 = True
config.section_("Data")

config.Data.inputDataset = '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/mikumar-Tree_11_Jul21_MC2016_QCD_Pt-300toInf_EMEnriched-8ecc050433dbcfb7ea89627141b876b6/USER'

config.Data.inputDBS = 'phys03'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/mikumar/RUN2/MiniTree_crab/SIXTEEN/MC/dR_len_with_Jet/2J1T0_el/QCD_Pt-300toInf_EMEnriched'

config.Data.publication = False

config.Data.outputDatasetTag = 'MiniTree_24_Jul21_MC2016_QCD_Pt-300toInf_EMEnriched_2J1T0'

config.section_("Site")
config.Site.storageSite = "T2_IN_TIFR"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

