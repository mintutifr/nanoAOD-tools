

import os
import glob
import multiprocessing as mp
import fileinput, string, sys, time, datetime

def run_cmd(run_command):
    os.system(run_command)

def replacemachine(fileName, sourceText, replaceText):
    print( "editing ",fileName,)
    for line in fileinput.input(fileName, inplace=True):
        if line.strip().startswith(sourceText):
                line = replaceText
        sys.stdout.write(line)
    print("All went well, the modifications are done")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='mu', help="lepton flavor [ el , mu ]")
    parser.add_argument('-r', '--region', dest='region', type=str, default='2J1T1', help="region of caluation [ 2J1T1 , 2J1T0 ]")
    parser.add_argument('-y', '--year', dest='year', type=str, default='UL2017', help="2017")
    parser.add_argument('-mc', '--ISMC', dest='ISMC', type=bool, default=True, help=" is MC sample [ True False ]")
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, default='/nfs/home/common/RUN2_UL/Minitree_crab/', help="Set Dir for the output files")
    args = parser.parse_args()

    Lep = args.lepton
    region = args.region
    year = args.year
    MC_Data = "mc" if args.ISMC else "data"
    year_folder = {'UL2016preVFP': 'SIXTEEN', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}
    tag =   region+'_'+Lep + '_' + MC_Data + '_' + year
    Out_dir = args.out_dir
    datasets = ['Tchannel','Tbarchannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','QCD_Pt-15To20_MuEnriched', 'QCD_Pt-20To30_MuEnriched', 'QCD_Pt-30To50_MuEnriched', 'QCD_Pt-50To80_MuEnriched', 'QCD_Pt-80To120_MuEnriched', 'QCD_Pt-120To170_MuEnriched', 'QCD_Pt-170To300_MuEnriched', 'QCD_Pt-300To470_MuEnriched', 'QCD_Pt-470To600_MuEnriched', 'QCD_Pt-600To800_MuEnriched', 'QCD_Pt-800To1000_MuEnriched', 'QCD_Pt-1000_MuEnriched', 'tw_antitop', 'tw_top', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WWTolnulnu', 'WZTo2Q2L', 'ZZTo2L2Nu', 'ZZTo2Q2L'] 
    #datasets = ['WJetsToLNu_0J']#[]#, 'ttbar_SemiLeptonic']
	#['QCD_Pt-120to170_EMEnriched', 'QCD_Pt-170to300_EMEnriched', 'QCD_Pt-300toInf_EMEnriched', 'QCD_Pt-30to50_EMEnriched', 'QCD_Pt-50to80_EMEnriched', 'QCD_Pt-80to120_EMEnriched', 'SLep', 'TbarLep', 'TLep', 'ttbar_FullyLeptonic', 'ttbar_SemiLeptonic', 'tw_antitop', 'tw_top', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'WWTo2L2Nu', 'WWTolnulnu', 'WZTo2Q2L', 'ZZTo2L2Nu', 'ZZTo2Q2L', 'DYJets'] 'ttbar_FullyLeptonic', 'ttbar_SemiLeptonic',
    run_commands = []
    Hadd_N_createoutfile_cmd = {}
    
    for dataset in datasets:
        print(dataset)
       	local_script_output_dir = Out_dir + year_folder[year]+'/'+region+'/'+Lep+'/'+dataset + '/' 
       	os.makedirs(local_script_output_dir+'log/', exist_ok = True)
       	#print('/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/MC/' + dataset)
       	in_files = glob.glob('/nfs/home/common/RUN2_UL/Tree_crab/'+year_folder[year]+'/MC/' + dataset + '/**/**/**/**/*.root')
       	print("total file selected : ",len(in_files))
       	Hadded_out_file_name = 'Minitree_'+ dataset+'_'+region+'_'+Lep+ '.root '
       	print(in_files)
       	inputFiles = [i for i in in_files if i != '']
       	Hadd_N_createoutfile_cmd[dataset] = 'python3 ../../scripts/haddnano.py ' + Out_dir +year_folder[year]+'/'+region+'/'+Hadded_out_file_name
        i=0
       	commom_run_cmd = 'pwd; cmsenv; python3 crab_script_Minitree_local.py  -d ' + dataset + ' -t ' + tag + ' -o ' + local_script_output_dir
       	total_file_in_set = 5
        fileSetcounter = 0
        infils = ''
       	for count,fil in enumerate(inputFiles):
            fileSetcounter+=1
            num = fil.split('/')[-1].split('.')[0].split('_')[-1]
       	    Hadd_N_createoutfile_cmd[dataset] += local_script_output_dir + 'tree_' + num + '_Skim.root '
       	    #print(Hadd_N_createoutfile_cmd[dataset])
            infils = infils+fil+" "
            if(fileSetcounter%total_file_in_set==0 or count+1==len(inputFiles)):
                #infils = infils+"]"
                run_commands.append(commom_run_cmd + ' -p ' + infils + ' &> ' + local_script_output_dir + 'log/log_' +str(count+1) + '.txt' )
                fileSetcounter = 0
                infils = ''
            i=i+1
            #if(i==total_file_in_set): break #switch of test perpose take only two file and the scripts
    print(run_commands)
    #print(Hadd_N_createoutfile_cmd[dataset])

    pool = mp.Pool(processes=10)
    pool.map(run_cmd, run_commands)


    for dataset in datasets:
        Hadded_out_file_name = 'Minitree_'+ dataset+'_'+region+'_'+Lep+ '.root '
        print("check if exists "+Out_dir + year_folder[year]+'/'+region+'/'+ Hadded_out_file_name)
        print(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name))
        if(os.path.isfile(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)):
                keyinput = input(Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name+ '  is exit should delete and recreate enter "yes" other wise press eneter key i will skip the hadd command' )
                if(keyinput=='yes'):os.system('rm ' + Out_dir + year_folder[year]+'/'+region+'/'+Hadded_out_file_name)
                else: exit(0)
        print("runing....", Hadd_N_createoutfile_cmd[dataset])
        os.system(Hadd_N_createoutfile_cmd[dataset])
