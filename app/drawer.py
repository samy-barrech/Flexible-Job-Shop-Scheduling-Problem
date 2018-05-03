import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Drawer:
	@staticmethod
	def draw(number_machines, max_operations, jobs):
		# Vertical space between operation
		vertical_space = 1
		# Vertical height of an operation
		vertical_height = 2

		# Dictionary of the operations done, the key correspond to the machine id
		operations_done = {}
		for job in jobs:
			for activity in job.activities_done + job.activities_to_be_done:
				# Add all done operations
				operation = activity.operation_done
				# If it's the first operation add on the machine, initialize the list
				if operations_done.get(operation.id_machine) is None:
					list_operations = []
				# Else, get the previously added operations
				else:
					list_operations = operations_done.get(operation.id_machine)

				# Append the current operation with its job's id and activity's id
				list_operations.append((job.id_job, activity.id_activity, operation))
				# Update the dictionary
				operations_done.update({operation.id_machine: list_operations})

		# Define random colors for jobs
		colors = ['#%06X' % random.randint(0,256**3-1) for _ in range(len(jobs))]

		# Draw
		plt.clf()
		plot = plt.subplot()

		for id_machine, list_operations in operations_done.items():
			for id_job, id_activity, operation in list_operations:
				# X coord corresponds to the operation's time
				# Y coord corresponds to the order of the operation
				# according to its machine's id, its place of arrival and the max operations allowed simultaneously
				x, y = operation.time, 1 + id_machine * max_operations * (vertical_space + vertical_height) + operation.place_of_arrival * (vertical_space + vertical_height)
				# Plot a rectangle with a width of the operation's duration
				plot.add_patch(
					patches.Rectangle(
						(x, y),
						operation.duration,
						vertical_height,
						facecolor=colors[id_job-1]
					)
				)

		# Display the machines' number as the y-axis legend
		plt.yticks([1 + (i+1) * max_operations * (vertical_space + vertical_height) + (max_operations * (vertical_height + vertical_space) - vertical_space)/2 for i in range(number_machines)], ["machine " + str(i + 1) for i in range(number_machines)])
		# Auto-scale to see all the operations
		plot.autoscale()

		# Display a rectangle with the color and the job's id as the x-axis legend
		handles = []
		for id_job, color in enumerate(colors):
			handles.append(patches.Patch(color=color, label='job ' + str(id_job + 1)))
		plt.legend(handles=handles)

		# Show the schedule order
		plt.show()
