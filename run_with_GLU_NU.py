#!/bin/python3
import os
import sys
import subprocess
import runFPMC

fpmc_build_folder = "./FPMC/build/"
CMSSW_folder = "./FPMC/CMSSW_10_6_10/"
fpmc_source_folder = "./FPMC/fpmc/"

def replace_GLU_NU_and_compile(glu_nu=-2,fpmc_output=True):
	"""
	This function replaces GLU_NU with the glu_nu value (careful, it must be a string like 0.5)
	and compiles FPMC
	"""
	# Set GLU_NU to the new value
	setenv_command = "cd "+CMSSW_folder+"src; eval `scramv1 runtime -sh`; cd -"
	# Find the line where GLU_NU is defined
	old_glu_nu_assignment = subprocess.getoutput("grep -m 1 'GLU_NU=' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f ")
	if fpmc_output:
		# Replace GLU_NU with the new value, only in the first occurrence
		subprocess.call("sed -i '0,/"+old_glu_nu_assignment.lstrip()+"/s//GLU_NU="+str(glu_nu)+"d0/' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f", shell=True,)
		# Compile FPMC with the new GLU_NU
		subprocess.call(setenv_command+";"+"cd "+fpmc_build_folder+"; make fpmc-lhe", shell=True,)
	else:
		# Replace GLU_NU with the new value, only in the first occurrence
		subprocess.call("sed -i '0,/"+old_glu_nu_assignment.lstrip()+"/s//GLU_NU="+str(glu_nu)+"d0/' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f", shell=True, stdout=subprocess.DEVNULL)
		# Compile FPMC with the new GLU_NU
		subprocess.call(setenv_command+";"+"cd "+fpmc_build_folder+"; make fpmc-lhe", shell=True, stdout=subprocess.DEVNULL)		

def run_with_GLU_NU(datacard="", glu_nu=2, fpmc_output=True):
	"""
	This function runs the FPMC simulation with a different GLU_NU value
	"""
	# Check that glu_nu is in range
	if not -1 <= float(glu_nu) <= 1:
		print("ERROR: GLU_NU out of range!")
		sys.exit(1) 
	# Find the old glu_nu value
	old_glu_nu = subprocess.getoutput("grep -m 1 'GLU_NU=' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f ")
	old_glu_nu = float(old_glu_nu.split("=")[1].replace("d","E"))
	# Rebuild FPMC with the new glu_nu value
	replace_GLU_NU_and_compile(glu_nu,fpmc_output)
	# Run the simulation
	runFPMC.runFPMC(datacard,fpmc_output)
	# Set FPMC back to the previoud configuration
	replace_GLU_NU_and_compile("{:f}".format(old_glu_nu),fpmc_output)

if __name__ == "__main__":
    run_with_GLU_NU(sys.argv[1], sys.argv[2])