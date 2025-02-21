# Define the arrays
YEARS=("UL2016postVFP" "UL2018" "UL2017" "UL2016preVFP")
LEP=("el" "mu")

# Loop through each combination
for year in "${YEARS[@]}"; do
    for lepton in "${LEP[@]}"; do
        echo "Running for Year: $year, Lepton: $lepton"
        python3 Create_mtopFit_Workspace_input_file.py -y "$year" -l "$lepton" -DC "(t_ch_CAsi>=0.7) " -v  lntopMass -allsys #-Bweight_sys #-puWeight_sys  #-ISR_FSR_sys #-JES_JER_sys #-allsys  #-Alt #-puWeight_sys #-Bweight_sys #-lepSF_sys #-JES_JER_sys
    done
done
