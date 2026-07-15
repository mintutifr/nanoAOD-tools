

#source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
#python -u Train_NN_pytorch.py -y ULpreVFP2016 -l mu &> log_Train_NN_pytorch_ULpreVFP2016_mu.out
#python -u Train_NN_pytorch.py -y ULpreVFP2016 -l el &> log_Train_NN_pytorch_ULpreVFP2016_el.out
#python -u Train_NN_pytorch.py -y ULpostVFP2016 -l mu &> log_Train_NN_pytorch_ULpostVFP2016_mu.out
#python -u Train_NN_pytorch.py -y ULpostVFP2016 -l el &> log_Train_NN_pytorch_ULpostVFP2016_el.out
#python3 -u Train_NN_pytorch.py -y UL2017 -l mu  &> log_Train_NN_pytorch_UL2017_mu.out
#python3 -u Train_NN_pytorch.py -y UL2017 -l el  &> log_Train_NN_pytorch_UL2017_el.out
python3 -u Train_NN_pytorch.py -y UL2018 -l mu &> log_Train_NN_pytorch_UL2018_mu.out
python3 -u Train_NN_pytorch.py -y UL2018 -l el &> log_Train_NN_pytorch_UL2018_el.out

#python Train_NN_pytorch_check_droplJetdeepJet.py -y UL2018 -l mu
#python Train_NN_pytorch_check_droplJetdeepJet.py -y UL2018 -l el