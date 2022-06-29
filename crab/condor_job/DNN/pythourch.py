import torch
import pandas as pd
import numpy as np
import ROOT as rt
from IPython.display import display
from torch.utils.data import TensorDataset, DataLoader
from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        #self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(9, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 3),
        )

    def forward(self, x):
        #x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits



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

df_top_signal = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_signal.root').AsNumpy()
df_top_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_bkg.root').AsNumpy()
df_EWK_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_EWK_BKG.root').AsNumpy()

#df_top_signal_new = df_top_signal[df_top_signal['__index__']>=5] #df[df['Age'] >= 37]    
display(df_top_signal_new)

x_Sig = np.vstack([df_top_signal[var] for var in VARS]).T
x_Top_BKG = np.vstack([df_top_BKG[var] for var in VARS]).T
x_EWK_BKG = np.vstack([df_EWK_BKG[var] for var in VARS]).T
x = np.vstack([x_Sig, x_Top_BKG, x_EWK_BKG])
print("shape of x" ,x.shape)

y_Sig = np.vstack([[1,0,0]]*(x_Sig.shape[0]))
y_Top_BKG = np.vstack([[1,0,0]]*(x_Top_BKG.shape[0]))
y_BKG_BKG = np.vstack([[1,0,0]]*(x_EWK_BKG.shape[0]))
y = np.vstack([y_Sig,y_Top_BKG,y_BKG_BKG])
print("shape of x", y.shape)

tensor_x = torch.Tensor(x) # transform to torch tensor
tensor_y = torch.Tensor(y)

if torch.cuda.is_available():
    tensor_x = tensor_x.to("cuda")
    tensor_y = tensor_y.to("cuda")

my_dataset = TensorDataset(tensor_x,tensor_y) # create your datset
my_dataloader = DataLoader(my_dataset, batch_size = 12, shuffle = True) # create your dataloader

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

model = NeuralNetwork().to(device)
print(model)

loss_fn = torch.nn.CrossEntropyLoss()
