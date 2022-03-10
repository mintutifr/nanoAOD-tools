1. Genral

	Jme Module check the recomdation file 

2. Specific

     1. Btagging evoluvation

     		#EfficiencyModule.py (we are not using it now this was for fix wp only and now we moved to iterativeFit)
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

4. Recomdation 

    UL16preAPV

	Btagging

	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
	DeepJet=DeepFlavour
		input csv file:
			reshaping_deepJet_106XUL16preVFP_v2.csv    	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16preVFP_v2.csv		csv (WP only) 
				
			loose 	0.0508 
			medium 	0.2598 
			tight 	0.6502
						
			measurement_types we are using : comb b / comb c /  incl  check ???
	For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 

    UL2016postVFiP

        Btagging

	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
	DeepJet=DeepFlavour 	
			reshaping_deepJet_106XUL16postVFP_v3.csv	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16postVFP_v3.csv		csv (WP only)
				
			loose 	0.0480 
			medium 	0.2489
			tight 	0.6377
	For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent.  

    UL17 
	
	Btagging

	https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
        DeepJet=DeepFlavour 
                input csv file: 
                        reshaping_deepJet_106XUL17_v3.csv       csv (iterativeFit shape correction)
                        wp_deepJet_106XUL17_v3.csv              csv (WP only)

                        loose   0.0532  
                        medium  0.3040           
                        tight   0.7476
	For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 
 
    UL18

	Btagging

	https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation106XUL18
	DeepJet=DeepFlavour
			reshaping_deepJet_106XUL18_v2.csv	csv (iterativeFit shape correction)
			wp_deepJet_106XUL18_v2.csv		csv (WP only)
			
			loose 	0.0490 
			medium 	0.2783 
			tight 	0.7100 
	For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 	 
