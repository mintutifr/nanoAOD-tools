# cmseenv needed
#python Create_Workspace_input_file.py -y ULpostVFP2016 -l mu -D 0 -v  mtwMass 
#python Create_Workspace_input_file.py -y ULpostVFP2016 -l el -D 0 -v  mtwMass 

#python Create_DNNFit_Workspace_input_file.py -y UL2017 -l mu -DS 0 -v t_ch_CAsi -DC 0.0
#python Create_DNNFit_Workspace_input_file.py -y UL2017 -l el -DS 0 -v t_ch_CAsi -DC 0.0

python Create_DNNFit_Workspace_input_file.py -y ULpostVFP2016 -l mu -DS 0 -v t_ch_CAsi -DC 0.0
python Create_DNNFit_Workspace_input_file.py -y ULpostVFP2016 -l el -DS 0 -v t_ch_CAsi -DC 0.0

python Create_DNNFit_Workspace_input_file.py -y ULpreVFP2016 -l mu -DS 0 -v t_ch_CAsi -DC 0.0
python Create_DNNFit_Workspace_input_file.py -y ULpreVFP2016 -l el -DS 0 -v t_ch_CAsi -DC 0.0
