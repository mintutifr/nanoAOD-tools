#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

btagSF2016 = lambda: btagSFProducer("2016",'deepcsv', ['L','M','T','shape_corr'])
btagSF2017 = lambda: btagSFProducer("2017",'deepcsv', ['L','M','T','shape_corr'])

