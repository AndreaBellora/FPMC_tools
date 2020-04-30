#!/bin/bash
mkdir FPMC
cd FPMC
git clone https://github.com/fpmc-hep/fpmc.git
mkdir build
scram project CMSSW CMSSW_10_6_10
cd CMSSW_10_6_10/src
eval `scramv1 runtime -sh`
cd ../../build
cmake ../fpmc
make fpmc-lhe
cd ../../
chmod u+x runFPMC.py 
chmod u+x run_with_GLU_NU.py