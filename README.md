# FPMC_tools
Tools for setting up FPMC and running versioned simulations

Tested on CERN lxplus (CC7)

Use:
```
source setupFPMC.sh
```
to clone the FPMC repository and automatically build FPMC

```
./runFPMC.py <datacard>
```
runs the simulation of the process specified by <datacard> 
  
```
./run_with_GLU_NU.py <datacard> <glu_nu>
```
runs the simulation of the process specified by <datacard> input and <glu_nu> value
