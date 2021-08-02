#!/bin/python3
import os
import sys
import subprocess

fpmc_build_folder = "./FPMC/build_ttbar/"
CMSSW_folder = "./FPMC/CMSSW_10_6_10/"
fpmc_source_folder = "./FPMC/fpmc/"
madgraph_folder = "/eos/home-a/abellora/SWAN_projects/TopPheno/MadGraph/MG5_aMC_v3_1_0/"
delphes_datacard = "Delphes/cards/delphes_card_CMS.tcl"
work_folder = os.getcwd()+"/"

def runFPMC(datacard ="", fpmc_output=True, LHE_output=False, ROOT_output=False, Delphes_output=False,seed=42,sampleID=""):
	if type(fpmc_output) == str:
		if fpmc_output.lower() == "true":
			fpmc_output = True
		else:
			fpmc_output = False
		if LHE_output.lower() == "true":
			LHE_output = True
		else:
			LHE_output = False
		if ROOT_output.lower() == "true":
			ROOT_output = True
		else:
			ROOT_output = False
		if Delphes_output.lower() == "true":
			Delphes_output = True
		else:
			Delphes_output = False

	def print_and_run(command):
		print(command)
		subprocess.call(command, shell=True)

	if not os.path.exists(datacard):
		print("ERROR: Missing datacard!")
		sys.exit(1)

	# Create the new directory for logging the simulation
	subprocess.call("mkdir -p LOG", shell=True)
	logfolder_dirs = [int(i) for i in os.listdir(path="LOG")]
	if sampleID == "":
		if logfolder_dirs == []:
			newdir = 1
		else:
			newdir = max(logfolder_dirs) + 1
	else:
		newdir = int(sampleID)+int(seed)
	print_and_run("mkdir -p LOG/"+str(newdir))

	# Set environment for fpmc & run the simulation
	datacard_tmp = datacard+"_tmp_"+seed+"_"+sampleID
	lhe_filename=""
	with open(datacard) as dc, open(datacard_tmp,"w") as dc_tmp:
		for line in dc: 
			if line.startswith("NRN1"):
				dc_tmp.write("NRN1        {}\n".format(newdir))
			elif line.startswith("LHEFILE"):
				lhe_filename = line.split()[1]
				lhe_filename = lhe_filename.replace(".lhe", "_"+seed+"_"+sampleID+".lhe").replace("'","")
				dc_tmp.write("LHEFILE     \'"+lhe_filename+"\'\n")
			else:
				dc_tmp.write(line)
	setenv_command = "cd "+CMSSW_folder+"src; eval `scramv1 runtime -sh`; cd -"
	fpmc_command = "cd "+fpmc_build_folder+"; ./fpmc-lhe < "+work_folder+datacard_tmp+" | tee "+work_folder+"out_tmp"+str(newdir)+"; cd -"
	print("Executing: \n"+setenv_command+"\n"+fpmc_command)
	if fpmc_output:
		subprocess.call(setenv_command+";"+fpmc_command, shell=True)
	else:
		subprocess.call(setenv_command+";"+fpmc_command, shell=True, stdout=subprocess.DEVNULL)

	# Save summary in the log file
	datacard_content = subprocess.getoutput("cat "+datacard_tmp)
	glu_nu = subprocess.getoutput("grep -m 1 'GLU_NU=' "+fpmc_source_folder+"/Fpmc/External/pdf/h1qcd.f | sed 's/d/e/'").lstrip()
	glu_nu = glu_nu.replace("=","      ")
	final_summary = subprocess.getoutput("tail --lines=1 out_tmp"+str(newdir))
	summaryFileName = "LOG/"+str(newdir)+"/Summary.txt"
	with open(summaryFileName, "w+") as summary_file:
		summary_file.write("*******************************DATACARD*******************************\n")
		summary_file.write(datacard_content)
		summary_file.write("\n********************************GLU_NU********************************\n")
		summary_file.write(glu_nu)	
		summary_file.write("\n********************************RESULT********************************\n")
		summary_file.write(final_summary)
		summary_file.write("\n**********************************************************************\n")

	os.remove(datacard_tmp)
	if lhe_filename == "":
		print("No LHE file name found in datacard!")
		sys.exit(1)

	lhe_filepath = "LHE/"+str(newdir)+"/"+lhe_filename
	root_filename = os.path.splitext(lhe_filename)[0]+".root"
	root_filepath = "ROOT/"+str(newdir)+"/"+root_filename
	delphes_filepath = "DELPHES/"+str(newdir)+"/"+root_filename

	print_and_run("mkdir -p LHE")
	print_and_run("mkdir -p LHE/"+str(newdir))
	print_and_run("mv "+fpmc_build_folder+lhe_filename+" "+lhe_filepath)
	
	# Convert LHE to ROOT file format
	if ROOT_output:
		print_and_run("mkdir -p ROOT")
		print_and_run("mkdir -p ROOT/"+str(newdir))
		print_and_run(setenv_command+";"+madgraph_folder+"ExRootAnalysis/ExRootLHEFConverter "+lhe_filepath+" "+root_filepath)
		print("ROOT file saved in: "+root_filepath)

	# Run Delphes on the LHE file
	if Delphes_output:
		setDelphesEnv = "source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc10-opt/setup.sh"
		print_and_run("mkdir -p DELPHES/"+str(newdir))
		print_and_run(setDelphesEnv+";"+madgraph_folder+"Delphes/DelphesLHEF "+madgraph_folder+delphes_datacard+" "+delphes_filepath+" "+lhe_filepath)		
		print("Delphes output file saved in: "+delphes_filepath)
		
	if not LHE_output:
		subprocess.call("rm -r LHE/"+str(newdir),shell=True)
	else:
		print("LHE file saved in: "+lhe_filepath)


	# clean outputs
	subprocess.call("rm out_tmp"+str(newdir), shell=True)
	print("Summary saved in: " + summaryFileName)


if __name__ == "__main__":
    runFPMC(*sys.argv[1:])
