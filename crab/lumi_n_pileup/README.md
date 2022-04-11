#To Make new files for paticular runs look at the following twiki
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile

#To set the brill cal inviroment vist the following page
https://twiki.cern.ch/twiki/bin/view/CMS/BrilcalcQuickStart

#To get the latest tag for the calculation visit the following page
https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec

#Golden jeson file
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

#Run Dependent Pileup distribition can we created 
pileupCalc.py -i RunC_UL2017.txt --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 99 --numPileupBins 99 MyDataPileupHistogram_RunC_UL2017.root
