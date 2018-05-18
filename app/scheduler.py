import sys

from colorama import init
from termcolor import colored


class Scheduler:
	def __init__(self, machines, max_operations, jobs):
		init()  # Init colorama for color display
		self.__original_stdout = sys.stdout
		self.__machines = machines
		self.__jobs_to_be_done = jobs
		self.__jobs_done = []
		self.__max_operations = max_operations

	# Run the scheduler with an heuristic
	def run(self, heuristic, verbose=True):
		# Disable print if verbose is False
		if not verbose:
			sys.stdout = None

		current_step = 0

		while len(self.__jobs_to_be_done) > 0:
			current_step += 1

			best_candidates = heuristic(self.__jobs_to_be_done, self.__max_operations, current_step)
			for id_machine, candidates in best_candidates.items():
				machine = self.__machines[id_machine - 1]
				for activity, operation in candidates:
					if not (machine.is_working_at_max_capacity() or activity.is_pending):
						machine.add_operation(activity, operation)

			for machine in self.__machines:
				machine.work()

			for job in self.__jobs_to_be_done:
				if job.is_done:
					self.__jobs_to_be_done = list(
						filter(lambda element: element.id_job != job.id_job, self.__jobs_to_be_done))
					self.__jobs_done.append(job)

		print(colored("[SCHEDULER]", "green"), "Done in " + str(current_step) + " units of time")

		# Reenable stdout
		if not verbose:
			sys.stdout = self.__original_stdout

		return current_step
