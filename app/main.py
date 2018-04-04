import os
import re


class Scheduler(object):
	def __init__(self, machines_number, jobs_number, tasks):
		self.t = 0
		self.machines_in_used = []
		self.machines_number = int(machines_number)
		self.jobs_number = int(jobs_number)
		self.tasks_to_be_done = tasks
		self.tasks_done = []
		print("Jobs and activities:\n", self.tasks_to_be_done)

	# Find the next best operations to start with
	def find_start(self):
		starter = {}

		for i in range(1, self.machines_number + 1):
			starter.update({i: None})

		for job_id, activities in enumerate(self.tasks_to_be_done):
			first_activity = activities[0]
			max_operation = None

			# Find the operation with the longest duration
			for operation_id, operation in enumerate(first_activity):
				if max_operation is None or max_operation.get('Duration') < operation.get('Duration'):
					max_operation = {'Index': operation_id, 'Duration': operation.get('Duration')}

			operation = first_activity[max_operation.get('Index')]
			machine_id = operation.get('Machine')
			if starter.get(machine_id) is None or starter.get(machine_id).get('Operation').get('Duration') < max_operation.get('Duration'):
				starter.update({machine_id: {'Job': job_id, 'Operation_Index': max_operation.get('Index'), 'Operation': operation}})

		return starter

	def run(self):
		starter = self.find_start()
		


with open(os.path.join(os.getcwd(), "data/test.fjs"), "r") as data:
	jobs, machines, operation = re.findall('\S+', data.readline())
	jobs_list = []

	for line in data:
		parsed_line = re.findall('\S+', line)  # Split data with multiple spaces as separator
		number_operations = int(parsed_line[0])
		activities_list = []
		i = 1
		while i < len(parsed_line):
			number_machines = int(parsed_line[i])
			list_operations = []
			for j in range(0, number_machines):
				list_operations.append({'Machine': int(parsed_line[i + 1 + 2 * j]), 'Duration': int(parsed_line[i + 2 * (j + 1)]), 'Status': False})
			activities_list.append(list_operations)
			i += 1 + 2 * number_machines
		jobs_list.append(activities_list)

s = Scheduler(machines, jobs, jobs_list)
s.find_start()
