from scheduler import Scheduler
from geneticscheduler import GeneticScheduler
from heuristics import Heuristics
from drawer import Drawer
from customparser import parse
from benchmarks import Benchmarks
from evaluatesolutions import EvaluateSolutions

import copy
import sys
import timeit

path = "data/test.fjs" if len(sys.argv) == 1 else sys.argv[1]
jobs_list, machines_list, number_max_operations = parse(path)
number_total_machines = len(machines_list)
number_total_jobs = len(jobs_list)

print("Scheduler launched with the following parameters:")
print('\t', number_total_jobs, "jobs")
print('\t', number_total_machines, "machine(s)")
print('\t', "Machine(s) can process", str(number_max_operations), "operation(s) at the same time")
print("\n")

loop = True
while loop:
	temp_jobs_list = copy.deepcopy(jobs_list)
	temp_machines_list = copy.deepcopy(machines_list)
	print(30 * "-", "MENU", 30 * "-")
	print("1. Scheduler with an heuristic")
	print("2. Genetic Scheduler")
	print("3. Benchmarks")
	print("4. Run an evaluation of the solutions")
	print("4. Exit")
	print(66 * "-")

	choice = input("Enter your choice [1-5]: ")
	if choice == "1":
		heuristic = None
		while heuristic is None:
			print("Heuristics availables:")
			print("\t", "1. When an activity has a multiple choice for the operations, choose the shortest one")
			print("\t", "2. Assign operations to machines randomly")
			heuristic_choice = input("Enter your choice [1-2]: ")
			if heuristic_choice == "1":
				heuristic = Heuristics.select_first_operation
			elif heuristic_choice == "2":
				heuristic = Heuristics.random_operation_choice
			else:
				input("Wrong option selection. Enter any key to try again...")

		start = timeit.default_timer()
		s = Scheduler(temp_machines_list, number_max_operations, temp_jobs_list)
		s.run(heuristic)
		stop = timeit.default_timer()
		print("Finished in " + str(stop - start) + " seconds")

		draw = input("Draw the schedule ? [Y/N, default=Y] ")
		if draw == "n" or draw == "N":
			continue
		else:
			Drawer.draw_schedule(number_total_machines, number_max_operations, temp_jobs_list,
								 filename="output_scheduler.png")
		del s
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
		s.run_genetic(total_population=total_population, max_generation=max_generation, verbose=True)
		stop = timeit.default_timer()
		print("Finished in " + str(stop - start) + " seconds")

		draw = input("Draw the schedule ? [Y/N, default=Y] ")
		if draw == "n" or draw == "N":
			continue
		else:
			Drawer.draw_schedule(number_total_machines, number_max_operations, temp_jobs_list,
								 filename="output_genetic.png")
		del s
	elif choice == "3":
		b = Benchmarks(path)
		b.run()

	elif choice == "4":
		e = EvaluateSolutions("data/Dauzere_Data/Text/")
		e.run()

	elif choice == "5":
		loop = False
	else:
		input("Wrong option selection. Enter any key to try again...")

	del temp_jobs_list, temp_machines_list
