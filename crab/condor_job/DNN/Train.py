#from __future__ import print_function
from loader import *
import ROOT 
import numpy as np  
import pandas as pd
import root_numpy 
import sys
from IPython.display import display

dataset_Tchannel = load_dataset(10000,"Tchannel", "mu")
dataset_ttbar = load_dataset(10000,"ttbar_FullyLeptonic", "mu")
#dataset_WToLNu_2J = load_dataset(10000, "WJetsToLNu_2J" ,"mu")

Muon_Eta_tchannel = dataset_Tchannel ["MuonEta"]
Muon_Eta_ttbar = dataset_ttbar ["MuonEta"]
#print(Muon_Eta_tchannel)
Jet_btagDeepFlavB_Tchannel = dataset_Tchannel ["Jet_btagDeepFlavB"]
nbjet_sel_Tchannel = dataset_Tchannel ["nbjet_sel"]

Jet_btagDeepFlavB_ttbar = dataset_ttbar ["Jet_btagDeepFlavB"]
nbjet_sel_ttbar = dataset_ttbar ["nbjet_sel"]

bjet_deepjet_score_tchannel = []
bjet_deepjet_score_ttbar = []

for i in range (0,len(Muon_Eta_tchannel)):
    if not len(Jet_btagDeepFlavB_Tchannel[i]) == 0:
        bjet_deepjet_score_tchannel.append(Jet_btagDeepFlavB_Tchannel[i][nbjet_sel_Tchannel[i]])
    else:   
        bjet_deepjet_score_tchannel.append(-1)
    
for i in range (0,len(Muon_Eta_ttbar)):
    if not len(Jet_btagDeepFlavB_ttbar[i]) == 0:
        bjet_deepjet_score_ttbar.append(Jet_btagDeepFlavB_ttbar[i][nbjet_sel_ttbar[i]])
    else:
        bjet_deepjet_score_ttbar.append(-1)

del nbjet_sel_Tchannel
del Jet_btagDeepFlavB_Tchannel

del nbjet_sel_ttbar
del Jet_btagDeepFlavB_ttbar

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

df['t_channel'] = pd.DataFrame(dataset_Tchannel,columns=VARS)
df['t_channel']['deepJet_score_b']= np.asarray(bjet_deepjet_score_tchannel)

df['ttbar'] = pd.DataFrame(dataset_ttbar,columns=VARS)
df['ttbar']['deepJet_score_b']= np.asarray(bjet_deepjet_score_ttbar)

#display(df)

#KERAS#

from keras.models import Sequential, Model
from keras.layers import Input, Activation, Dense, Convolution2D, MaxPooling2D, Dropout, Flatten
from keras.constraints import max_norm

model = Sequential()

NDIM = len(VARS)+1

model.add(Dense(240, kernel_initializer='glorot_normal', activation='relu', input_dim=NDIM))
model.add(Dense(120, kernel_initializer='glorot_normal', activation='relu', kernel_constraint=max_norm(1.)))
model.add(Dense(60, kernel_initializer='glorot_normal', activation='relu', kernel_constraint=max_norm(1.)))
model.add(Dense(4, kernel_initializer='glorot_normal', activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.summary()

print("done")
