import onnxruntime as ort
import uproot
import numpy as np
import math
import uproot_methods

# open the root file and get the desired tree
file = uproot.open("/pnfs/desy.de/cms/tier2/store/mc/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/70000/1F39E43A-2869-4540-8A95-B46F63B7D7B0.root")
tree = file["Events"]

# Get the desired arrays from the data
GenPart_pdgId = tree["GenPart_pdgId"].array()
GenPart_statusFlags = tree["GenPart_statusFlags"].array()
GenPart_pt = tree["GenPart_pt"].array()
GenPart_phi = tree["GenPart_phi"].array()
GenPart_eta = tree["GenPart_eta"].array()
GenPart_mass = tree["GenPart_mass"].array()


## create inference session using ort.InferenceSession from a given model
ort_sess = ort.InferenceSession('/afs/desy.de/user/v/vaguglie/saved_models/onnx/model12Down.onnx')
input_name = ort_sess.get_inputs()[0].name
label_name = ort_sess.get_outputs()[0].name

##Values that you have to set
hdamp = 1.379 ##This value is the value of hdamp of your NanoAOD divided by 172.5
maxM =  243.9517 ##This value is needed to normalise the mass of the particles in each event and comes from the maximum mass value we had in the training+validation sample

##Def of rapidity
def rapidity (eta, mass, pt):
    y = 0.5 * math.log((math.sqrt(mass**2 + pt**2 * math.cosh(eta)**2) + pt * math.sinh(eta)) / (math.sqrt(mass**2 + pt**2 * math.cosh(eta)**2) - pt * math.sinh(eta)))
    return y

# PDGid to small float dictionary
PID2FLOAT_MAP = {21: 0,
                 6: .1, -6: .2,
                 5: .3, -5: .4,
                 4: .5, -4: .6,
                 3: .7, -3: .8,
                 2: 0.9, -2: 1.0,
                 1: 1.1, -1: 1.2}

countTop = 0

# Loop over the entries
for jEntry in range(1000):
    print("Entry: ", jEntry)
    particlesvector=[]
    P0 = []

    # Loop on the genParticles, selecting only INITIAL top and antitop (considering parton shower) 
    for i in range(0, len(GenPart_pdgId[jEntry])):
        if GenPart_pdgId[jEntry][i] == 6:

            if (((GenPart_statusFlags[jEntry][i] >> 12) & 0x1) > 0):
                countTop += 1
                ptop = uproot_methods.TLorentzVector.from_ptetaphim(GenPart_pt[jEntry][i], GenPart_eta[jEntry][i], GenPart_phi[jEntry][i], GenPart_mass[jEntry][i])
        
        if GenPart_pdgId[jEntry][i] == -6:

            if (((GenPart_statusFlags[jEntry][i] >> 12) & 0x1) > 0):
                countTop += 1
                patop = uproot_methods.TLorentzVector.from_ptetaphim(GenPart_pt[jEntry][i], GenPart_eta[jEntry][i], GenPart_phi[jEntry][i], GenPart_mass[jEntry][i])
   
    # Creating the array with all info needed to pass to the NN model, already normalised
    
    particlesvector.append([math.log10(ptop.pt), rapidity(ptop.eta, ptop.mass, ptop.pt), ptop.phi, ptop.mass/maxM, PID2FLOAT_MAP.get(6, 0), hdamp])
    particlesvector.append([math.log10(patop.pt), rapidity(patop.eta, patop.mass, patop.pt), patop.phi, patop.mass/maxM, PID2FLOAT_MAP.get(-6, 0), hdamp])
    P0.append(particlesvector)
    P0=np.array(P0)
    print(P0.shape)
    print(P0)

    p_tt = ptop + patop

    ## run inference
    pred = ort_sess.run([label_name], {input_name: P0.astype(np.float32)})[0]
    if (p_tt.pt<1000):
        weight = pred[:,0]/pred[:,1]
    else:
        weight = 1.0
     
print('countTop:'+str(countTop))
