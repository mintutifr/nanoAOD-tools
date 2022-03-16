import ROOT

# from within CMSSW:
#ROOT.gSystem.Load('libCondFormatsBTauObjects')
#ROOT.gSystem.Load('libCondToolsBTau')

# OR using standalone code:
ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

# get the sf data loaded
calib = ROOT.BTagCalibration ('deepjet', '/afs/cern.ch/work/m/mikumar/private/NanoAOD_new/CMSSW_10_6_0/src/PhysicsTools/NanoAODTools/data/btagSF/DeepJet_106XUL17SF_V2p1.csv')

v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

# make a reader instance and load the sf data

reader = ROOT.BTagCalibrationReader (
    3,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
) 


reader.load(
    calib,
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG
    "comb"      # measurement type
)

# in your event loop
sf = reader.eval_auto_bounds(
    'central',      # systematic (here also 'up'/'down' possible)
    0,              # jet flavor
    1.2,            # absolute value of eta
    31.             # pt
)

print sf 
