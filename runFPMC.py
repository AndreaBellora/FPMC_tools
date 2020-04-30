#!/bin/python3
import os
import sys
import subprocess

fpmc_build_folder = "./FPMC/build/"
CMSSW_folder = "./FPMC/CMSSW_10_6_10/"
fpmc_source_folder = "./FPMC/fpmc/"

saveLHEFile=False

def runFPMC(datacard ="", fpmc_output=True):

	def print_and_run(command):
		print(command)
		subprocess.call(command, shell=True)

	if not os.path.exists(datacard):
		print("ERROR: Missing datacard!")
		sys.exit(1)

	# Create the new directory for logging the simulation
	subprocess.call("mkdir -p LOG", shell=True)
	logfolder_dirs = [int(i) for i in os.listdir(path="LOG")]
	if logfolder_dirs == []:
		newdir = 1
	else:
		newdir = max(logfolder_dirs) + 1
	print_and_run("mkdir -p LOG/"+str(newdir))

	# Set environment for fpmc & run the simulation
	setenv_command = "cd "+CMSSW_folder+"src; eval `scramv1 runtime -sh`; cd -"
	fpmc_command = "./"+fpmc_build_folder+"fpmc-lhe < "+datacard+" | tee out_tmp"
	print("Executing: \n"+setenv_command+"\n"+fpmc_command)
	if fpmc_output:
		subprocess.call(setenv_command+";"+fpmc_command, shell=True)
	else:
		subprocess.call(setenv_command+";"+fpmc_command, shell=True, stdout=subprocess.DEVNULL)

	# Save summary in the log file
	datacard = subprocess.getoutput("cat "+datacard)
	glu_nu = subprocess.getoutput("grep -m 1 'GLU_NU=' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f | sed 's/d/e/'").lstrip()
	glu_nu = glu_nu.replace("=","      ")
	final_summary = subprocess.getoutput("tail --lines=1 out_tmp")
	summaryFileName = "LOG/"+str(newdir)+"/Summary.txt"
	with open(summaryFileName, "w+") as summary_file:
		summary_file.write("*******************************DATACARD*******************************\n")
		summary_file.write(datacard)
		summary_file.write("\n********************************GLU_NU********************************\n")
		summary_file.write(glu_nu)	
		summary_file.write("\n********************************RESULT********************************\n")
		summary_file.write(final_summary)
		summary_file.write("\n**********************************************************************\n")


	# Save the LHE file if needed
	with open("Datacards/incl_Ttbar_QCD") as datacard:
		for line in datacard: 
			if line.startswith("LHEFILE"):
				lhe_filename = line.split()[1]
	if saveLHEFile:
		os.system("mkdir -p LHE")
		print_and_run("mkdir -p LHE/"+str(newdir))
		subprocess.call("mv "+lhe_filename+" LHE/"+str(newdir)+"/", shell=True)
		print("LHE file saved in: LHE/"+str(newdir)+"/"+lhe_filename)
	else:
		subprocess.call("rm "+lhe_filename, shell=True)

	# clean outputs
	subprocess.call("rm out_tmp", shell=True)
	print("Summary saved in: " + summaryFileName)


if __name__ == "__main__":
    runFPMC(sys.argv[1])