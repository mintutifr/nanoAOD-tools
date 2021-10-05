1. Genral

	Jme Module check the recomdation file 

2. Specific

     1. Btagging evoluvation

     		#EfficiencyModule.py
     		1. Check the efficiency are calculted with the recommaded lose, midium and tight criteria  at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation"
		2. check we are using correct Module producer while creating efficiency file "EfficiencyConstr_2016"

     2. Tree crab

     		#MainModule.py
     		1. chose the right module Run "Year" as function
		2. Look at the correctorlly written dleverd luminocity "TotalLumi" for the lepton sale factor
		
		#scaleFactor.py
		1. Check the paths for the efficiency file are correctly provided "mu_fpath" and "el_fpath"

	 	#btagSFProducer.py
	 	1. check the recomandaion for the csv file at "https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation" if reco chage then put new csv file in data and update module with new file name
	 	2. check the Module producer we are going to run "btagSF2016"
 
		#puWeightProducer.py
		1.check you runing right module "puWeight_2016()"

		#jmeModule
		1.check the JEC recomation at "https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC" if it reco change the then put the new tar ball in data and chage the "jecTagsMC and jecTagsDATA" in jetmetHelperRun2.py
		2.if JEC reco chage the check the "globalTag" in  jetmetUncertainties.py
		3.check the JER recomandation at "https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution#Run2_JER_uncertainty_correlation" if the reco chaged the put the new taball in data and chage the "jerTagsMC" in jetmetHelperRun2.py


3. Warnings

	1. python/postprocessing/modules/common/PrefireCorr16.py is not there in new setup

	2. jecredo option has been removed check why------> Does't matter because redo option was for fat jets not for AK4 jets 
