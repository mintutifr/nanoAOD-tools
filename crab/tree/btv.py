#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

btagSF2016preVFP = lambda: btagSFProducer("UL2016preVFP",'deepjet', ['shape_corr'])
btagSF2016postVFP = lambda: btagSFProducer("UL2016postVFP",'deepjet', ['shape_corr'])
btagSF2017 = lambda: btagSFProducer("UL2017",'deepjet', ['L','M','T','shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer
btagSF2018 = lambda: btagSFProducer("UL2018",'deepjet', ['L','M','T','shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer

