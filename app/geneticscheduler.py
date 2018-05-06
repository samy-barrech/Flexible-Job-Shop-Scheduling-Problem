import copy
import itertools
import sys
import random

import multiprocessing

from deap import base
from deap import creator
from deap import tools

from scheduler import Scheduler
from heuristics import Heuristics

from colorama import init
from termcolor import colored


class GeneticScheduler:
	def __init__(self, machines, jobs):
		init()  # Init colorama for color display
		self.__original_stdout = sys.stdout
		self.__toolbox = base.Toolbox()
		self.__machines = machines
		self.__jobs = jobs

	# Constraint order
	@staticmethod
	def constraint_order_respected(individual):
		list = [(activity.id_job, activity.id_activity) for (activity, _) in individual]
		for key, (id_job, id_activity) in enumerate(list):
			if id_activity == 1:
				continue
			elif not list.index((id_job, id_activity - 1)) < key:
				return False
		return True

	# Initialize an individual for the genetic algorithm
	def init_individual(self, ind_class, size):
		print(colored("[DEAP]", "cyan"), "Running the scheduler with an heuristic to get a first solution")
		temp_jobs_list = copy.deepcopy(self.__jobs)
		temp_machines_list = copy.deepcopy(self.__machines)

		# Run the scheduler
		s = Scheduler(temp_machines_list, 1, temp_jobs_list)
		initial_time = s.run(Heuristics.select_first_operation, verbose=False)
		print(colored("[DEAP]", "cyan"), "Initial time the solution take", initial_time)

		# Retriving all the activities and the operation done
		list_activities = []
		for temp_job in temp_jobs_list:
			for temp_activity in temp_job.activities_done:
				activity = self.__jobs[temp_activity.id_job - 1].get_activity(temp_activity.id_activity)
				operation = activity.get_operation(temp_activity.operation_done.id_operation)
				list_activities.append((temp_activity.operation_done.time, activity, operation))
		# Ordering activities by time
		list_activities = sorted(list_activities, key=lambda x: x[0])
		individual = [(activity, operation) for (_, activity, operation) in list_activities]
		del temp_jobs_list, temp_machines_list
		return ind_class(individual)

	# Initialize a population
	def init_population(self, total_population):
		individual = self.__toolbox.individual()
		return [individual for _ in range(total_population)]

	# Compute the time an individual take
	def compute_time(self, individual):
		# List matching the activities to the time it takes place
		list_time = []
		# Operation schedule on machines indexed by machines' id
		schedule = {}
		for machine in self.__machines:
			schedule.update({machine.id_machine: []})
		# Operation done indexed by job's id
		operations_done = {}
		for job in self.__jobs:
			operations_done.update({job.id_job: []})

		# For each item in individual, we compute the actual time at which the operation considered start
		for activity, operation in individual:
			# Get at which time the previous operation is done
			time_last_operation, last_operation_job = operations_done.get(activity.id_job)[-1] if len(
				operations_done.get(activity.id_job)) > 0 else (0, None)
			time_last_machine, last_operation_machine = schedule.get(operation.id_machine)[-1] if len(
				schedule.get(operation.id_machine)) > 0 else (0, None)

			if last_operation_machine is None and last_operation_job is None:
				time = 0
			elif last_operation_machine is None:
				time = time_last_operation + last_operation_job.duration
			elif last_operation_job is None:
				time = time_last_machine + last_operation_machine.duration
			else:
				time = max(time_last_machine + last_operation_machine.duration,
						   time_last_operation + last_operation_job.duration)

			list_time.append(time)

			operations_done.update({activity.id_job: operations_done.get(activity.id_job) + [(time, operation)]})
			schedule.update({operation.id_machine: schedule.get(operation.id_machine) + [(time, operation)]})

		# We compute the total time we need to process all the jobs
		total_time = 0
		for machine in self.__machines:
			if len(schedule.get(machine.id_machine)) > 0:
				time, operation = schedule.get(machine.id_machine)[-1]
				if time + operation.duration > total_time:
					total_time = time + operation.duration

		return total_time, list_time

	# Evaluate the fitness for an individual, in our case it means compute the total time an individual take
	def evaluate_individual(self, individual):
		return self.compute_time(individual)[0],

	# Create a mutant based on an individual
	# In our case it means select another operation within an activity with multiple choices for an operation
	@staticmethod
	def mutate_individual(individual):
		mutant = copy.deepcopy(individual)
		# Select the possible candidates, meaning the activities with multiple choices for an operation
		candidates = list(filter(lambda element: len(element[0].next_operations) > 1, mutant))
		# If some candidates have been found, mutate a random one
		if len(candidates) > 0:
			mutant_activity, previous_operation = candidates[random.randint(0, len(candidates) - 1)]
			id_mutant_activity = [element[0] for element in mutant].index(mutant_activity)
			mutant_operation = previous_operation
			while mutant_operation.id_operation == previous_operation.id_operation:
				mutant_operation = mutant_activity.next_operations[
					random.randint(0, len(mutant_activity.next_operations) - 1)]
			mutant[id_mutant_activity] = (mutant_activity, mutant_operation)
		# Remove the previous fitness value because it is deprecated
		del mutant.fitness.values
		# Return the mutant
		return mutant

	# Permute an individual
	# In our case it means select an activity and permute it with another
	# It needs to meet some constraint to be efficient:
	#	You can't move an activity before or after another one from the same job
	@staticmethod
	def compute_bounds(permutation, considered_index):
		considered_activity, _ = permutation[considered_index]
		min_index = key = 0
		max_index = len(permutation) - 1
		while key < max_index:
			activity, _ = permutation[key]
			if activity.id_job == considered_activity.id_job:
				if min_index < key < considered_index:
					min_index = key
				if considered_index < key < max_index:
					max_index = key
			key += 1
		return min_index, max_index

	def permute_individual(self, individual):
		permutation = copy.deepcopy(individual)
		permutation_possible = False
		considered_index = considered_permutation_index = 0
		while not permutation_possible:
			considered_index = min_index = max_index = 0
			# Loop until we can make some moves, i.e. when max_index - min_index > 2
			while max_index - min_index <= 2:
				considered_index = random.randint(0, len(permutation) - 1)
				min_index, max_index = self.compute_bounds(permutation, considered_index)

			# Select a random activity within those bounds (excluded) to permute with
			considered_permutation_index = random.randint(min_index + 1, max_index - 1)
			min_index_permutation, max_index_permutation = self.compute_bounds(permutation,
																			   considered_permutation_index)
			if min_index_permutation < considered_index < max_index_permutation:
				permutation_possible = considered_index != considered_permutation_index

		# A possible permutation has been found
		permutation[considered_index], permutation[considered_permutation_index] = permutation[
																					   considered_permutation_index], \
																				   permutation[considered_index]
		return permutation

	# Evolve an individual
	def evolve_individual(self, individual, mutation_probability, permutation_probability):
		future_individual = individual
		if random.randint(0, 100) < mutation_probability:
			future_individual = self.mutate_individual(future_individual)
		if random.randint(0, 100) < permutation_probability:
			future_individual = self.permute_individual(future_individual)
		return future_individual if self.constraint_order_respected(future_individual) else individual

	# Simulate the individual with the machines
	def run_simulation(self, individual):
		_, list_time = self.compute_time(individual)
		for key, (individual_activity, individual_operation) in enumerate(individual):
			activity = self.__jobs[individual_activity.id_job - 1].get_activity(individual_activity.id_activity)
			operation = activity.get_operation(individual_operation.id_operation)
			operation.time = list_time[key]
			operation.place_of_arrival = 0
			activity.terminate_operation(operation)

	# Run the genetic scheduler
	def run_deap(self, total_population=10, max_generation=100, verbose=False):
		# Disable print if verbose is False
		if not verbose:
			sys.stdout = None

		creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
		creator.create("Individual", list, fitness=creator.FitnessMin)

		self.__toolbox.register("individual", self.init_individual, creator.Individual, size=1)
		self.__toolbox.register("mutate", self.mutate_individual)
		self.__toolbox.register("permute", self.permute_individual)
		self.__toolbox.register("evaluate", self.evaluate_individual)

		print(colored("[DEAP]", "cyan"), "Generating population")
		population = self.init_population(total_population)

		best = None
		print(colored("[DEAP]", "cyan"), "Starting evolution for", max_generation, "generations")
		for current_generation in range(max_generation):
			# Evaluate the entire population
			fitnesses = list(map(self.evaluate_individual, population))
			for ind, fit in zip(population, fitnesses):
				ind.fitness.values = fit
				if best is None or best.fitness.values[0] > ind.fitness.values[0]:
					print(colored("[DEAP]", "cyan"), "A better individual has been found. New best time = ",
						  ind.fitness.values[0])
					best = copy.deepcopy(ind)

			# Generate mutation and permutation probabilities for the next generation
			mutation_probability = random.randint(0, 100)
			permutation_probability = random.randint(0, 100)

			# Evolve the population
			print(colored("[DEAP]", "cyan"), "Evolving to generation", current_generation+1)
			for key, individual in enumerate(population):
				population[key] = self.evolve_individual(individual, mutation_probability, permutation_probability)
				del individual
		print(colored("[DEAP]", "cyan"), "Evolution finished")
		if self.constraint_order_respected(best):
			print(colored("[DEAP]", "cyan"), "Best time found equals", best.fitness.values[0])
			print(colored("[DEAP]", "cyan"), "Simulating work on machines")
			self.run_simulation(best)
			print(colored("[DEAP]", "cyan"), "Simulation finished")
			print(colored("[DEAP]", "cyan"), "Genetic scheduler finished")
		else:
			print(colored("[DEAP]", "cyan"), "The individual doesn't match the constraint order")

		# Reenable stdout
		if not verbose:
			sys.stdout = self.__original_stdout
