#!/bin/python3
import run_with_GLU_NU
import os
import sys
# import matplotlib.pyplot as plt

measurements = 5
glu_nu_min = -1
glu_nu_max = 1

# def plot(glu_nus, cross_sections,title=""):
# 	plt.plot(glu_nus,cross_sections)
# 	plt.xlabel("GLU_NU")
# 	plt.ylabel("Cross Section (pb)")
# 	plt.title(title)
# 	plt.show()

def run_GLU_NU_analysis(datacard = "", LHE_output=False, ROOT_output=False):
	"""
	This function simulates for a variety of 
	"""
	# Compute the id of the first simulation
	logfolder_dirs = [int(i) for i in os.listdir(path="LOG")]
	if logfolder_dirs == []:
		first_simId = 1
	else:
		first_simId = max(logfolder_dirs) + 1

	glu_nus = []
	cross_sections = []
	# Perform the measurements 
	for i in range(measurements):
		# Compute glu_nu and simulate with it
		glu_nu = glu_nu_min + i * (glu_nu_max - glu_nu_min) / (measurements-1)
		print("*************************************************************")
		print("Running simulation with GLU_NU = "+str(glu_nu))
		run_with_GLU_NU.run_with_GLU_NU(datacard,glu_nu, False, LHE_output, ROOT_output)
		
		# Compute the id of the i-th simulation and get the result from the summary
		simId = first_simId + i
		# Extract the cross section measurement
		with open("LOG/"+str(simId)+"/Summary.txt") as summary:
			for line in summary: 
				if line.lstrip().startswith("Cross"):
					xsec = float(line.split()[2]) 
					print("Cross section (pb) = ",xsec)
		glu_nus.append(glu_nu)
		cross_sections.append(xsec)
		print("*************************************************************")

	print("Result lists: ")
	print(glu_nus)
	print(cross_sections)
	process_name= os.path.splitext(os.path.basename(datacard))[0]
	# plot(glu_nus,cross_sections,process_name)

	print("Summaries saved with simIds: "+str(first_simId)+"..."+str(first_simId+measurements-1))



if __name__ == "__main__":
	run_GLU_NU_analysis(*sys.argv[1:])	