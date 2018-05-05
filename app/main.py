from job import Job
from activity import Activity
from operation import Operation
from machine import Machine
from scheduler import Scheduler
from geneticscheduler import GeneticScheduler
from heuristics import Heuristics
from drawer import Drawer

import os
import copy
import re
import timeit

# Parser
#with open(os.path.join(os.getcwd(), "data/Barnes/Text/setb4c9.fjs"), "r") as data:
with open(os.path.join(os.getcwd(), "data/test.fjs"), "r") as data:
	total_jobs, total_machines, max_operations = re.findall('\S+', data.readline())
	number_total_jobs, number_total_machines, number_max_operations = int(total_jobs), int(total_machines), int(
		max_operations)
	jobs_list = []
	# Current job's id
	id_job = 1

	for line in data:
		# Split data with multiple spaces as separator
		parsed_line = re.findall('\S+', line)
		# Total number of operations for the job
		number_total_operations = int(parsed_line[0])
		# Current job
		job = Job(id_job)
		# Current activity's id
		id_activity = 1
		# Current item of the parsed line
		i = 1

		while i < len(parsed_line):
			# Total number of operations for the activity
			number_operations = int(parsed_line[i])
			# Current activity
			activity = Activity(job, id_activity)
			for id_operation in range(1, number_operations + 1):
				activity.add_operation(Operation(id_operation, int(parsed_line[i + 2 * id_operation - 1]),
												 int(parsed_line[i + 2 * id_operation])))

			job.add_activity(activity)
			i += 1 + 2 * number_operations
			id_activity += 1

		jobs_list.append(job)
		id_job += 1

# Machines
machines_list = []
for id_machine in range(1, number_total_machines + 1):
	machines_list.append(Machine(id_machine, number_max_operations))

print("Scheduler launched with the following parameters:")
print('\t', str(number_total_jobs), "jobs")
print('\t', str(number_total_machines), "machine(s)")
print('\t', "Machine(s) can process", str(number_max_operations), "operation(s) at the same time")
print("\n")

loop = True
while loop:
	temp_jobs_list = copy.deepcopy(jobs_list)
	temp_machines_list = copy.deepcopy(machines_list)
	print(30 * "-", "MENU", 30 * "-")
	print("1. Scheduler with the longest-operation-first heuristic")
	print("2. Genetic Scheduler")
	print("3. Exit")
	print(67 * "-")

	choice = input("Enter your choice [1-3]: ")
	if choice == "1":
		heuristic = None
		while heuristic is None:
			print("Heuristics availables:")
			print("\t", "1. When an activity has a multiple choice for the operations, choose the shortest one")
			heuristic_choice = input("Enter your choice [1-1]: ")
			if heuristic_choice == "1":
				heuristic = Heuristics.select_first_operation
			else:
				input("Wrong option selection. Enter any key to try again...")

		start = timeit.default_timer()
		s = Scheduler(machines_list, number_max_operations, temp_jobs_list)
		s.run(heuristic)
		stop = timeit.default_timer()
		print("Finished in " + str(stop - start) + " seconds")

		draw = input("Draw the schedule ? [Y/N, default=Y] ")
		if draw == "n" or draw == "N":
			continue
		else:
			Drawer.draw(number_total_machines, number_max_operations, temp_jobs_list, filename="output_scheduler.png")

	elif choice == "2":
		string = input("Total population [default=20] ")
		try:
			total_population = int(string)
		except ValueError:
			total_population = 20
		string = input("Max generation [default=400] ")
		try:
			max_generation = int(string)
		except ValueError:
			max_generation = 400
		start = timeit.default_timer()
		s = GeneticScheduler(temp_machines_list, temp_jobs_list)
		s.run_deap(total_population=total_population, max_generation=max_generation, verbose=True)
		stop = timeit.default_timer()
		print("Finished in " + str(stop - start) + " seconds")

		draw = input("Draw the schedule ? [Y/N, default=Y] ")
		if draw == "n" or draw == "N":
			continue
		else:
			Drawer.draw(number_total_machines, number_max_operations, temp_jobs_list, filename="output_genetic.png")

	elif choice == "3":
		loop = False
	else:
		input("Wrong option selection. Enter any key to try again...")

	del temp_jobs_list, temp_machines_list
