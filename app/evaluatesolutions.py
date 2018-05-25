from drawer import Drawer
from geneticscheduler import GeneticScheduler
from customparser import parse

from colorama import init
from termcolor import colored

import os
import copy
import timeit


class EvaluateSolutions:
	def __init__(self, path):
		init()  # Init colorama for color display
		self.__path = path
		self.__files_list = {}

	def run(self, population_size=100, max_generation=200):
		results = {}
		print(colored("[EVALUATION]", "red"), "Population size =", population_size, "& Max generation =",
			  max_generation)
		for (path, _, filenames) in os.walk(self.__path):
			for filename in filenames:
				jobs_list, machines_list, _ = parse(os.path.join(path, filename))
				print(colored("[EVALUATION]", "red"), "Running evaluation for", filename)
				time_results = []
				computation_times = []
				for i in range(1, 6):
					print(colored("[EVALUATION]", "red"), "Starting instance", i)
					temp_machines_list, temp_jobs_list = copy.deepcopy(machines_list), copy.deepcopy(
						jobs_list)
					start = timeit.default_timer()	
					s = GeneticScheduler(temp_machines_list, temp_jobs_list)
					time = s.run_genetic(total_population=population_size, max_generation=max_generation, verbose=False)
					stop = timeit.default_timer()
					print(colored("[EVALUATION]", "red"), "Done in", time, "units of time,", stop - start, "seconds")
					time_results.append(time)
					computation_times.append(stop - start)
					del s, start, stop, time, temp_jobs_list, temp_machines_list
				average_time = sum(time_results) / float(len(time_results))
				computation_time = sum(computation_times) / float(len(computation_times))
				print(colored("[EVALUATION]", "red"), "Average time found for", filename, ":", average_time)
				results.update({filename: (average_time, computation_time)})
				del time_results, computation_times

			print(colored("[EVALUATION]", "red"), "Resulting average time for files in", self.__path)
			for filename, (average_time, computation_time) in results.items():
				print("\t", filename, "- Average time =", average_time, "for an average computation time of",
					  computation_time, "seconds")
