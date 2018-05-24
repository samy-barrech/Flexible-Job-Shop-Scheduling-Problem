from customparser import parse
from geneticscheduler import GeneticScheduler
from drawer import Drawer

from colorama import init
from termcolor import colored

import copy
import numpy as np
import timeit


class Benchmarks:
	def __init__(self, path, start=0, stop=4, samples=20):
		init()  # Init colorama for color display
		self.__size = list(set(np.logspace(start, stop, num=samples, dtype=np.int)))
		self.__name = path.split('/')[-1].split('.')[0]
		self.__jobs_list, self.__machines_list, self.__number_max_operations = parse(path)

	# Benchmarks the genetic scheduler when we increase total population
	def population(self, max_generation=100):
		benchmarks_population = []

		print(colored("[BENCHMARKS]", "yellow"), "Gathering computation time for different population sizes")
		for size in self.__size:
			print(colored("[BENCHMARKS]", "yellow"), "Current population size =", size)
			start = timeit.default_timer()
			temp_machines_list, temp_jobs_list = copy.deepcopy(self.__machines_list), copy.deepcopy(self.__jobs_list)
			s = GeneticScheduler(temp_machines_list, temp_jobs_list)
			total_time = s.run_genetic(total_population=size, max_generation=max_generation, verbose=False)
			stop = timeit.default_timer()
			print(colored("[BENCHMARKS]", "yellow"), "Done in", stop - start, "seconds")
			benchmarks_population.append((size, max_generation, stop - start, total_time))
			del s, temp_machines_list, temp_jobs_list
		print(colored("[BENCHMARKS]", "yellow"), "Gathering for different population sizes completed")

		Drawer.plot2d(self.__name + "_benchmarks_population", [element[0] for element in benchmarks_population],
					  [element[2] for element in benchmarks_population],
					  "Time as a function of population size for " + self.__name + " (" + str(
						  max_generation) + " generations)", "Population size", "Time (in seconds)", approximate=True)

		return benchmarks_population

	# Benchmarks the genetic scheduler when we increase max generation
	def generation(self, population_size=100):
		benchmarks_generation = []

		print(colored("[BENCHMARKS]", "yellow"), "Gathering computation time for different generation numbers")
		for size in self.__size:
			print(colored("[BENCHMARKS]", "yellow"), "Current max generation =", size)
			start = timeit.default_timer()
			temp_machines_list, temp_jobs_list = copy.deepcopy(self.__machines_list), copy.deepcopy(
				self.__jobs_list)
			s = GeneticScheduler(temp_machines_list, temp_jobs_list)
			total_time = s.run_genetic(total_population=population_size, max_generation=size, verbose=False)
			stop = timeit.default_timer()
			print(colored("[BENCHMARKS]", "yellow"), "Done in", stop - start, "seconds")
			benchmarks_generation.append((population_size, size, stop - start, total_time))
			del s, temp_machines_list, temp_jobs_list
		print(colored("[BENCHMARKS]", "yellow"), "Gathering for different population sizes completed")

		Drawer.plot2d(self.__name + "_benchmarks_generation", [element[1] for element in benchmarks_generation],
					  [element[2] for element in benchmarks_generation],
					  "Time as a function of max generation for " + self.__name + " (" + str(
						  population_size) + " individuals)", "Max generation", "Time (in seconds)")

		return benchmarks_generation

	# Benchmarks the genetic scheduler for different couples of population size and max generation
	def population_and_generation(self):
		import itertools
		benchmarks_population_and_generation = []
		params = itertools.product(self.__size, repeat=2)
		print(colored("[BENCHMARKS]", "yellow"),
			  "Gathering times for different couples of population size and max generation")
		for population, generation in params:
			print(colored("[BENCHMARKS]", "yellow"), "Current population size =", population, ", max generation =",
				  generation)
			start = timeit.default_timer()
			temp_machines_list, temp_jobs_list = copy.deepcopy(self.__machines_list), copy.deepcopy(
				self.__jobs_list)
			s = GeneticScheduler(temp_machines_list, temp_jobs_list)
			total_time = s.run_genetic(total_population=population, max_generation=generation, verbose=False)
			stop = timeit.default_timer()
			print(colored("[BENCHMARKS]", "yellow"), "Done in", stop - start, "seconds")
			benchmarks_population_and_generation.append((population, generation, stop - start, total_time))
			del s, temp_machines_list, temp_jobs_list
		print(colored("[BENCHMARKS]", "yellow"), "Gathering for different couples completed")

		# Plot graph with solution time as Z axis
		Drawer.plot3d(self.__name + "_benchmarks_generation_with_solution_time",
					  [element[0] for element in benchmarks_population_and_generation],
					  [element[1] for element in benchmarks_population_and_generation],
					  [element[3] for element in benchmarks_population_and_generation],
					  "Best time found as a function of population size and max generation", "Population size",
					  "Max generation", "Total time")

		# Plot graph with computation time as Z axis
		Drawer.plot3d(self.__name + "_benchmarks_generation_with_computation_time",
					  [element[0] for element in benchmarks_population_and_generation],
					  [element[1] for element in benchmarks_population_and_generation],
					  [element[2] for element in benchmarks_population_and_generation],
					  "Computation time as a function of population size and max generation", "Population size",
					  "Max generation", "Computation time")

		return benchmarks_population_and_generation

	# Run all the benchmarks
	def run(self):
		# Run benchmark with constant max generation
		benchmark_population = self.population()

		# Run benchmark with constant population size
		benchmark_generation = self.generation()

		# Run benchmark with changing population size and max generation
		benchmark_population_and_generation = self.population_and_generation()

		return benchmark_population, benchmark_generation, benchmark_population_and_generation
