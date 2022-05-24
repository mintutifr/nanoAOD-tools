#!/bin/bash

#REFERENCE
#https://github.com/florez/CONDOR
printf "Start Running Histogramming at ";/bin/date
printf "Worker node hostname ";/bin/hostname

date
outputroot=$1
echo "ouput root file wull be" $outputroot
echo "CONDOR DIR: $_CONDOR_SCRATCH_DIR"
cd ${_CONDOR_SCRATCH_DIR}
ls -ltr
#------------------------------------------------
# set cmsenv
#------------------------------------------------
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_10_6_28
cd CMSSW_10_6_28/src
eval `scramv1 runtime -sh`

#------------------------------------------------
# untar nanoaod tools ans list the directory
#------------------------------------------------
mv ../../cutflow.tar.gz .
tar --strip-components=0 -zxf cutflow.tar.gz
pwd
ls -la
cp ../../cutflowModule.py PhysicsTools/NanoAODTools/crab/cutflow/ 
cp ../../crab_script_cutflow.py PhysicsTools/NanoAODTools/crab/cutflow/
scram b -j4

cd PhysicsTools/NanoAODTools/crab/cutflow/
echo "python crab_script_cutflow.py"
python crab_script_cutflow.py

printf "Done cutflow at ";/bin/date

#---------------------------------------------
#copy the output from remote machine to the lxplus
#------------------------------------------------
xrdcp -f Cutflow_hist.root ${outputroot}

#---------------------------------------------
#Remove the package, after copying the output
#------------------------------------------------
echo "Cleaning up condor directory"


cd ${_CONDOR_SCRATCH_DIR}
rm -rf cutflow.tar.gz
rm -rf CMSSW_10_6_28
rm -rf *.py
ls -ltr
printf "Done ";/bin/date

