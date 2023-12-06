#from __future__ import print_function
import sys, os
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
parser.add_argument('-s', '--sample', dest='samples', type=str, nargs=1, help="sample [ Mc_Nomi , Mc_Alt , Mc_sys ]")
parser.add_argument('-r', '--region', dest='regions', type=str, nargs=1, help="sample [ 2J1T , 3J1T , 2J1L0T , 3J2T , 2J0T ]")

args = parser.parse_args()

if (args.year == None or args.lepton == None):
        print("USAGE: %s [-h] [-y <Data year> -l <lepton>]"%(sys.argv [0]))
        sys.exit (1)

if args.year[0] not in ['ULpreVFP2016', 'ULpostVFP2016','UL2017','UL2018']:
    print('Error: Incorrect choice of year, use -h for help')
    exit()

if args.lepton[0] not in ['el','mu']:
    print('Error: Incorrect choice of lepton, use -h for help')
    exit()

if args.samples[0] not in ['Mc_Nomi', 'Mc_Alt', 'Mc_sys']:
    print('Error: Incorrect choice of sample type, use -h for help')
    exit()


print(args)

lep = args.lepton[0]
year= args.year[0]
sample = args.samples[0]
region = args.regions[0]

if(lep=="mu"):
	lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)


#if not os.path.exists('dataframe_saved/'+region+'1/'): os.makedirs('dataframe_saved/'+region+'1/')
if not os.path.exists('dataframe_saved/'+region+'1/sys_N_Alt'): os.makedirs('dataframe_saved/'+region+'1/sys_N_Alt')

from loader import *
import ROOT 
import numpy as np  
import pandas as pd
import root_pandas as rpd
import root_numpy 
from IPython.display import display
import glob
from time import time

if(sample=="Mc_Nomi"):
      channels = ['Tchannel' , 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']#,'Data'] #WWTolnulnu
      channels.append("Data"+year)

elif(sample=="Mc_Alt"):
        channels = [ 'ttbar_SemiLeptonic_mtop1695',   'ttbar_FullyLeptonic_mtop1695',   'Tbarchannel_mtop1735',   'ttbar_FullyLeptonic_widthx0p55',   'ttbar_FullyLeptonic_widthx0p7',   'ttbar_FullyLeptonic_mtop1735',   'Tbarchannel_mtop1715',   'ttbar_FullyLeptonic_widthx1p3',   'ttbar_FullyLeptonic_widthx1p45',   'ttbar_FullyLeptonic_mtop1715',   'Tchannel_mtop1715',   'ttbar_SemiLeptonic_mtop1755',   'ttbar_SemiLeptonic_mtop1735',   'ttbar_SemiLeptonic_mtop1715',   'ttbar_FullyLeptonic_widthx0p85',   'Tbarchannel_mtop1755',   'Tchannel_mtop1695',   'ttbar_FullyLeptonic_widthx1p15',   'Tchannel_mtop1735',   'Tchannel_mtop1755','ttbar_FullyLeptonic_mtop1755','Tbarchannel_mtop1695']

elif(sample=="Mc_sys"):
        channels =['Tchannel_TuneCP5CR2',  'Tchannel_TuneCP5CR1',   'Tchannel_hdampdown',   'Tbarchannel_hdampdown',  'Tchannel_TuneCP5down',   'Tbarchannel_hdampup',   'Tchannel_hdampup',   'Tbarchannel_TuneCP5down',   'Tchannel_erdON',   'Tchannel_TuneCP5up',   'Tbarchannel_TuneCP5up',  'Tbarchannel_erdON',   'Tbarchannel_TuneCP5CR1',   'Tbarchannel_TuneCP5CR2']


print channels
datasets = []                                            # this object will be a list of list
for channel in channels:
        datasets.append(load_dataset(-1,channel, lep, year,region,sample)) #apped all data frames in datasets

print(type(datasets[0]))
#bjet_deepjet_score = [] 
corr_assig = []
for channel_no in range(0,7):#len(channels)-1): 
        assig_channel = []
        Jet_partonFlavour_channel = datasets[channel_no]["Jet_partonFlavour"]  # get Jet_partonFlavour from the list of dataframes
        nbjet_sel_channel = datasets[channel_no]["nbjet_sel"]
        lepton_charge_channel = datasets[channel_no][lepton+"Charge"]
        for i in range (0,len(datasets[channel_no][lepton+"Eta"])): #loop over all events per channel since outer loop is over channels
                        if(Jet_partonFlavour_channel[i][nbjet_sel_channel[i]]*lepton_charge_channel[i]==5):
                                assig_channel.append(1) # this need not be done for each channel we suppose to do it for only Tchannel and Tbarchannel 
                        else:
                                assig_channel.append(0)
        corr_assig.append(assig_channel)
        del Jet_partonFlavour_channel
        del assig_channel
        del nbjet_sel_channel
        del lepton_charge_channel
        


VARS = [lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E',   lepton+'Charge',
        'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        'Px_nu', 'Py_nu', 'Pz_nu',
        'dEta_'+lep+'_lJet', 'dEta_'+lep+'_bJet',
        'dPhi_'+lep+'_lJet', 'dPhi_'+lep+'_bJet',
        'mtwMass',
        'dR_bJet_lJet',
        'abs_lJetEta',
        'jetpTSum',
        'diJetMass',
        'cosThetaStar',
        'FW1','Jet_partonFlavour',
        'bJetdeepJet',
        'lJetdeepJet',
        'Xsec_wgt',
        'LHEWeightSign',
        'L1PreFiringWeight_Nom',
        'event',
        'topMass'
        ]

df = {}  # remember this will be set of dataframe


for channel_no,channel  in enumerate(channels): #channels: #try to enumare funchtion to remove channel_no in this loop
     if("Data" not in channel and "QCD" not in channel):
        df[channel] = pd.DataFrame(datasets[channel_no],columns=VARS) #adding dataframes in the list
        if( channel in ['Tchannel', 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
              df[channel]['Assig'] = np.asarray(corr_assig[channel_no]) # adding new variable in each dataframe of a given channel 
     else:
        if("Xsec_wgt" in VARS): VARS.remove("Xsec_wgt")
        if("LHEWeightSign" in VARS): VARS.remove("LHEWeightSign")
        df[channel] = pd.DataFrame(datasets[channel_no],columns=VARS) #adding dataframes in the list
        
     print("df shape ", channel," : ",df[channel].shape[0])
     #df[channel]=df[channel].loc[(df[channel]['mtwMass']>50)]
     if(sample=="Mc_Nomi"):df[channel].to_root('dataframe_saved/'+region+'1/'+year+'_'+channel+'_Apply_all_'+lep+'.root',key='Events') 
     else:df[channel].to_root('dataframe_saved/'+region+'1/sys_N_Alt/'+year+'_'+channel+'_Apply_all_'+lep+'.root',key='Events')

if(sample!="Mc_Nomi"): sys.exit(sample+" saved")
del datasets
del corr_assig #this has been added
print("len of the list of dataframs  = ",len(df))
print("len of the list of channels  = ",len(channels))
channels.remove("Data"+year)
del df["Data"+year]

print("len of the list of dataframs  = ",len(df))
print("len of the list of channels  = ",len(channels))

#defin dec to store info channel wise
df_train = {}
df_valid = {}
df_test = {}

#loop to devide sample in train, valid and test
for channel in channels:
        Entries = df[channel].shape[0]
        df[channel] = df[channel].sample(frac = 1) ##randamize the sample
        df_train[channel] = df[channel].iloc[:int(Entries/2),:] # select half 0 to entries/2 for the traing
        df_valid[channel] = df[channel].iloc[int(Entries/2):int(3*Entries/4),:] # select entries/2 to (3/4)*entries for the validate
        df_test[channel] = df[channel].iloc[int(3*Entries/4):,:] ## select (3/4)*entries to end for the test
        print("total = ", df[channel].shape[0], " df_train = ", df_train[channel].shape[0], " df_valid = ",df_valid[channel].shape[0]," df_test = ",df_test[channel].shape[0])

del df #delete df since information is already split in df_train, df_valid, df_test

#define list to store the correct and incoorect assignment
df_signal_train_valid_test = []
df_signal_train_valid_test_correct_assign = []
df_signal_train_valid_test_wrong_assign = []

for df in [df_train,df_valid,df_test]:
	df_temp = pd.concat([df['Tchannel'],df['Tbarchannel']])                  # create temp df by adding tchannel and tbarchannel
	df_signal_train_valid_test.append(df_temp)                               # adding temp df to list of df where correcte and inccorrect assigment is not distigued
	df_temp_correct_assign = df_temp.query('Assig==1',inplace = False)       # saprate out the correct assignment and push to a new temp df
	df_signal_train_valid_test_correct_assign.append(df_temp_correct_assign) # adding temp df to list of df where only correcte assigment are allowed 
	del df_temp_correct_assign                                               # delete temp df for correct assignment
	df_temp_wrong_assign = df_temp.query('Assig==0',inplace = False)         # saprate out the incorrect assignment and push to a new temp df
	df_signal_train_valid_test_wrong_assign.append(df_temp_wrong_assign)     # adding temp df to list of df where only incorrecte assigment are allowed
	del df_temp_wrong_assign                                                 # delete temp df for incorrect assignment
	del df_temp                                                              # delete temp df which created in the begning of the for loop


print("\n==========================================================")
print("full signal")
print("train : ", df_signal_train_valid_test[0].shape, "valid : ", df_signal_train_valid_test[1].shape, "test : ", df_signal_train_valid_test[2].shape)

del df_signal_train_valid_test # delete the full datafrm for full sample since it aleady split in correct and wrong assignment list this was created just to check consitancy

print("only correct assignment signal")
print("train : ", df_signal_train_valid_test_correct_assign[0].shape, "valid : ", df_signal_train_valid_test_correct_assign[1].shape, "test : ", df_signal_train_valid_test_correct_assign[2].shape)
final_Events_for_training = df_signal_train_valid_test_correct_assign[0].shape[0]
final_Events_for_validatation = df_signal_train_valid_test_correct_assign[1].shape[0]
print()
print("Updated Number of Event for Traing = ", final_Events_for_training," ",type(final_Events_for_training) )
print("Updated Number of Event for Validate = ", final_Events_for_validatation," ",type(final_Events_for_validatation) )

print( "only wrong assignment signal")
print( "train : ", df_signal_train_valid_test_wrong_assign[0].shape, "valid : ", df_signal_train_valid_test_wrong_assign[1].shape, "test : ", df_signal_train_valid_test_wrong_assign[2].shape)
if(df_signal_train_valid_test_wrong_assign[0].shape[0] < final_Events_for_training): 
      final_Events_for_training=df_signal_train_valid_test_wrong_assign[0].shape[0]
      print()
      print("Updated Number of Event for Traing = ",final_Events_for_training)

if(df_signal_train_valid_test_wrong_assign[1].shape[0] < final_Events_for_validatation ): 
      final_Events_for_validatation = df_signal_train_valid_test_wrong_assign[1].shape[0]      
      print()
      print("Updated Number of Event for Validation = ", final_Events_for_validatation)

df_TopBKG_train_valid_test = []  #define a new list for train test and validation
df_TopBKG_train_valid_test_correct_assign = []
df_TopBKG_train_valid_test_wrong_assign = []

for i,df in enumerate([df_train,df_valid,df_test]):
    df_temp = pd.concat([df['tw_top'],df['tw_antitop'],df['Schannel'],df['ttbar_SemiLeptonic'],df['ttbar_FullyLeptonic']]) #adding all real top baground and push to a temp df
    df_TopBKG_train_valid_test.append(df_temp)
    df_temp_correct_assign = df_temp.query('Assig==1',inplace = False)       # saprate out the correct assignment and push to a new temp df
    df_TopBKG_train_valid_test_correct_assign.append(df_temp_correct_assign) # adding temp df to list of df where only correcte assigment are allowed 
    del df_temp_correct_assign                                               # delete temp df for correct assignment
    df_temp_wrong_assign = df_temp.query('Assig==0',inplace = False)         # saprate out the incorrect assignment and push to a new temp df
    df_TopBKG_train_valid_test_wrong_assign.append(df_temp_wrong_assign)     # adding temp df to list of df where only incorrecte assigment are allowed
    del df_temp_wrong_assign                                                 # delete temp df for incorrect assignment
    del df_temp #delete temp df
 
print( "\n==========================================================")
print( "full Top background")
print( "train : ", df_TopBKG_train_valid_test[0].shape, " valid : ", df_TopBKG_train_valid_test[1].shape, " test : ", df_TopBKG_train_valid_test[2].shape)

del df_TopBKG_train_valid_test # delet the full datafrm for full sample since it aleady split in correct and wrong assignment list this was created just to check consitancy

print("only correct assignment Top background")
print( "train : ", df_TopBKG_train_valid_test_correct_assign[0].shape, "valid : ", df_TopBKG_train_valid_test_correct_assign[1].shape, "test : ", df_TopBKG_train_valid_test_correct_assign[2].shape)
if(df_TopBKG_train_valid_test_correct_assign[0].shape[0] < final_Events_for_training):
      final_Events_for_training=df_TopBKG_train_valid_test_correct_assign[0].shape[0]
      print()
      print("Updated Number of Event for Traing = ",final_Events_for_training)

if(df_TopBKG_train_valid_test_correct_assign[1].shape[0] < final_Events_for_validatation):
      final_Events_for_validatation=df_TopBKG_train_valid_test_correct_assign[1].shape[0]
      print()
      print("Updated Number of Event for validation = ",final_Events_for_validatation)
        
print("only wrong assignment Top background")
print("train : ", df_TopBKG_train_valid_test_wrong_assign[0].shape, "valid : ", df_TopBKG_train_valid_test_wrong_assign[1].shape, "test : ", df_TopBKG_train_valid_test_wrong_assign[2].shape)
if(df_TopBKG_train_valid_test_wrong_assign[0].shape[0] < final_Events_for_training):
      final_Events_for_training=df_TopBKG_train_valid_test_wrong_assign[0].shape[0]
      print()
      print("Updated Number of Event for Traing = ",final_Events_for_training)
        
if(df_TopBKG_train_valid_test_wrong_assign[1].shape[0] <final_Events_for_validatation ):
      final_Events_for_validatation=df_TopBKG_train_valid_test_wrong_assign[1].shape[0]
      print()
      print("Updated Number of Event for Validation = ",final_Events_for_validatation)

df_EWKBKG_train_valid_test = []  #define a new list for train test and validation
for i,df in enumerate([df_train,df_valid,df_test]):
    df_temp = pd.concat([df['WJetsToLNu_0J'],df['WJetsToLNu_1J'],df['WJetsToLNu_2J'],df['DYJetsToLL'],df['WWTo2L2Nu'],df['WZTo2Q2L'],df['ZZTo2Q2L']]) # adding all EWK bkg and push to a temp df
    
    df_temp = df_temp.sample(frac = 1) #randamize the sample
    df_EWKBKG_train_valid_test.append(df_temp)
    del df_temp # #delete temp df

print("\n==========================================================")
print("EWK background")
print("train : ", df_EWKBKG_train_valid_test[0].shape, " valid : ", df_EWKBKG_train_valid_test[1].shape, " test : ", df_EWKBKG_train_valid_test[2].shape)
if(df_EWKBKG_train_valid_test[0].shape[0] < final_Events_for_training):
      final_Events_for_training=df_EWKBKG_train_valid_test[0].shape[0]
      print()
      print("Updated Number of Event for Traing = ",final_Events_for_training)

if(df_EWKBKG_train_valid_test[1].shape[0] < final_Events_for_validatation):
      final_Events_for_validatation=df_EWKBKG_train_valid_test[1].shape[0]
      print()
      print("Updated Number of Event for Validation = ",final_Events_for_validatation)
        
df_QCD_train_valid_test = []  #define a new list for train test and validation
for i,df in enumerate([df_train,df_valid,df_test]):
    df_QCD_train_valid_test.append(df['QCD'])

del df_train,df_valid,df_test # deleting datadames since the full information already absorbed in signal and backgrounds

print()
print("\n==========================================================")
print("QCD background")
print("train : ", df_QCD_train_valid_test[0].shape, " valid : ", df_QCD_train_valid_test[1].shape, " test : ", df_QCD_train_valid_test[2].shape)
#print "df_top_signal_corre_aaign : ",df_top_signal_correct_assign_new
if(df_QCD_train_valid_test[0].shape[0] < final_Events_for_training):
      final_Events_for_training=df_QCD_train_valid_test[0].shape[0]
      print()
      print("Updated Number of Event for Traing = ",final_Events_for_training)

if(df_QCD_train_valid_test[1].shape[0] < final_Events_for_validatation):
      final_Events_for_validatation=df_QCD_train_valid_test[1].shape[0]
      print()
      print("Updated Number of Event for Validation = ",final_Events_for_validatation)
        
print("\nFinal Number of Event for Traing = ",final_Events_for_training,type(final_Events_for_training))
print("\nFinal Number of Event for Validation = ",final_Events_for_training,type(final_Events_for_validatation))

print("\n========================== saving dataframes in root files after cross check ================================")


print("\n==========================================================")
print("signal")

df_signal_train_wrong_assign_final = df_signal_train_valid_test_wrong_assign[0].iloc[:int(final_Events_for_training),:]
df_signal_train_valid_test_wrong_assign[2] = df_signal_train_valid_test_wrong_assign[2].append(df_signal_train_valid_test_wrong_assign[0].iloc[int(final_Events_for_training):,:])

df_signal_valid_wrong_assign_final = df_signal_train_valid_test_wrong_assign[1].iloc[:int(final_Events_for_validatation),:]
df_signal_train_valid_test_wrong_assign[2] = df_signal_train_valid_test_wrong_assign[2].append(df_signal_train_valid_test_wrong_assign[1].iloc[int(final_Events_for_validatation):,:])

print( "only wrong assignment signal")
print( "train : ", df_signal_train_wrong_assign_final.shape, "valid : ", df_signal_valid_wrong_assign_final.shape, "test : ", df_signal_train_valid_test_wrong_assign[2].shape)

df_signal_train_wrong_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_signal_train_'+lep+'.root',key='Events') # write df in root file
df_signal_valid_wrong_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_signal_valid_'+lep+'.root',key='Events')
df_signal_train_valid_test_wrong_assign[2].to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_signal_test_'+lep+'.root',key='Events')

del df_signal_train_valid_test_wrong_assign # delete this dataframe since information is alreadyadded to new list of top backgrounds df
del df_signal_train_wrong_assign_final
del df_signal_valid_wrong_assign_final

df_signal_train_correct_assign_final = df_signal_train_valid_test_correct_assign[0].iloc[:int(final_Events_for_training),:]
df_signal_train_valid_test_correct_assign[2] = df_signal_train_valid_test_correct_assign[2].append(df_signal_train_valid_test_correct_assign[0].iloc[int(final_Events_for_training):,:])

df_signal_valid_correct_assign_final = df_signal_train_valid_test_correct_assign[1].iloc[:int(final_Events_for_validatation),:]
df_signal_train_valid_test_correct_assign[2] = df_signal_train_valid_test_correct_assign[2].append(df_signal_train_valid_test_correct_assign[1].iloc[int(final_Events_for_validatation):,:])

print("only correct assignment signal")
print("train : ", df_signal_train_correct_assign_final.shape, "valid : ", df_signal_valid_correct_assign_final.shape, "test : ", df_signal_train_valid_test_correct_assign[2].shape)

df_signal_train_correct_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_Top_signal_train_'+lep+'.root',key='Events') # write df in root file
df_signal_valid_correct_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_Top_signal_valid_'+lep+'.root',key='Events')
df_signal_train_valid_test_correct_assign[2].to_root('dataframe_saved/'+region+'1/'+year+'_Top_signal_test_'+lep+'.root',key='Events')

del df_signal_train_valid_test_correct_assign
del df_signal_train_correct_assign_final
del df_signal_valid_correct_assign_final

print("\n==========================================================")
print("Top Background")

df_TopBKG_train_correct_assign_final = df_TopBKG_train_valid_test_correct_assign[0].iloc[:int(final_Events_for_training),:]
df_TopBKG_train_valid_test_correct_assign[2] = df_TopBKG_train_valid_test_correct_assign[2].append(df_TopBKG_train_valid_test_correct_assign[0].iloc[int(final_Events_for_training):,:])

df_TopBKG_valid_correct_assign_final = df_TopBKG_train_valid_test_correct_assign[1].iloc[:int(final_Events_for_validatation),:]
df_TopBKG_train_valid_test_correct_assign[2] = df_TopBKG_train_valid_test_correct_assign[2].append(df_TopBKG_train_valid_test_correct_assign[1].iloc[int(final_Events_for_validatation):,:])

print("only correct assignment Top background")
print( "train : ", df_TopBKG_train_correct_assign_final.shape, "valid : ", df_TopBKG_valid_correct_assign_final.shape, "test : ", df_TopBKG_train_valid_test_correct_assign[2].shape)

df_TopBKG_train_correct_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_Top_bkg_train_'+lep+'.root',key='Events')
df_TopBKG_valid_correct_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_Top_bkg_valid_'+lep+'.root',key='Events')
df_TopBKG_train_valid_test_correct_assign[2].to_root('dataframe_saved/'+region+'1/'+year+'_Top_bkg_test_'+lep+'.root',key='Events')

del df_TopBKG_train_valid_test_correct_assign
del df_TopBKG_train_correct_assign_final
del df_TopBKG_valid_correct_assign_final

df_TopBKG_train_wrong_assign_final = df_TopBKG_train_valid_test_wrong_assign[0].iloc[:int(final_Events_for_training),:]
df_TopBKG_train_valid_test_wrong_assign[2] = df_TopBKG_train_valid_test_wrong_assign[2].append(df_TopBKG_train_valid_test_wrong_assign[0].iloc[int(final_Events_for_training):,:])

df_TopBKG_valid_wrong_assign_final = df_TopBKG_train_valid_test_wrong_assign[1].iloc[:int(final_Events_for_validatation),:]
df_TopBKG_train_valid_test_wrong_assign[2] = df_TopBKG_train_valid_test_wrong_assign[2].append(df_TopBKG_train_valid_test_wrong_assign[1].iloc[int(final_Events_for_validatation):,:])

print("only wrong assignment Top background")
print("train : ", df_TopBKG_train_wrong_assign_final.shape, "valid : ", df_TopBKG_valid_wrong_assign_final.shape, "test : ", df_TopBKG_train_valid_test_wrong_assign[2].shape)

df_TopBKG_train_wrong_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_bkg_train_'+lep+'.root',key='Events')
df_TopBKG_valid_wrong_assign_final.to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_bkg_valid_'+lep+'.root',key='Events')
df_TopBKG_train_valid_test_wrong_assign[2].to_root('dataframe_saved/'+region+'1/'+year+'_WS_Top_bkg_test_'+lep+'.root',key='Events')

del df_TopBKG_train_valid_test_wrong_assign
del df_TopBKG_train_wrong_assign_final
del df_TopBKG_valid_wrong_assign_final

df_EWKBKG_train_final = df_EWKBKG_train_valid_test[0].iloc[:int(final_Events_for_training),:]
df_EWKBKG_train_valid_test[2] = df_EWKBKG_train_valid_test[2].append(df_EWKBKG_train_valid_test[0].iloc[int(final_Events_for_training):,:])

df_EWKBKG_valid_final = df_EWKBKG_train_valid_test[1].iloc[:int(final_Events_for_validatation),:]
df_EWKBKG_train_valid_test[2] = df_EWKBKG_train_valid_test[2].append(df_EWKBKG_train_valid_test[1].iloc[int(final_Events_for_validatation):,:])

print("\n==========================================================")
print("EWK background")
print("train : ", df_EWKBKG_train_final.shape, " valid : ", df_EWKBKG_valid_final.shape, " test : ", df_EWKBKG_train_valid_test[2].shape)

df_EWKBKG_train_final.to_root('dataframe_saved/'+region+'1/'+year+'_EWK_BKG_train_'+lep+'.root',key='Events')
df_EWKBKG_valid_final.to_root('dataframe_saved/'+region+'1/'+year+'_EWK_BKG_valid_'+lep+'.root',key='Events')
df_EWKBKG_train_valid_test[2].to_root('dataframe_saved/'+region+'1/'+year+'_EWK_BKG_test_'+lep+'.root',key='Events')

del df_EWKBKG_train_valid_test
del df_EWKBKG_train_final
del df_EWKBKG_valid_final

df_QCD_train_final = df_QCD_train_valid_test[0].iloc[:int(final_Events_for_training),:]
df_QCD_train_valid_test[2] = df_QCD_train_valid_test[2].append(df_QCD_train_valid_test[0].iloc[int(final_Events_for_training):,:])

df_QCD_valid_final = df_QCD_train_valid_test[1].iloc[:int(final_Events_for_validatation),:]
df_QCD_train_valid_test[2] = df_QCD_train_valid_test[2].append(df_QCD_train_valid_test[1].iloc[int(final_Events_for_validatation):,:])
print("\n==========================================================")
print("QCD background")
print("train : ", df_QCD_train_final.shape, " valid : ", df_QCD_valid_final.shape, " test : ", df_QCD_train_valid_test[2].shape)

df_QCD_train_final.to_root('dataframe_saved/'+region+'1/'+year+'_QCD_BKG_train_'+lep+'.root',key='Events')
df_QCD_valid_final.to_root('dataframe_saved/'+region+'1/'+year+'_QCD_BKG_valid_'+lep+'.root',key='Events')
df_QCD_train_valid_test[2].to_root('dataframe_saved/'+region+'1/'+year+'_QCD_BKG_test_'+lep+'.root',key='Events')


del df_QCD_train_valid_test
del df_QCD_train_final
del df_QCD_valid_final
print("done")
