import fileinput, string, sys, os, time

dataset = ['/SingleElectron/mikumar-Tree_october_Seventeen_Run2016B_vert2_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016C_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016D_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016E_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016F_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016G_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER', '/SingleElectron/mikumar-Tree_october_Seventeen_Run2016H_el-a73a1c2d67cfafe3e3eae6836e89c2e1/USER']

for i in range(0,len(dataset)):
    cmd_crab_invalidate = "python $DBS3_CLIENT_ROOT/examples/DataOpsScripts/DBS3SetDatasetStatus.py --url=https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter --status=INVALID --recursive=False --dataset="+dataset[i]
    os.system(cmd_crab_invalidate)
