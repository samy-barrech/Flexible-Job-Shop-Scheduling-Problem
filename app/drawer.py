import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Drawer:
	@staticmethod
	def draw(number_machines, max_operations, jobs):
		operations_done = {}
		for job in jobs:
			for activity in job.activities_done + job.activities_to_be_done:
				# Add all done operations
				for operation in activity.operations_done:
					if operations_done.get(operation.id_machine) is None:
						list_operations = []
					else:
						list_operations = operations_done.get(operation.id_machine)

					list_operations.append((job.id_job, activity.id_activity, operation))
					operations_done.update({operation.id_machine: list_operations})

		# Sort operations by time
		# for id_machine, list_operations in operations_done.items():
		# operations_done.update({id_machine: sorted(list_operations, key=lambda element: element[2].time)})

		# Define color for jobs
		colors = ['#%06X' % random.randint(0,256**3-1) for i in range(len(jobs))]

		# Draw
		plt.clf()
		plot = plt.subplot()

		for id_machine, list_operations in operations_done.items():
			for id_job, id_activity, operation in list_operations:
				x, y = operation.time, 1 + id_machine * max_operations * 3 + operation.place_of_arrival * 3
				plot.add_patch(
					patches.Rectangle(
						(x, y),  			# (x,y)
						operation.duration, # width
						2,  				# height
						facecolor=colors[id_job-1],
						label="job " + str(id_job)
					)
				)

		plt.yticks([1 + (i+1) * max_operations * 3 + max_operations * 1.5 for i in range(number_machines)], ["machine " + str(i + 1) for i in range(number_machines)])
		plot.autoscale()

		handles = []
		for id_job, color in enumerate(colors):
			handles.append(patches.Patch(color=color, label='job ' + str(id_job + 1)))
		plt.legend(handles=handles)

		plt.show()
