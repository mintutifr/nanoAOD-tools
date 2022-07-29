#from __future__ import print_function
from loader import *
import ROOT 
import numpy as np  
import pandas as pd
import root_pandas as rpd
import root_numpy 
import sys, os
from IPython.display import display
import glob
from time import time

channels = ['Tchannel', 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTolnulnu', 'WZTo2Q2L', 'ZZTo2Q2L', 'DataULpreVFP2016']

datasets = []                                            # this object will be a list of list
for channel in channels:
        datasets.append(load_dataset(-1,channel, "mu")) #apped all data frames in datasets

#bjet_deepjet_score = [] 
corr_assig = []
for channel_no in range(0,7):#len(channels)-1): 
        assig_channel = []
        Jet_partonFlavour_channel = datasets[channel_no]["Jet_partonFlavour"]  # get Jet_partonFlavour from the list of dataframes
        nbjet_sel_channel = datasets[channel_no]["nbjet_sel"]
        lepton_charge_channel = datasets[channel_no]["MuonCharge"]
        for i in range (0,len(datasets[channel_no]["MuonEta"])): #loop over all events per channel since outer loop is over channels
                        if(Jet_partonFlavour_channel[i][nbjet_sel_channel[i]]*lepton_charge_channel[i]==5):
                                assig_channel.append(1) # this need not be done for each channel we suppose to do it for only Tchannel and Tbarchannel 
                        else:
                                assig_channel.append(0)
        corr_assig.append(assig_channel)
        del Jet_partonFlavour_channel
        del assig_channel
        del nbjet_sel_channel
        del lepton_charge_channel
        


VARS = ['MuonEta', 'MuonPt', 'MuonPhi', 'MuonE',   'MuonCharge',
        'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        'Px_nu', 'Py_nu', 'Pz_nu',
        'dEta_mu_lJet', 'dEta_mu_bJet',
        'dPhi_mu_lJet', 'dPhi_mu_bJet',
        'mtwMass',
        'dR_bJet_lJet',
        'abs_lJetEta',
        'jetpTSum',
        'diJetMass',
        'cosThetaStar',
        'FW1',
        'bJetdeepJet',
        'lJetdeepJet',
        'Xsec_wgt',
        'LHEWeightSign',
        'L1PreFiringWeight_Nom',
        'event'
        ]

df = {}  # remember this will be list of dataframe

for channel_no,channel  in enumerate(channels): #channels: #try to enumare funchtion to remove channel_no in this loop
     if("Data" not in channel):
        df[channel] = pd.DataFrame(datasets[channel_no],columns=VARS) #adding dataframes in the list
        if( channel in ['Tchannel', 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic']):
              df[channel]['Assig'] = np.asarray(corr_assig[channel_no]) # adding new variable in each dataframe of a given channel 
     else:
        VARS.remove("Xsec_wgt")
        VARS.remove("LHEWeightSign")
        df[channel] = pd.DataFrame(datasets[channel_no],columns=VARS) #adding dataframes in the list

del datasets
del corr_assig #this has been added

#defin dec to store info channel wise
df_train = {}
df_valid = {}
df_test = {}

#loop to devide sample in train, valid and test
for channel in channels:
        Entries = df[channel].shape[0]
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

print "\n=========================================================="    
print "full signal"
print "train : ", df_signal_train_valid_test[0].shape, "valid : ", df_signal_train_valid_test[1].shape, "test : ", df_signal_train_valid_test[2].shape

del df_signal_train_valid_test # delet the full datafrm for full sample since it aleady split in correct and wrong assignment list this was created just to check consitancy

print "only correct assignment signal"
print "train : ", df_signal_train_valid_test_correct_assign[0].shape, "valid : ", df_signal_train_valid_test_correct_assign[1].shape, "test : ", df_signal_train_valid_test_correct_assign[2].shape

print "only wrong assignment signal"
print "train : ", df_signal_train_valid_test_wrong_assign[0].shape, "valid : ", df_signal_train_valid_test_wrong_assign[1].shape, "test : ", df_signal_train_valid_test_wrong_assign[2].shape


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
 
print "\n=========================================================="
print "full Top background"
print "train : ", df_TopBKG_train_valid_test[0].shape, " valid : ", df_TopBKG_train_valid_test[1].shape, " test : ", df_TopBKG_train_valid_test[2].shape

del df_TopBKG_train_valid_test # delet the full datafrm for full sample since it aleady split in correct and wrong assignment list this was created just to check consitancy

print "only correct assignment signal"
print "train : ", df_TopBKG_train_valid_test_correct_assign[0].shape, "valid : ", df_TopBKG_train_valid_test_correct_assign[1].shape, "test : ", df_TopBKG_train_valid_test_correct_assign[2].shape

print "only wrong assignment signal"
print "train : ", df_TopBKG_train_valid_test_wrong_assign[0].shape, "valid : ", df_TopBKG_train_valid_test_wrong_assign[1].shape, "test : ", df_TopBKG_train_valid_test_wrong_assign[2].shape



df_EWKBKG_train_valid_test = []  #define a new list for train test and validation
for i,df in enumerate([df_train,df_valid,df_test]):
    df_temp = pd.concat([df['WJetsToLNu_0J'],df['WJetsToLNu_1J'],df['WJetsToLNu_2J'],df['DYJets'],df['WWTolnulnu'],df['WZTo2Q2L'],df['ZZTo2Q2L']]) # adding all EWK bkg and push to a temp df
    df_EWKBKG_train_valid_test.append(df_temp)
    del df_temp # #delete temp df

df_QCD_train_valid_test = []  #define a new list for train test and validation
for i,df in enumerate([df_train,df_valid,df_test]):
    df_QCD_train_valid_test.append(df['DataULpreVFP2016'])

del df_train,df_valid,df_test # deleting datadames since the full information already absorbed in signal and backgrounds

print "\n=========================================================="
print "EWK background"
print "train : ", df_EWKBKG_train_valid_test[0].shape, " valid : ", df_EWKBKG_train_valid_test[1].shape, " test : ", df_EWKBKG_train_valid_test[2].shape

#print "df_top_signal_corre_aaign : ",df_top_signal_correct_assign_new

print "\n========================== saving dataframes in root files ================================"


df_signal_train_valid_test_wrong_assign[0].to_root('dataframe_saved/preVFP2016_WS_Top_signal_train.root',key='Events') # write df in root file
df_signal_train_valid_test_wrong_assign[1].to_root('dataframe_saved/preVFP2016_WS_Top_signal_valid.root',key='Events')
df_signal_train_valid_test_wrong_assign[2].to_root('dataframe_saved/preVFP2016_WS_Top_signal_test.root',key='Events')

del df_signal_train_valid_test_wrong_assign # delete this dataframe since information is alreadyadded to new list of top backgrounds df



df_signal_train_valid_test_correct_assign[0].to_root('dataframe_saved/preVFP2016_Top_signal_train.root',key='Events') # write df in root file
df_signal_train_valid_test_correct_assign[1].to_root('dataframe_saved/preVFP2016_Top_signal_valid.root',key='Events')
df_signal_train_valid_test_correct_assign[2].to_root('dataframe_saved/preVFP2016_Top_signal_test.root',key='Events')

del df_signal_train_valid_test_correct_assign

df_TopBKG_train_valid_test_correct_assign[0].to_root('dataframe_saved/preVFP2016_Top_bkg_train.root',key='Events')
df_TopBKG_train_valid_test_correct_assign[1].to_root('dataframe_saved/preVFP2016_Top_bkg_valid.root',key='Events')
df_TopBKG_train_valid_test_correct_assign[2].to_root('dataframe_saved/preVFP2016_Top_bkg_test.root',key='Events')

del df_TopBKG_train_valid_test_correct_assign

df_TopBKG_train_valid_test_wrong_assign[0].to_root('dataframe_saved/preVFP2016_WS_Top_bkg_train.root',key='Events')
df_TopBKG_train_valid_test_wrong_assign[1].to_root('dataframe_saved/preVFP2016_WS_Top_bkg_valid.root',key='Events')
df_TopBKG_train_valid_test_wrong_assign[2].to_root('dataframe_saved/preVFP2016_WS_Top_bkg_test.root',key='Events')

del df_TopBKG_train_valid_test_wrong_assign


df_EWKBKG_train_valid_test[0].to_root('dataframe_saved/preVFP2016_EWK_BKG_train.root',key='Events')
df_EWKBKG_train_valid_test[1].to_root('dataframe_saved/preVFP2016_EWK_BKG_valid.root',key='Events')
df_EWKBKG_train_valid_test[2].to_root('dataframe_saved/preVFP2016_EWK_BKG_test.root',key='Events')

del df_EWKBKG_train_valid_test


df_QCD_train_valid_test[0].to_root('dataframe_saved/preVFP2016_QCD_BKG_train.root',key='Events')
df_QCD_train_valid_test[1].to_root('dataframe_saved/preVFP2016_QCD_BKG_valid.root',key='Events')
df_QCD_train_valid_test[2].to_root('dataframe_saved/preVFP2016_QCD_BKG_test.root',key='Events')

del df_QCD_train_valid_test

print("done")
