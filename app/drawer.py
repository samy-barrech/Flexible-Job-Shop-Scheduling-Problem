import random
import os


class Drawer:
	@staticmethod
	def draw_schedule(number_machines, max_operations, jobs, filename=None):
		import matplotlib.pyplot as plt
		import matplotlib.patches as patches

		# Vertical space between operation
		vertical_space = 1
		# Vertical height of an operation
		vertical_height = 2

		# Dictionary of the operations done, the key correspond to the machine id
		operations_done = {}
		for job in jobs:
			for activity in job.activities_done:
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
		colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(jobs))]

		# Draw
		plt.clf()
		plot = plt.subplot()

		for id_machine, list_operations in operations_done.items():
			for id_job, id_activity, operation in list_operations:
				# X coord corresponds to the operation's time
				# Y coord corresponds to the order of the operation
				# according to its machine's id, its place of arrival and the max operations allowed simultaneously
				x, y = operation.time, 1 + id_machine * max_operations * (
						vertical_space + vertical_height) + operation.place_of_arrival * (
							   vertical_space + vertical_height)
				# Plot a rectangle with a width of the operation's duration
				plot.add_patch(
					patches.Rectangle(
						(x, y),
						operation.duration,
						vertical_height,
						facecolor=colors[id_job - 1]
					)
				)

		# Display the machines' number as the y-axis legend
		plt.yticks([1 + (i + 1) * max_operations * (vertical_space + vertical_height) + (
				max_operations * (vertical_height + vertical_space) - vertical_space) / 2 for i in
					range(number_machines)], ["machine " + str(i + 1) for i in range(number_machines)])
		# Auto-scale to see all the operations
		plot.autoscale()

		# Display a rectangle with the color and the job's id as the x-axis legend
		handles = []
		for id_job, color in enumerate(colors):
			handles.append(patches.Patch(color=color, label='job ' + str(id_job + 1)))
		plt.legend(handles=handles)

		# Show the schedule order
		plt.show()
		# Saving the scheduler order
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')

	# Plot a 2d graph
	@staticmethod
	def plot2d(filename, xdata, ydata, title, xlabel, ylabel, approximate=False, min_degree=2, max_degree=8):
		import matplotlib.pyplot as plt
		plt.clf()
		plot = plt.subplot()
		plot.set_title(title)
		plot.set_xlabel(xlabel)
		plot.set_ylabel(ylabel)
		plot.plot(xdata, ydata, 'o' if approximate else '-')
		
		if approximate:
			import numpy as np
			from scipy.interpolate import UnivariateSpline
			from colorama import init
			from termcolor import colored
			init()
			
			# Compute an interval of 150 points
			x = np.linspace(xdata[0], xdata[-1], 150)
			
			# Compute a spline to measure the error between the approximation and the data set
			spline = UnivariateSpline(xdata, ydata)
			y_spline = spline(x)
			plot.plot(x, y_spline, 'C0')
			
			# Compute different polynomial approximations
			legends = ["Original data", "Spline approximation"]
			# Save best polynomial approximation
			best_degree = best_coefficients = best_residual = best_y_poly = None
			
			# Computing different polynomial approximations
			for degree in range(min_degree, max_degree + 1):
				# Find a polynomial to fit the spline
				coefficients = np.polyfit(xdata, ydata, degree)
				poly = np.poly1d(coefficients)
				y_poly = poly(x)
				# Compute the residual (the error)
				residual = np.linalg.norm(y_spline - y_poly, 2)
				# Display current polynomial approximation residual
				print(colored("[DRAWER]", "magenta"), "Polynomial approximation of degree", str(degree),
					  "-> Residual =", residual)
				# Checking if it's a better approximation
				if best_residual is None or residual < best_residual:
					best_degree, best_coefficients, best_residual, best_y_poly = degree, coefficients, residual, y_poly
					
			# Displaying best polynomial found
			legends.append("Approximation of degree " + str(best_degree))
			print(colored("[DRAWER]", "magenta"), "Best approximation found is a polynomial of degree",
				  str(best_degree))
			print("\t", "Coefficients:", best_coefficients)
			print("\t", "Residual:", best_residual)
			# Plotting resulting polynomial
			plot.plot(x, best_y_poly, '--')
			plot.legend(legends)
			
		plot.autoscale()
		plt.show()
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')

	# Plot a 3d graph
	@staticmethod
	def plot3d(filename, xdata, ydata, zdata, title, xlabel, ylabel, zlabel):
		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt

		plt.clf()
		fig = plt.figure()
		plot = fig.gca(projection='3d')
		plot.set_title(title)
		plot.set_xlabel(xlabel)
		plot.set_ylabel(ylabel)
		plot.set_zlabel(zlabel)
		plot.scatter(xdata, ydata, zdata, c='b', marker='o')
		plot.autoscale()
		plt.show()
		if not (filename is None):
			plt.savefig(os.path.join("output", filename), bbox_inches='tight')
