Crab submission for MC skimtree
 	1. Lines in crab_cfg_skimTree.py must check for mc samples:

		config.Data.splitting = 'FileBased'
		config.Data.unitsPerJob = 1
		config.Data.publication = True
		#config.Data.totalUnits = 10 (this has line must be commented out othewise inly jobs for 10 files only wull be submitted for each dataset)
		#config.Data.lumiMask = <path to Json file> (this has line must be commented out for MC dataset, this will be needed for data)

 	2. Crab submission for UL mc samples can be done using "crab_submission_mcUL.py" file using the following commond:

	 	python crab_submission_mcUL.py  -y UL2016preVFP -h (-y stands for year -h stands for help, Script have to run without -h option otherwise it prints the help option only)

 	3. For new used user name has to be changes in following files:

		a. crab_submission_mcUL.py  ->  outputDir = "/store/user/<username>/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP/check/"
		b. crab_cfg_skimTree.py     ->  config.Site.storageSite = "<T2_IN_TIFR>" (need to chage storege unit accordingly)
		c. crab_script_skimTree.sh  ->  export X509_USER_PROXY=/afs/cern.ch/user/m/mikumar/x509up_u106474 (need to chage proxy path accordingly)	
 
