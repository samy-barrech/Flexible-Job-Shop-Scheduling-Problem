from job import Job
from activity import Activity
from operation import Operation
from machine import Machine

import os
import re


def parse(path):
	with open(os.path.join(os.getcwd(), path), "r") as data:
		total_jobs, total_machines, max_operations = re.findall('\S+', data.readline())
		number_total_jobs, number_total_machines, number_max_operations = int(total_jobs), int(total_machines), int(float(
			max_operations))
		jobs_list = []
		# Current job's id
		id_job = 1

		for key, line in enumerate(data):
			if key >= number_total_jobs:
				break
			# Split data with multiple spaces as separator
			parsed_line = re.findall('\S+', line)
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

	return jobs_list, machines_list, number_max_operations
