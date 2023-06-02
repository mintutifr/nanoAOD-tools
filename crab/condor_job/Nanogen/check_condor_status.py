import fileinput, string, sys, os, time, subprocess
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')  
parser.add_argument('-d', '--dir', dest='CondorDir', type=str, nargs=1, help="condor directory")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc , Data ]")
parser.add_argument('-y', '--year', dest='years', type=str, nargs=1, help="Year [ UL2016 ]")
parser.add_argument('-l', '--lepton', dest='leptons', type=str, nargs=1, help="sample [ mu , el ]")

args = parser.parse_args()

if args.CondorDir == None:
	print "USAGE: %s [-h] [-d <condor directory>]"%(sys.argv [0])
        sys.exit (1) 
if args.years[0] not in ['UL2016']:
    print('Error: Incorrect choice of year, use -h for help')
    sys.exit(1)
if args.leptons[0] not in ['mu','el']:
    print('Error: Incorrect choice of lepton type, use -h for help')
    sys.exit(1)

CondorDir=args.CondorDir[0]
if not (os.path.isdir(CondorDir)):
	print "Dir", " '",CondorDir,"' "," does not exist" 
	sys.exit (1)


def get_dirs(rootdir):
    Dirs=[]
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            #print(d)
	    Dirs.append(d)
            #listdirs(d)
    return Dirs

def find_files(search_path):
   result = []
   # Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
   	for filename in files:
	    if filename.endswith('_phy3.py'):
		#print root+'/'+str(filename)
         	result.append(root+'/'+str(filename))
		if(len(result)==1): break
	    if(len(result)==1): break
   return result

datasets_file=find_files(CondorDir)
datasets_file=datasets_file[0]
print datasets_file
print str(datasets_file.rsplit(".")[0])
sys.path.insert(0,str(datasets_file.rsplit(".")[0].rsplit("/",1)[0]))
#datasetspy=__import__(str(datasets_file.rsplit(".")[0].rsplit("/",1)[1]))

lep = args.leptons[0]
year   = args.years[0]
sample = args.samples[0]

if(year == 'UL2016'):
    from dataset_UL2016_phy3 import *
    if sample=="Mc" : Datasets = Datasets_MC_UL2016


#channels=['WWTo2L2Nu']
channels=Datasets.keys()
print 
print "-----------------------------------------    chacking     --------------------------------"
print
cwd = os.getcwd()
for channel in channels:
    if((lep=="el" and "MuEnriched" in channel) or (lep=="mu" and "EMEnriched" in channel)):
        continue
    if not (os.path.isdir(CondorDir+"/"+channel)):
        print
        proceed = raw_input(CondorDir+"/"+channel +"  does not exist; you can skip this press 1/Yes and press other key to exit : ")
        if(proceed=="1" or proceed=="yes"): continue
        else: exit()
    Dirs=get_dirs(CondorDir+"/"+channel)

    for Dir in Dirs:
        cmd_grep = 'grep "Server responded with an error" '+Dir+'/*'
        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        skip_tranfer_check = False
        if(output.count("Server responded with an error")>0):
                print "Server responded with an error in ",Dir
                #print os.system(cmd_grep)
                skip_tranfer_check = True
                condor_resubmit = raw_input("file acess error in @@ " +Dir+"/ to resubmit the job press 1/yes: ")
                if(condor_resubmit=="yes" or condor_resubmit=="1"):
                        os.chdir(Dir)
                        os.system("rm condor_out_*.std*")
                        os.system("condor_submit condorSetup.sub")
                        os.chdir(cwd)


        cmd_grep = 'grep "Redirect limit has been reached" '+Dir+'/*'
        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if(output.count("Redirect limit has been reached")>0):
                print "Redirect limit has been reached ",Dir
                #print os.system(cmd_grep)
                skip_tranfer_check = True
                condor_resubmit = raw_input("file acess error in @@ " +Dir+"/ to resubmit the job press 1/yes: ")
                if(condor_resubmit=="yes" or condor_resubmit=="1"):
                       os.chdir(Dir)
                       os.system("rm condor_out_*.std*")
                       os.system("condor_submit condorSetup.sub")
                       os.chdir(cwd)


        cmd_grep = 'grep "100%" '+Dir+'/*'
        #os.system(cmd_grep)

        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        if(output.count("100%")==0): 
	     condor_resubmit = raw_input("did not enouter '100%' tranfer @ " +Dir+"/ to resubmit the job press 1/yes: ")
	     if(condor_resubmit=="yes" or condor_resubmit=="1"):
	     	os.chdir(Dir)
	     	os.system("condor_submit condorSetup.sub")
	     	os.chdir(cwd)
 
