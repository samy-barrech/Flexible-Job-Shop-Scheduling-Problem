from drawer import Drawer
from geneticscheduler import GeneticScheduler
from customparser import parse

from colorama import init
from termcolor import colored

from os import walk

import copy


class EvaluateSolutions:
	def __init__(self, path):
		init()  # Init colorama for color display
		self.__path = path
		self.__files_list = {}

	def run(self, population_size=100, max_generation=300):
		results = {}
		print(colored("[EVALUATION]", "red"), "Population size =", population_size, "& Max generation =",
			  max_generation)
		for (path, _, filenames) in walk(self.__path):
			for filename in filenames:
				jobs_list, machines_list, _ = parse(path + filename)
				print(colored("[EVALUATION]", "red"), "Running evaluation for", filename)
				time_results = []
				for i in range(1, 6):
					print(colored("[EVALUATION]", "red"), "Starting instance", i)
					temp_machines_list, temp_jobs_list = copy.deepcopy(machines_list), copy.deepcopy(
						jobs_list)
					s = GeneticScheduler(temp_machines_list, temp_jobs_list)
					time = s.run_genetic(total_population=population_size, max_generation=max_generation, verbose=False)
					del s, temp_jobs_list, temp_machines_list
					print(colored("[EVALUATION]", "red"), "Done in", time, "units of time")
					time_results.append(time)
				average_time = sum(time_results) / float(len(time_results))
				print(colored("[EVALUATION]", "red"), "Average time found for", filename, ":", average_time)
				results.update({filename: average_time})

			print(colored("[EVALUATION]", "red"), "Resulting average time for files in", self.__path)
			for filename, average_time in results.items():
				print("\t", filename, " - Average time =", average_time)
