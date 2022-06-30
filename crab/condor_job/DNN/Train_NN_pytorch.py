import torch
import pandas as pd
import numpy as np
import ROOT as rt
from IPython.display import display
from torch.utils.data import TensorDataset, DataLoader
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime


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

def train_one_epoch(epoch_index, tb_writer, training_loader):
    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    for i, data in enumerate(training_loader):
        # Every data instance is an input + label pair
        inputs, labels = data

        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        outputs = model(inputs)

        # Compute the loss and its gradients
        #print(outputs.shape)
        #print(labels.long()[:,0])
        loss = loss_fn(outputs, labels.long()[:,0])
        loss.backward()

        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        if i % 1000 == 999:
            last_loss = running_loss / 1000 # loss per batch
            print('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.

    return last_loss

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

df_tr_top_signal = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_signal_train.root').AsNumpy()
df_tr_top_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_bkg_train.root').AsNumpy()
df_tr_EWK_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_EWK_BKG_train.root').AsNumpy()

df_val_top_signal = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_signal_valid.root').AsNumpy()
df_val_top_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_Top_bkg_valid.root').AsNumpy()
df_val_EWK_BKG = rt.RDataFrame("Events",'dataframe_saved/preVFP2016_EWK_BKG_valid.root').AsNumpy()

#display(df_tr_top_signal_new)

x_Sig_tr = np.vstack([df_tr_top_signal[var] for var in VARS]).T
x_Top_BKG_tr = np.vstack([df_tr_top_BKG[var] for var in VARS]).T
x_EWK_BKG_tr = np.vstack([df_tr_EWK_BKG[var] for var in VARS]).T
x_tr = np.vstack([x_Sig_tr, x_Top_BKG_tr, x_EWK_BKG_tr])
print("shape of x for training" ,x_tr.shape)

y_Sig_tr = np.vstack([0]*(x_Sig_tr.shape[0]))
y_Top_BKG_tr = np.vstack([1]*(x_Top_BKG_tr.shape[0]))
y_BKG_BKG_tr = np.vstack([2]*(x_EWK_BKG_tr.shape[0]))
y_tr = np.vstack([y_Sig_tr,y_Top_BKG_tr,y_BKG_BKG_tr]).astype(int)
print("shape of y for training", y_tr.shape)


x_Sig_val = np.vstack([df_val_top_signal[var] for var in VARS]).T
x_Top_BKG_val = np.vstack([df_val_top_BKG[var] for var in VARS]).T
x_EWK_BKG_val = np.vstack([df_val_EWK_BKG[var] for var in VARS]).T
x_val = np.vstack([x_Sig_val, x_Top_BKG_val, x_EWK_BKG_val])
print("shape of x for validation" ,x_val.shape)

y_Sig_val = np.vstack([0]*(x_Sig_val.shape[0]))
y_Top_BKG_val = np.vstack([1]*(x_Top_BKG_val.shape[0]))
y_BKG_BKG_val = np.vstack([2]*(x_EWK_BKG_val.shape[0]))
y_val = np.vstack([y_Sig_val,y_Top_BKG_val,y_BKG_BKG_val]).astype(int)
print("shape of y for validation", y_val.shape)

tensor_x_tr = torch.Tensor(x_tr) # transform to torch tensor
tensor_y_tr = torch.Tensor(y_tr)

tensor_x_val = torch.Tensor(x_val) # transform to torch tensor
tensor_y_val = torch.Tensor(y_val)

if torch.cuda.is_available():
    tensor_x_tr = tensor_x_tr.to("cuda")
    tensor_y_tr = tensor_y_tr.to("cuda")
    tensor_x_val = tensor_x_val.to("cuda")
    tensor_y_val = tensor_y_val.to("cuda")

train_dataset = TensorDataset(tensor_x_tr,tensor_y_tr) # create your datset
validation_dataset = TensorDataset(tensor_x_val,tensor_y_val)
training_loader = DataLoader(train_dataset, batch_size = 20, shuffle = True) # create your dataloader
validation_loader = DataLoader(validation_dataset, batch_size = 20, shuffle = True)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

model = NeuralNetwork().to(device)
print(model)

loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
writer = SummaryWriter('runs/fashion_trainer_{}'.format(timestamp))
epoch_number = 0

EPOCHS = 10

best_vloss = 1000000

for epoch in range(EPOCHS):
    print('EPOCH {}:'.format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer, training_loader)

    # We don't need gradients on to do reporting
    model.train(False)

    running_vloss = 0.0
    for i, vdata in enumerate(validation_loader):
        vinputs, vlabels = vdata
        voutputs = model(vinputs)
        vloss = loss_fn(voutputs, vlabels.long()[:,0])
        running_vloss += vloss

    avg_vloss = running_vloss / (i + 1)
    print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars('Training vs. Validation Loss',
                    { 'Training' : avg_loss, 'Validation' : avg_vloss },
                    epoch_number + 1)
    writer.flush()

    # Track best performance, and save the model's state
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        model_path = 'model_{}_{}'.format(timestamp, epoch_number)
        torch.save(model.state_dict(), model_path)

    epoch_number += 1





