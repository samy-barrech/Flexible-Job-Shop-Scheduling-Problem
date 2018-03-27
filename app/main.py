import os
import re

with open(os.path.join(os.getcwd(), "data/Dauzere_Data/Text/01a.fjs"), "r") as data:
	jobs, machines, operation = re.findall('\S+', data.readline())
	jobs_list = []

	for line in data:
		parsed_line = re.findall('\S+', line)
		number_operations = parsed_line[0]
		activities_list = []
		i = 1
		while i < len(parsed_line):
			number_machines = int(parsed_line[i])
			list_operations = []
			for j in range(0, number_machines):
				list_operations.append((parsed_line[i + 1 + 2*j], parsed_line[i + 2*(j+1)]))
			activities_list.append(list_operations)
			i += 1 + 2 * number_machines
		jobs_list.append(activities_list)



