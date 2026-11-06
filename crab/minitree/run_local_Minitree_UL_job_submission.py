#Example usage:

###############################

# for proessing UL2018 only sample processing: (MC and Data)
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 --processing &> Mintree_processing_mu_2J1T1_UL2018_MC_processing.out
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 -data --processing &> Mintree_processing_mu_2J1T1_UL2018_data_processing.out

# for particular channel processing:(MC and Data)
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 --processing --channel ttbar_SemiLeptonic ttbar_FullyLeptonic &> Mintree_processing_mu_2J1T1_UL2018_MC_processing.out
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 -data --processing --channel Run2018A_mu &> Mintree_processing_mu_2J1T1_UL2018_data_processing.out


# for proessing UL2018 only hadd processed files: (MC and Data)
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 --hadd #&> Mintree_processing_mu_2J1T1_UL2018_MC_hadd.out
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 -data --hadd #&> Mintree_processing_mu_2J1T1_UL2018_data_hadd.out

# for particular channel only hadd processed files:(MC and Data)
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 --hadd --channel ttbar_SemiLeptonic ttbar_FullyLeptonic &> Mintree_processing_mu_2J1T1_UL2018_MC_hadd.out
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 -data --hadd --channel Run2018A_mu &> Mintree_processing_mu_2J1T1_UL2018_data_hadd.out

# Exclude ttbar samples from only hadd processed files:(MC only)
# python3 -u crab_submission_Minitree_UL_local.py -y UL2018 -l mu -r 2J1T1 --hadd --exclude_ttbar_fromhadd &> Mintree_processing_mu_2J1T1_UL2018_MC_hadd_exclude_ttbar.out

# check file processing faild jobs (MC and Dtata)
# you can skip --run_missing flag just to print the missing files and rerun commands for failed jobs
# python3 -u check_local_pooljob_status_V2.py -d /nfs/home/common/RUN2_UL/Minitree_trial/EIGHTEEN/2J1T1/ -s Mc_Nomi -l mu --run_missing
# python3 -u check_local_pooljob_status_V2.py -d /nfs/home/common/RUN2_UL/Minitree_trial/EIGHTEEN/2J1T1/ -l mu  --data --run_missing
##############################
