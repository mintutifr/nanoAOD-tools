#source /cvmfs/cms.cern.ch/cmsset_default.sh
#source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
import sys, os
import argparse as arg

parser = arg.ArgumentParser(description='inputs discription')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, nargs=1, help="lepton [ el  mu ]")
parser.add_argument('-y', '--year  ', dest='year', type=str, nargs=1, help="Year [ ULpreVFP2016  ULpostVFP2016  UL2017  UL2018 ]")
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

print(args)

lep = args.lepton[0]
year= args.year[0]

if(lep=="mu"):
	lepton = "Muon"
elif(lep=="el"):
        lepton = "Electron"
print(lepton)


import torch
import pandas as pd
import numpy as np
import ROOT as rt
from IPython.display import display
from torch.utils.data import TensorDataset, DataLoader
from torch.optim.lr_scheduler import MultiStepLR
from torch import nn
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

def distance_corr(var_1,var_2,normedweight,power=2):
    """var_1: First variable to decorrelate (eg mass)
    var_2: Second variable to decorrelate (eg classifier output)
    normedweight: Per-example weight. Sum of weights should add up to N (where N is the number of examples)
    power: Exponent used in calculating the distance correlation
    
    va1_1, var_2 and normedweight should all be 1D torch tensors with the same number of entries
    
    Usage: Add to your loss function. total_loss = BCE_loss + lambda * distance_corr
    """
    
    
    xx = var_1.view(-1, 1).repeat(1, len(var_1)).view(len(var_1),len(var_1))
    yy = var_1.repeat(len(var_1),1).view(len(var_1),len(var_1))
    amat = (xx-yy).abs()

    xx = var_2.view(-1, 1).repeat(1, len(var_2)).view(len(var_2),len(var_2))
    yy = var_2.repeat(len(var_2),1).view(len(var_2),len(var_2))
    bmat = (xx-yy).abs()

    amatavg = torch.mean(amat*normedweight,dim=1)
    Amat=amat-amatavg.repeat(len(var_1),1).view(len(var_1),len(var_1))\
        -amatavg.view(-1, 1).repeat(1, len(var_1)).view(len(var_1),len(var_1))\
        +torch.mean(amatavg*normedweight)

    bmatavg = torch.mean(bmat*normedweight,dim=1)
    Bmat=bmat-bmatavg.repeat(len(var_2),1).view(len(var_2),len(var_2))\
        -bmatavg.view(-1, 1).repeat(1, len(var_2)).view(len(var_2),len(var_2))\
        +torch.mean(bmatavg*normedweight)

    ABavg = torch.mean(Amat*Bmat*normedweight,dim=1)
    AAavg = torch.mean(Amat*Amat*normedweight,dim=1)
    BBavg = torch.mean(Bmat*Bmat*normedweight,dim=1)

    if(power==1):
        dCorr=(torch.mean(ABavg*normedweight))/torch.sqrt((torch.mean(AAavg*normedweight)*torch.mean(BBavg*normedweight)))
    elif(power==2):
        dCorr=(torch.mean(ABavg*normedweight))**2/(torch.mean(AAavg*normedweight)*torch.mean(BBavg*normedweight))
    else:
        dCorr=((torch.mean(ABavg*normedweight))/torch.sqrt((torch.mean(AAavg*normedweight)*torch.mean(BBavg*normedweight))))**power
    
    return dCorr


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        #self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(18, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 6),
            nn.LogSoftmax(dim=1),
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
        inputs, labels1 = data

        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        outputs = model(inputs)
        labels = labels1[:,0]
        # Compute the loss and its gradients
        loss = loss_fn(outputs, labels.long()) + lamda * distance_corr(labels1[:,1],torch.exp(outputs[:,1]), labels1[:,2]) +  lamda * distance_corr(labels1[:,1],torch.exp(outputs[:,2]), labels1[:,2]) +  lamda * distance_corr(labels1[:,1],torch.exp(outputs[:,3]), labels1[:,2]) +  lamda * distance_corr(labels1[:,1],torch.exp(outputs[:,4]), labels1[:,2]) +  lamda * distance_corr(labels1[:,1],torch.exp(outputs[:,5]), labels1[:,2])
        loss.backward()
        #print(loss)
        # Adjust learning weights
        optimizer.step()

        # Gather data and report
        running_loss += loss.item()
        if i % 1000 == 999:
            last_loss = running_loss / 1000 # loss per batch
            #print('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(training_loader) + i + 1
            tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.

    return last_loss

VARS = [lepton+'Eta', lepton+'Pt', lepton+'Phi', lepton+'E',
        'lJetEta', 'lJetPt', 'lJetPhi', 'lJetMass',
        'bJetEta', 'bJetPt', 'bJetPhi', 'bJetMass',
        'Px_nu', 'Py_nu', 'Pz_nu',
        'FW1', 'bJetdeepJet', 'lJetdeepJet',
        ]

train_ch = ['WS_Top_signal', 'Top_signal', 'Top_bkg', 'WS_Top_bkg', 'EWK_BKG', 'QCD_BKG']
df_train={}
df_val = {}
x_tr_ch = {}
y_tr_ch = {}
x_val_ch = {}
y_val_ch = {}

n_tr = 50000
n_val = 10000
dir='dataframe_saved/'
for count, channel in enumerate(train_ch):	
    print("Events",dir+year+'_' + channel + '_train_'+lep+'.root')
    df_train[channel] = rt.RDataFrame("Events",dir+year+'_' + channel + '_train_'+lep+'.root').AsNumpy()
    df_val[channel] = rt.RDataFrame("Events",dir+year+'_' + channel + '_valid_'+lep+'.root').AsNumpy()
    x_tr_ch[channel] = np.vstack([df_train[channel][var] for var in VARS]).T
    x_val_ch[channel] = np.vstack([df_val[channel][var] for var in VARS]).T
    print("shape of x for training " + channel + " " , np.shape(x_tr_ch[channel]))
    print("shape of x for validation " + channel + " " , x_val_ch[channel].shape)
    #sel_tr = np.random.choice(x_tr_ch[channel].shape[0], n_tr, replace=False)
    #sel_val = np.random.choice(x_val_ch[channel].shape[0], n_val, replace=False)
    print(np.shape(df_train[channel]['topMass']))
    y_tr_ch[channel] = np.vstack([np.array([count]*(x_tr_ch[channel].shape[0])), df_train[channel]['topMass'], np.array([1]*(x_tr_ch[channel].shape[0]))]).T 
    y_val_ch[channel] = np.vstack([np.array([count]*(x_val_ch[channel].shape[0])), df_val[channel]['topMass'], np.array([1]*(x_val_ch[channel].shape[0]))]).T
    if count == 0:
        x_tr = np.vstack([x_tr_ch[channel]])
        y_tr = np.vstack([y_tr_ch[channel]])
        x_val = np.vstack([x_val_ch[channel]])
        y_val = np.vstack([y_val_ch[channel]])
    else:
        x_tr = np.vstack([x_tr, x_tr_ch[channel]])
        y_tr = np.vstack([y_tr, y_tr_ch[channel]])
        x_val = np.vstack([x_val, x_val_ch[channel]])
        y_val = np.vstack([y_val, y_val_ch[channel]])

print("shape of x for training" ,x_tr.shape)

print("shape of x for validation" ,x_val.shape)

print("shape of y for validation", y_val.shape)

tensor_x_tr = torch.Tensor(x_tr) # transform to torch tensor
tensor_y_tr = torch.Tensor(y_tr)

tensor_x_val = torch.Tensor(x_val) # transform to torch tensor
tensor_y_val = torch.Tensor(y_val)

device = "cuda:3" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

if torch.cuda.is_available():
    tensor_x_tr = tensor_x_tr.to(device)
    tensor_y_tr = tensor_y_tr.to(device)
    tensor_x_val = tensor_x_val.to(device)
    tensor_y_val = tensor_y_val.to(device)

batch = 40
train_dataset = TensorDataset(tensor_x_tr,tensor_y_tr) # create your datset
validation_dataset = TensorDataset(tensor_x_val,tensor_y_val)
training_loader = DataLoader(train_dataset, batch_size = batch, shuffle = True) # create your dataloader
validation_loader = DataLoader(validation_dataset, batch_size = batch, shuffle = True)


model = NeuralNetwork().to(device)
print(model)

#loss_fn = torch.nn.CrossEntropyLoss()
loss_fn = torch.nn.NLLLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
scheduler = MultiStepLR(optimizer, milestones=[30,40], gamma=0.2)


timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
writer = SummaryWriter('runs/fashion_trainer_{}'.format(timestamp))
epoch_number = 0

EPOCHS = 50
lamda = 0.5
best_vloss = 1000000
f = open('loss'+year+'_'+lep+'.csv', 'w')
for epoch in range(EPOCHS):
    #print('EPOCH {}:'.format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer, training_loader)

    # We don't need gradients on to do reporting
    model.train(False)

    running_vloss = 0.0
    for i, vdata in enumerate(validation_loader):
        vinputs, vlabels1 = vdata
        voutputs = model(vinputs)
        vlabels = vlabels1[:,0]
        vloss = loss_fn(voutputs, vlabels.long()) + lamda * distance_corr(vlabels1[:,1],torch.exp(voutputs[:,1]),vlabels1[:,2]) + lamda * distance_corr(vlabels1[:,1],torch.exp(voutputs[:,2]),vlabels1[:,2]) + lamda * distance_corr(vlabels1[:,1],torch.exp(voutputs[:,3]),vlabels1[:,2]) + lamda * distance_corr(vlabels1[:,1],torch.exp(voutputs[:,4]),vlabels1[:,2]) + lamda * distance_corr(vlabels1[:,1],torch.exp(voutputs[:,5]),vlabels1[:,2])
        #print(distance_corr(vlabels1[:,1],torch.exp(voutputs[:,1]),vlabels1[:,2]))
        running_vloss += vloss

    avg_vloss = running_vloss / (i + 1)
    #print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))
    print(str(epoch) + ',' + str(avg_loss) + ',' +str(avg_vloss.item()))
    f.write(str(epoch) + ',' + str(avg_loss) + ',' +str(avg_vloss.item()) + '\n')
    scheduler.step()
    # Log the running loss averaged per batch
    # for both training and validation
    writer.add_scalars('Training vs. Validation Loss',
                    { 'Training' : avg_loss, 'Validation' : avg_vloss },
                    epoch_number + 1)
    writer.flush()

    # Track best performance, and save the model's state
    if avg_vloss < best_vloss:
        best_vloss = avg_vloss
        wightpath = 'weight/'+year+'/'+lep
        if not os.path.exists(wightpath): 
            os.makedirs(wightpath)
        model_path = wightpath+'/model_{}_{}'.format(timestamp, epoch_number)
        torch.save(model.state_dict(), model_path)

    epoch_number += 1
f.close()




