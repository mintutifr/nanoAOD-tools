import fileinput, string, sys, os, time, subprocess
import argparse as arg
import multiprocessing as mp
import glob

def run_cmd(run_command):
    os.system(run_command)


if __name__ == '__main__':
	parser = arg.ArgumentParser(description='inputs discription')  
	parser.add_argument('-d', '--dir', dest='LocalDir', type=str, default=['/nfs/home/common/RUN2_UL/Minitree_crab/SEVENTEEN/2J1T1'], nargs=1, help="condor directory")
	parser.add_argument('-s', '--sample', dest='samples', type=str, default=['Mc_Nomi'], nargs=1, help="sample [ Mc_Nomi , Mc_Alt , Mc_sys , Data ]")
	parser.add_argument('-l', '--lepton', dest='leptons', type=str, default=['mu'], nargs=1, help="sample [ mu , el ]")
	
	args = parser.parse_args()
	
	if args.LocalDir == None:
	    print("USAGE: %s [-h] [-d <condor directory>]"%(sys.argv [0]))
	    exit(1) 
	if args.leptons[0] not in ['mu','el']:
	    print('Error: Incorrect choice of lepton type, use -h for help')
	    exit(1)
	if args.samples[0] not in ['Mc_Nomi', 'Mc_Alt', 'Mc_sys', 'Data']:
	    print('Error: Incorrect choice of sample type, use -h for help')
	    exit()
	
	
	LocalDir=args.LocalDir[0]
	if not (os.path.isdir(LocalDir)):
	    print("Dir", " '",LocalDir,"' "," does not exist")
	    exit()
	
	year_folder = {'SIXTEEN_preVFP':'UL2016preVFP', 'SIXTEEN_postVFP':'UL2016postVFP', 'SEVENTEEN':'UL2017', 'EIGHTEEN':'UL2018'}
	year = year_folder[LocalDir.split('/')[-2]] 
	
	lep = args.leptons[0]
	sample = args.samples[0]
	print(year)
	if(sample=="Mc_Nomi"):
	    channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']#,'Data'] #WWTolnulnu
	    channels.append("Data"+year)

	elif(sample=="Mc_sys"):
	    channels =['Tchannel_TuneCP5CR2',  'Tchannel_TuneCP5CR1',   'Tchannel_hdampdown',   'Tbarchannel_hdampdown',  'Tchannel_TuneCP5down',   'Tbarchannel_hdampup',   'Tchannel_hdampup',   'Tbarchannel_TuneCP5down',   'Tchannel_erdON',   'Tchannel_TuneCP5up',   'Tbarchannel_TuneCP5up',  'Tbarchannel_erdON',   'Tbarchannel_TuneCP5CR1',   'Tbarchannel_TuneCP5CR2']	
	
	#python3 crab_script_Minitree_local.py  -d ttbar_SemiLeptonic -t 2J1T1_mu_mc_UL2017 -o /nfs/home/common/RUN2_UL/Minitree_crab/SEVENTEEN/2J1T1/ -p /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_12_May23_MCUL2017_ttbar_SemiLeptonic/230512_063649/0000/tree_194.root /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_12_May23_MCUL2017_ttbar_SemiLeptonic/230512_063649/0000/tree_1.root /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_12_May23_MCUL2017_ttbar_SemiLeptonic/230512_063649/0000/tree_195.root /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_12_May23_MCUL2017_ttbar_SemiLeptonic/230512_063649/0000/tree_10.root /nfs/home/common/RUN2_UL/Tree_crab/SEVENTEEN/MC/ttbar_SemiLeptonic/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/Tree_12_May23_MCUL2017_ttbar_SemiLeptonic/230512_063649/0000/tree_145.root   &> /nfs/home/common/RUN2_UL/Minitree_crab/SEVENTEEN/2J1T1/mu/ttbar_SemiLeptonic/log/log_5.txt
	
	print()
	print("-----------------------------------------    chacking     --------------------------------")
	print()
	
	rerun_list = []
	cwd = os.getcwd()
	channels = ['ttbar_SemiLeptonic']
	for channel in channels:
	    outputDir = LocalDir + '/' + lep + '/' + channel + '/log'
	    log_files = glob.glob(outputDir + '/log_*.txt')
	    print(outputDir + '/log_*.txt') 
	    print(log_files)
	    for log_file in log_files:
	        cmd_grep = 'grep "Error" '+log_file
	        p = subprocess.Popen(cmd_grep, stdout=subprocess.PIPE, shell=True)
	        (output, err) = p.communicate()
	        p_status = p.wait()
	        skip_tranfer_check = False
	        #print(type(output))
	        output = str(output)
	        #print(output.count('Error'))
	        if(output.count("Error")>0):
	            cmd_grep2 = 'grep "python3 crab_script_Minitree_local.py" '+log_file
	            p2 = subprocess.Popen(cmd_grep2, stdout=subprocess.PIPE, shell=True)
	            (output2, err2) = p2.communicate()
	            rerun_list.append(str(output2)[2:-3]) # remove /n and b' from and end of command
	print(rerun_list)
	pool = mp.Pool(processes=10)
	pool.map(run_cmd, rerun_list)


