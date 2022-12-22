# cmseenv needed
#python save_dataframe.py -y ULpreVFP2016 -l mu
#python save_dataframe.py -y ULpreVFP2016 -l el
#python save_dataframe.py -y ULpostVFP2016 -l mu
#python save_dataframe.py -y ULpostVFP2016 -l el
#python save_dataframe.py -y UL2017 -l mu
#python save_dataframe.py -y UL2017 -l el

#torch needed
python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y ULpreVFP2016
python Apply_NN_pytorch_FullMC_N_Data.py -l el -y ULpreVFP2016
python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y ULpostVFP2016
python Apply_NN_pytorch_FullMC_N_Data.py -l el -y ULpostVFP2016
python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y UL2017
python Apply_NN_pytorch_FullMC_N_Data.py -l el -y ULpreVFP2016

#source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
#python Train_NN_pytorch.py -y UL2017 -l mu
#python Train_NN_pytorch.py -y UL2017 -l el
#python Train_NN_pytorch.py -y ULpreVFP2016 -l mu
#python Train_NN_pytorch.py -y ULpreVFP2016 -l el
#python Train_NN_pytorch.py -y ULpostVFP2016 -l mu
#python Train_NN_pytorch.py -y ULpostVFP2016 -l el

#source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
#python Test_NN_pytorch.py -y UL2017 -l mu
#python Test_NN_pytorch.py -y UL2017 -l el
#python Test_NN_pytorch.py -y ULpreVFP2016 -l mu
#python Test_NN_pytorch.py -y ULpreVFP2016 -l el
#python Test_NN_pytorch.py -y ULpostVFP2016 -l mu
#python Test_NN_pytorch.py -y ULpostVFP2016 -l el

#source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
#python roc_creater.py -y UL2017 -l mu
#python roc_creater.py -y UL2017 -l el
#python roc_creater.py -y ULpreVFP2016 -l mu
##python roc_creater.py -y ULpreVFP2016 -l el
#python roc_creater.py -y ULpostVFP2016 -l mu
#python roc_creater.py -y ULpostVFP2016 -l el
