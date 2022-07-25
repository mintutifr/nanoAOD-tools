import fileinput, string, sys, os, time, datetime
import argparse as arg
from tqdm import tqdm

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-y', '--year', dest='inputs', type=str, nargs=1, help="Year [UL2016preVFP, UL2016postVFP, UL2017, UL2018]")
args = parser.parse_args()


if args.inputs == None:
        print "USAGE: %s [-h] [-y <Data year>]"%(sys.argv [0])
        sys.exit (1)

if args.inputs[0] not in ['UL2016']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

print "year = ",args.inputs[0]
year   = args.inputs[0]
date   = datetime.datetime.now()

if(year == 'UL2016'):
    from dataset_UL2016 import *
    outputDir = "/store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_NaNOGEN/"
    Datasets = Datasets_Alt_MC_UL2016APV

RequestNames = Datasets.keys()
print RequestNames
print "len(Datasets) = ",len(Datasets)

cfgfile = "crab_cfg_NanoGen_skimTree.py"
scriptfile = "crab_script_NanoGen_skimtree.py"

def replacemachine(fileName, sourceText, replaceText):
    ##################################################################
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
        	line = replaceText
    	sys.stdout.write(line)
    print "All went well, the modifications are done"
    ##################################################################

#print RequestName
for i in tqdm(range(0,len(RequestNames))):
    RequestName = RequestNames[i]
    Dataset = Datasets[RequestName]
    print RequestName, " : ",Dataset
    update_RequestName = "config.General.requestName = '"+RequestName+"_Tree_"+year+"'\n" 
    update_Dataset = "config.Data.inputDataset = '"+Dataset+"'\n"
    update_DirBase = "config.Data.outLFNDirBase = '"+outputDir+RequestName+"'\n"
    update_DatasetTag = "config.Data.outputDatasetTag = 'Tree_"+date.strftime("%d")+"_"+date.strftime("%b")+date.strftime("%y")+"_MC"+year+"_"+RequestName+"'\n"
    update_InputFiles = "config.JobType.inputFiles = ['crab_script_NanoGen_skimtree.py','../../scripts/haddnano.py','clean_All_keep_GenPart.txt','Gen_mass_reconstract_SingleTop.py','Gen_mass_functions.py']\n"    
    update_site = "config.Site.storageSite = 'T2_IN_TIFR'\n"
    update_module = "\tmodules=[NanoGenConstr_"+year+"()],\n"

    print "RequestName = ",update_RequestName ,"\tDatasets = ",update_Dataset,"\tDirBase = ",update_DirBase,"\tDatasetTag = ",update_DatasetTag 
    print "InputFiles = ",update_InputFiles
    print  update_site
    print  update_module

    replacemachine(cfgfile,'config.General.requestName =', update_RequestName)
    replacemachine(cfgfile,'config.Data.inputDataset =', update_Dataset )
    replacemachine(cfgfile,'config.Data.outLFNDirBase =', update_DirBase )
    replacemachine(cfgfile,'config.Data.outputDatasetTag =', update_DatasetTag )
    replacemachine(cfgfile,'config.JobType.inputFiles =', update_InputFiles )
    replacemachine(cfgfile,'config.Site.storageSite =', update_site )
    replacemachine(scriptfile,'modules=', update_module ) 

    cmd_crab_submit = "crab submit -c "+cfgfile
    #os.system(cmd_crab_submit)  
 
    #cmd_crab_kill = "crab kill -d crab_"+RequestName[i]
    #os.system(cmd_crab_kill)

    #cmd_rm_dir = "rm -rf crab_"+RequestName[i]
    #os.system(cmd_rm_dir)


    print "DONE -----",RequestName,"--------------------------------------------------------------------------------------------"
    time.sleep(10) 
    
