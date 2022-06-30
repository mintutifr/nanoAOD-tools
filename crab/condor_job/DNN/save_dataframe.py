#from __future__ import print_function
from loader import *
import ROOT 
import numpy as np  
import pandas as pd
import root_pandas as rpd
import root_numpy 
import sys
from IPython.display import display

channels = ['Tchannel', 'Tbarchannel','tw_top', 'tw_antitop', 'Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic', 'WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJets', 'WWTolnulnu', 'WZTo2Q2L', 'ZZTo2Q2L', 'QCD']

datasets = []
for channel in channels:
        datasets.append(load_dataset(1000,channel, "mu"))

bjet_deepjet_score = []
corr_assig = []
for channel_no in range(0,len(channels)):
        corr_assig_channel = []
        bjet_deepjet_score_channel = []
        Jet_btagDeepFlavB_channel = datasets[channel_no]["Jet_btagDeepFlavB"]
        Jet_partonFlavour_channel = datasets[channel_no]["Jet_partonFlavour"]
        nbjet_sel_channel = datasets[channel_no]["nbjet_sel"]
        bJethadronFlavour_channel = datasets[channel_no]["bJethadronFlavour"] 
        lepton_channel = datasets[channel_no]["MuonCharge"]
        #Event_channel = datasets[channel_no]["event"]
        for i in range (0,len(datasets[channel_no]["MuonEta"])):
                if not len(Jet_btagDeepFlavB_channel[i]) == 0:
                        bjet_deepjet_score_channel.append(Jet_btagDeepFlavB_channel[i][nbjet_sel_channel[i]])
                        if(Jet_partonFlavour_channel[i][nbjet_sel_channel[i]]*lepton_channel[i]==5):
                                corr_assig_channel.append(1) 
                        else:
                                corr_assig_channel.append(0)
                                #print Event_channel[i]," : ",bJethadronFlavour_channel[i]," : ",lepton_channel[i]
                else:
                        bjet_deepjet_score_channel.append(-1)
        bjet_deepjet_score.append(bjet_deepjet_score_channel)
        corr_assig.append(corr_assig_channel)
        del Jet_partonFlavour_channel
        del corr_assig_channel
        del bjet_deepjet_score_channel
        del Jet_btagDeepFlavB_channel
        del nbjet_sel_channel
        del bJethadronFlavour_channel
        del lepton_channel
        

    

VARS = ['MuonEta',
        'dEta_mu_bJet',
        'mtwMass',
        'abs_lJetEta',
        'jetpTSum',
        'diJetMass',
        'cosThetaStar',
        'dR_bJet_lJet',
        'FW1',
        ]

df = {}

channel_no=0
for channel in channels:
        df[channel] = pd.DataFrame(datasets[channel_no],columns=VARS)
        df[channel]['deepJet_score_b'] = np.asarray(bjet_deepjet_score[channel_no])
        df[channel]['Assig'] = np.asarray(corr_assig[channel_no])
        channel_no=channel_no+1
del datasets
del bjet_deepjet_score
del corr_assig


df_train = {}
df_valid = {}
df_test = {}

for channel in channels:
        Entries = df[channel].shape[0]
        df_train[channel] = df[channel].iloc[:int(Entries/2),:]
        df_valid[channel] = df[channel].iloc[int(Entries/2):int(3*Entries/4),:]
        df_test[channel] = df[channel].iloc[int(3*Entries/4):,:]
        print("total = ", df[channel].shape[0], " df_train = ", df_train[channel].shape[0], " df_valid = ",df_valid[channel].shape[0]," df_test = ",df_test[channel].shape[0])

del df

df_samples_train_valid_test = []
df_samples_train_valid_test_correct_assign = []
df_samples_train_valid_test_wrong_assign = []

for df in [df_train,df_valid,df_test]:
	df_temp = pd.concat([df['Tchannel'],df['Tbarchannel']])
	df_samples_train_valid_test.append(df_temp)
        df_temp_correct_assign = df_temp.query('Assig==1',inplace = False)
        df_samples_train_valid_test_correct_assign.append(df_temp_correct_assign)
        del df_temp_correct_assign
        df_temp_wrong_assign = df_temp.query('Assig==0',inplace = False)
        df_samples_train_valid_test_wrong_assign.append(df_temp_wrong_assign)
        del df_temp_wrong_assign
        del df_temp
    
print "full sample"
print "train : ", df_samples_train_valid_test[0].shape, "valid : ", df_samples_train_valid_test[1].shape, "test : ", df_samples_train_valid_test[2].shape

print "only correct assignment"
print "train : ", df_samples_train_valid_test_correct_assign[0].shape, "valid : ", df_samples_train_valid_test_correct_assign[1].shape, "test : ", df_samples_train_valid_test_correct_assign[2].shape

print "only wrong assignment"
print "train : ", df_samples_train_valid_test_wrong_assign[0].shape, "valid : ", df_samples_train_valid_test_wrong_assign[1].shape, "test : ", df_samples_train_valid_test_wrong_assign[2].shape


#print "df_top_signal_train : ",df_top_signal_train.shape, " df_top_signal_valid : ",df_top_signal_valid.shape, "df_top_signal_test : ",df_top_signal_test.shape
#print "df_top_signal_correct_assign_train : ",df_top_signal_correct_assign_train.shape,"df_top_signal_correct_assign_valid : ",df_top_signal_correct_assign_valid.shape,"df_top_signal_correct_assign_test : ",df_top_signal_correct_assign_test.shape
#print "df_top_signal_wrong_assign_train : ",df_top_signal_wrong_assign_train.shape,"df_top_signal_wrong_assign_valid : ",df_top_signal_wrong_assign_valid.shape,"df_top_signal_wrong_assign_test : ",df_top_signal_wrong_assign_test.shape

df_top_BKG_train = pd.concat([df_train['tw_top'],df_train['tw_antitop'],df_train['Schannel'],df_train['ttbar_SemiLeptonic'],df_train['ttbar_FullyLeptonic'],df_top_signal_wrong_assign_train])
df_top_BKG_valid = pd.concat([df_valid['tw_top'],df_valid['tw_antitop'],df_valid['Schannel'],df_valid['ttbar_SemiLeptonic'],df_valid['ttbar_FullyLeptonic'],df_top_signal_wrong_assign_valid])
df_top_BKG_test = pd.concat([df_test['tw_top'],df_test['tw_antitop'],df_test['Schannel'],df_test['ttbar_SemiLeptonic'],df_test['ttbar_FullyLeptonic'],df_top_signal_wrong_assign_test])



df_EWK_BKG_train = pd.concat([df_train['WJetsToLNu_0J'],df_train['WJetsToLNu_1J'],df_train['WJetsToLNu_2J'],df_train['DYJets'],df_train['WWTolnulnu'],df_train['WZTo2Q2L'],df_train['ZZTo2Q2L']])
df_EWK_BKG_valid = pd.concat([df_valid['WJetsToLNu_0J'],df_valid['WJetsToLNu_1J'],df_valid['WJetsToLNu_2J'],df_valid['DYJets'],df_valid['WWTolnulnu'],df_valid['WZTo2Q2L'],df_valid['ZZTo2Q2L']])
df_EWK_BKG_test = pd.concat([df_test['WJetsToLNu_0J'],df_test['WJetsToLNu_1J'],df_test['WJetsToLNu_2J'],df_test['DYJets'],df_test['WWTolnulnu'],df_test['WZTo2Q2L'],df_test['ZZTo2Q2L']])
#print(type(df_top_signal),df_top_signal.columns.tolist())


#print "df_top_signal_corre_aaign : ",df_top_signal_correct_assign_new

df_top_signal_correct_assign_train.to_root('dataframe_saved/preVFP2016_Top_signal_train.root',key='Events')
df_top_signal_correct_assign_valid.to_root('dataframe_saved/preVFP2016_Top_signal_valid.root',key='Events')
df_top_signal_correct_assign_test.to_root('dataframe_saved/preVFP2016_Top_signal_test.root',key='Events')

df_top_BKG_train.to_root('dataframe_saved/preVFP2016_Top_bkg_train.root',key='Events')
df_top_BKG_valid.to_root('dataframe_saved/preVFP2016_Top_bkg_valid.root',key='Events')
df_top_BKG_test.to_root('dataframe_saved/preVFP2016_Top_bkg_test.root',key='Events')

df_EWK_BKG_train.to_root('dataframe_saved/preVFP2016_EWK_BKG_train.root',key='Events')
df_EWK_BKG_valid.to_root('dataframe_saved/preVFP2016_EWK_BKG_valid.root',key='Events')
df_EWK_BKG_test.to_root('dataframe_saved/preVFP2016_EWK_BKG_test.root',key='Events')

del df_top_signal_correct_assign_train
del df_top_signal_wrong_assign_train
del df_top_signal_train
del df_top_BKG_train
del df_EWK_BKG_train

del df_top_signal_correct_assign_valid
del df_top_signal_wrong_assign_valid
del df_top_signal_valid
del df_top_BKG_valid
del df_EWK_BKG_valid

del df_top_signal_correct_assign_test
del df_top_signal_wrong_assign_test
del df_top_signal_test
del df_top_BKG_test
del df_EWK_BKG_test

#KERAS#

"""from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dense, Convolution2D, MaxPooling2D, Dropout, Flatten
from keras.constraints import max_norm

model = Sequential()

NDIM = len(VARS)+1

model.add(Dense(240, kernel_initializer='glorot_normal', activation='relu', input_dim=NDIM))
model.add(Dense(120, kernel_initializer='glorot_normal', activation='relu', kernel_constraint=max_norm(1.)))
model.add(Dense(60, kernel_initializer='glorot_normal', activation='relu', kernel_constraint=max_norm(1.)))
model.add(Dense(4, kernel_initializer='glorot_normal', activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.summary()"""

print("done")
