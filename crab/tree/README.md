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

4. Recomdation  UL16preVFP 

	Btagging (RunIISummer20UL16)

		https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16preVFP
		DeepJet=DeepFlavour 
		input csv file:
			reshaping_deepJet_106XUL16preVFP_v2.csv (problem)    	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16preVFP_v2.csv (problem)		csv (WP only) 

			old version finle name remain the same 
			
			loose 	0.0508 
			medium 	0.2598 
			tight 	0.6502
						
			measurement_types we are used right now depends on btv_flavour. 0: Comb, 1:comb, 2:incl , shapevariation:  "iterativefit"

	          For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 
	
	jecTagsMC (Summer19UL16APV_V7_MC)	

			inputfile: 
				Summer19UL16APV_V7_MC.tar.gz     
			GT:
				Summer19UL16APV_V7_MC.tar.gz   
				(GT for Summer20UL samples is 106X_mcRun2_asymptotic_preVFP_v11)

	jecTagsData (Summer19UL16_V7_DATA  )

                https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
                        inputfiles:
                                Summer19UL16_V7_all.tar.gz
                        GT:     
				106X_dataRun2_v35
	
	jerMC (2016)

		https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
		inputfile:
			Summer20UL16APV_JRV3_MC.tar.gz

	jerData (2016)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                      	 Summer20UL16APV_JRV3_DATA.tar.gz

5. Recomdation UL16postVFP 

        Btagging ( RunIISummer20UL16)

		https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL16postVFP
		DeepJet=DeepFlavour 	
		input csv file:
			reshaping_deepJet_106XUL16postVFP_v3.csv (problem)	csv (iterativeFit shape correction)
			wp_deepJet_106XUL16postVFP_v3.csv(problem)		csv (WP only)
	
			old version file name remain the same
							
			loose 	0.0480 
			medium 	0.2489
			tight 	0.6377
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent.  

	jecTagsMC (Summer19UL16_V7_MC)
	
		inputfile: 
			Summer19UL16_V7_MC.tar.gz   
		GT: 
			106X_mcRun2_asymptotic_v17 
			(GT for Summer20UL samples is 106X_mcRun2_asymptotic_v17)

	jecTagsData (Summer19UL16_V7_DATA  )

                https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
                        inputfiles:
				Summer19UL16_V7_all.tar.gz
			GT: 	
				106X_dataRun2_v35

	jerMC (2016)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                         Summer20UL16_JRV3_MC.tar.gz

	jerData (2016)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                         Summer20UL16_JRV3_DATA.tar.gz

6. Recomdation  UL17 
	
	Btagging (RunIISummer19UL17 )

		https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
        	DeepJet=DeepFlavour 
                input csv file: 
                        reshaping_deepJet_106XUL17_v3.csv (problem because of chages applied)       csv (iterativeFit shape correction)
                        wp_deepJet_106XUL17_v3.csv  (problem because of chages applied)             csv (WP only)

			DeepJet_106XUL17SF_V2p1.csv             csv (iterativeFit shape correction +  WP)
                        DeepJet_106XUL17SF_WPonly_V2p1.csv      csv (WP only)

                        loose   0.0532  
                        medium  0.3040           
                        tight   0.7476
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 
	
	jecTagsMC (Summer19UL17 V5 )
		
		inputfile: 
			Summer19UL17_V5_MC.tar.gz   
		GT: 	
			106X_mc2017_realistic_v8  
			(GT for Summer20UL samples is 106X_mc2017_realistic_v9)

	jecTagsData (Summer19UL17 )

                https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
                        inputfiles:
                                Summer19UL17_RunB_V5_DATA.tar.gz
                                Summer19UL17_RunC_V5_DATA.tar.gz
                                Summer19UL17_RunD_V5_DATA.tar.gz
                                Summer19UL17_RunE_V5_DATA.tar.gz
                                Summer19UL17_RunF_V5_DATA.tar.gz
                        GT:     
				106X_dataRun2_v33

 	jerMC (Summer19UL17)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                         Summer19UL17_JRV2_MC.tar.gz

	jerData (Summer19UL17)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                        Summer19UL17_JRV2_DATA.tar.gz

7. Recomdation UL18

	Btagging (RunIISummer19UL18)

		https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation106XUL18
		DeepJet=DeepFlavour
			reshaping_deepJet_106XUL18_v2.csv (problem because of chages applied) 	csv (iterativeFit shape correction)
			wp_deepJet_106XUL18_v2.csv	(problem because of chages applied) 	csv (WP only)
		
			DeepJet_106XUL18SF_V1p1.csv		csv (iterativeFit shape correction + fix wp)
			DeepJet_106XUL18SF_WPonly_V1p1.csv	csv (WP only)
	
			loose 	0.0490 
			medium 	0.2783 
			tight 	0.7100 
		For precision measurements on top physics, it is recommended to use the "mujets" scale factors, as statistically independent. 	 

	jecTagsMC (Summer19UL18 V5)

                inputfile: 
			Summer19UL18_V5_MC.tar.gz   
		GT: 
			106X_upgrade2018_realistic_v15_L1v1  
			(GT for Summer20UL samples is 106X_upgrade2018_realistic_v16_L1v1)

	jecTagsData (Summer19UL18 )

                https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
                        inputfiles:
                                Summer19UL18_RunA_V5_DATA.tar.gz
                                Summer19UL18_RunB_V5_DATA.tar.gz
                                Summer19UL18_RunC_V5_DATA.tar.gz
                                Summer19UL18_RunD_V5_DATA.tar.gz
                        GT :    
				106X_dataRun2_v33 (GT for Summer20UL samples is )

	jerMC (Summer19UL18)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                       	Summer19UL18_JRV2_MC.tar.gz

	jerData (Summer19UL18)

                https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
                inputfile:
                        Summer19UL18_JRV2_DATA.tar.gz
