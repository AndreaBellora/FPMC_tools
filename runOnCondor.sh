#!/bin/bash

cd /afs/cern.ch/user/a/abellora/workarea/Work/TopPheno/FPMC_tools
pwd
echo "python3 runFPMC.py $1 $2 $3 $4 $5 $6 $7"
python3 runFPMC.py $1 $2 $3 $4 $5 $6 $7
