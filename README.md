# FPMC_tools
Tools for setting up FPMC and running versioned simulations

Tested on CERN lxplus (CC7)

Use:
```
bash setupFPMC.sh
```
to clone the FPMC repository and automatically build FPMC

Use:
```
./runFPMC.py <datacard>
```
runs the simulation of the process specified by <datacard> 

Use:  
```
./run_with_GLU_NU.py <datacard> <glu_nu>
```
runs the simulation of the process specified by <datacard> input and <glu_nu> value

# For MadGraph
Setup with 'source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh'
Install pythia, install Delphes separately -> copied DelphesHEPMC2 in DelphesHEPMC