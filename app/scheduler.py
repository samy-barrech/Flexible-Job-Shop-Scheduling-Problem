class Scheduler:
	def __init__(self, machines, max_operations, jobs):
		self.__machines = machines
		self.__jobs_to_be_done = jobs
		self.__jobs_done = []
		self.__max_operations = max_operations

	# Find the next longest operations
	def find_next_longest_operations(self):
		best_candidates = {}

		for job in self.__jobs_to_be_done:
			current_activity = job.current_activity

			# Find the operations with the longest duration
			for operation in current_activity.next_operations:
				if best_candidates.get(operation.id_machine) is None:
					best_candidates.update({operation.id_machine: [(current_activity, operation)]})
				elif len(best_candidates.get(operation.id_machine)) < self.__max_operations:
					list_operations = best_candidates.get(operation.id_machine)
					list_operations.append((current_activity, operation))
					best_candidates.update({operation.id_machine: list_operations})
				else:
					list_operations = list(filter(lambda element: element.duration < operation.duration, best_candidates.get(operation.id_machine)))
					if len(list_operations) < self.__max_operations:
						list_operations.append((current_activity, operation))
						best_candidates.update({operation.id_machine: list_operations})

		return best_candidates

	def run(self):
		current_step = 0

		while len(self.__jobs_to_be_done) > 0:
			current_step += 1

			best_candidates = self.find_next_longest_operations()
			for id_machine, candidates in best_candidates.items():
				machine = self.__machines[id_machine-1]
				for candidate in candidates:
					if not machine.is_working_at_max_capacity():
						activity, operation = candidate
						machine.add_operation(activity, operation)

			for machine in self.__machines:
				machine.work()

			for job in self.__jobs_to_be_done:
				if job.is_done:
					self.__jobs_to_be_done = list(filter(lambda element: element.id_job != job.id_job, self.__jobs_to_be_done))
					self.__jobs_done.append(job)

		print("Done in " + str(current_step) + " units of time")
