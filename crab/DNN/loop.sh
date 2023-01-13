# cmseenv needed
#python save_dataframe.py -y ULpreVFP2016 -l mu
#python save_dataframe.py -y ULpreVFP2016 -l el
#python save_dataframe.py -y ULpostVFP2016 -l mu
#python save_dataframe.py -y ULpostVFP2016 -l el
#python save_dataframe.py -y UL2017 -l mu
#python save_dataframe.py -y UL2017 -l el


#source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
#python Train_NN_pytorch.py -y ULpreVFP2016 -l mu
#python Train_NN_pytorch.py -y ULpreVFP2016 -l el
#python Train_NN_pytorch.py -y ULpostVFP2016 -l mu
#python Train_NN_pytorch.py -y ULpostVFP2016 -l el
#python Train_NN_pytorch.py -y UL2017 -l mu
#python Train_NN_pytorch.py -y UL2017 -l el

#source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
#python Test_NN_pytorch.py -y ULpreVFP2016 -l mu
#python Test_NN_pytorch.py -y ULpreVFP2016 -l el
#python Test_NN_pytorch.py -y ULpostVFP2016 -l mu
#python Test_NN_pytorch.py -y ULpostVFP2016 -l el
#python Test_NN_pytorch.py -y UL2017 -l mu
#python Test_NN_pytorch.py -y UL2017 -l el

#torch needed
#python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y ULpreVFP2016
#python Apply_NN_pytorch_FullMC_N_Data.py -l el -y ULpreVFP2016
#python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y ULpostVFP2016
#python Apply_NN_pytorch_FullMC_N_Data.py -l el -y ULpostVFP2016
#python Apply_NN_pytorch_FullMC_N_Data.py -l mu -y UL2017
#python Apply_NN_pytorch_FullMC_N_Data.py -l el -y UL2017

#source /cvmfs/sft.cern.ch/lcg/views/LCG_100cuda/x86_64-centos7-gcc8-opt/setup.sh
#python roc_creater_from_test_sample_withoutweight.py -y ULpreVFP2016 -l mu
#python roc_creater_from_test_sample_withoutweight.py -y ULpreVFP2016 -l el
#python roc_creater_from_test_sample_withoutweight.py -y ULpostVFP2016 -l mu
#python roc_creater_from_test_sample_withoutweight.py -y ULpostVFP2016 -l el
#python roc_creater_from_test_sample_withoutweight.py -y UL2017 -l mu
#python roc_creater_from_test_sample_withoutweight.py -y UL2017 -l el

# cmseenv needed
#python roc_creater_from_full_sample_withweights.py -y ULpreVFP2016 -l mu
#python roc_creater_from_full_sample_withweights.py -y ULpreVFP2016 -l el
#python roc_creater_from_full_sample_withweights.py -y ULpostVFP2016 -l mu
#python roc_creater_from_full_sample_withweights.py -y ULpostVFP2016 -l el
#python roc_creater_from_full_sample_withweights.py -y UL2017 -l mu
#python roc_creater_from_full_sample_withweights.py -y UL2017 -l el

# cmseenv needed
python Efficiency_creater.py -y ULpreVFP2016 -l mu
python Efficiency_creater.py -y ULpreVFP2016 -l el
python Efficiency_creater.py -y ULpostVFP2016 -l mu
python Efficiency_creater.py -y ULpostVFP2016 -l el
python Efficiency_creater.py -y UL2017 -l mu
python Efficiency_creater.py -y UL2017 -l el

# cmseenv needed
#python Efficiency_ploter.py -y ULpreVFP2016 -l mu
#python Efficiency_ploter.py -y ULpreVFP2016 -l el
#python Efficiency_ploter.py -y ULpostVFP2016 -l mu
#python Efficiency_ploter.py -y ULpostVFP2016 -l el
#python Efficiency_ploter.py -y UL2017 -l mu
#python Efficiency_ploter.py -y UL2017 -l el

# cmseenv needed
#python Efficiency_optomization_2D.py -y ULpreVFP2016 -l mu
#python Efficiency_optomization_2D.py -y ULpreVFP2016 -l el
#python Efficiency_optomization_2D.py -y ULpostVFP2016 -l mu
#python Efficiency_optomization_2D.py -y ULpostVFP2016 -l el
#python Efficiency_optomization_2D.py -y UL2017 -l mu
#python Efficiency_optomization_2D.py -y UL2017 -l el

#root -l -q 'Purity_signalEffi.C("el","ULpreVFP2016")'
#root -l -q 'Purity_signalEffi.C("mu","ULpreVFP2016")'
#root -l -q 'Purity_signalEffi.C("el","ULpostVFP2016")'
#root -l -q 'Purity_signalEffi.C("mu","ULpostVFP2016")'
#root -l -q 'Purity_signalEffi.C("el","UL2017")'
#root -l -q 'Purity_signalEffi.C("mu","UL2017")'
