class Scheduler:
	def __init__(self, machines, max_operations, jobs):
		self.__machines = machines
		self.__jobs_to_be_done = jobs
		self.__jobs_done = []
		self.__max_operations = max_operations

	# Run the scheduler with an heuristic
	def run(self, heuristic):
		current_step = 0

		while len(self.__jobs_to_be_done) > 0:
			current_step += 1

			best_candidates = heuristic(self.__jobs_to_be_done, self.__max_operations, current_step)
			for id_machine, candidates in best_candidates.items():
				machine = self.__machines[id_machine - 1]
				for candidate in candidates:
					if not machine.is_working_at_max_capacity():
						activity, operation = candidate
						machine.add_operation(activity, operation)

			for machine in self.__machines:
				machine.work()

			for job in self.__jobs_to_be_done:
				if job.is_done:
					self.__jobs_to_be_done = list(
						filter(lambda element: element.id_job != job.id_job, self.__jobs_to_be_done))
					self.__jobs_done.append(job)

		print("Done in " + str(current_step) + " units of time")

	# Run the scheduler with the solver
	# noinspection PyAssignmentToLoopOrWithParameter
	def run_pywrapcp(self):
		from ortools.constraint_solver import pywrapcp
		import itertools

		print("WARNING : This method may be very long")

		# Create the solver.
		solver = pywrapcp.Solver('jobshop')

		machines_count = len(self.__machines)
		jobs_count = len(self.__jobs_to_be_done)
		all_machines = range(0, machines_count)
		all_jobs = range(0, jobs_count)

		# Define data.
		list_combinations_for_each_job = []
		for job in self.__jobs_to_be_done:
			job_data = []
			for activity in job.activities_to_be_done:
				activity_data = []
				if len(job_data) == 0:
					for operation in activity.next_operations:
						activity_data.append([(activity, operation)])
				else:
					for operation in activity.next_operations:
						for data in job_data:
							activity_data.append(data + [(activity, operation)])
				job_data = activity_data
			list_combinations_for_each_job.append(job_data)

		# Build all the combinations between each job
		all_combinations = itertools.product(*list_combinations_for_each_job)

		# Create data
		all_data = []
		for combination in all_combinations:
			machines = []
			processing_times = []
			for job in combination:
				m = []
				p = []
				for activity, operation in job:
					m.append(operation.id_machine - 1)
					p.append(operation.duration)
				machines.append(m)
				processing_times.append(p)
			all_data.append((machines, processing_times))

		for key, data in enumerate(all_data):
			machines, processing_times = data
			# Computes horizon.
			horizon = 0
			for i in all_jobs:
				horizon += sum(processing_times[i])

			# Creates jobs.
			all_tasks = {}
			for i in all_jobs:
				for j in range(0, len(machines[i])):
					all_tasks[(i, j)] = solver.FixedDurationIntervalVar(0,
																		horizon,
																		processing_times[i][j],
																		False,
																		'Job_%i_%i' % (i, j))

				# Creates sequence variables and add disjunctive constraints.
				all_sequences = []

				for i in all_machines:

					machines_jobs = []
					for j in all_jobs:
						for k in range(0, len(machines[j])):
							if machines[j][k] == i:
								machines_jobs.append(all_tasks[(j, k)])
					disj = solver.DisjunctiveConstraint(machines_jobs, 'machine %i' % i)
					all_sequences.append(disj.SequenceVar())
					solver.Add(disj)

				# Add conjunctive contraints.
				for i in all_jobs:
					for j in range(0, len(machines[i]) - 1):
						solver.Add(all_tasks[(i, j + 1)].StartsAfterEnd(all_tasks[(i, j)]))

				# Set the objective.
				obj_var = solver.Max([all_tasks[(i, len(machines[i]) - 1)].EndExpr() for i in all_jobs])
				objective_monitor = solver.Minimize(obj_var, 1)

				# Create search phases.
				sequence_phase = solver.Phase([all_sequences[i] for i in all_machines],
											  solver.SEQUENCE_DEFAULT)
				vars_phase = solver.Phase([obj_var],
										  solver.CHOOSE_FIRST_UNBOUND,
										  solver.ASSIGN_MIN_VALUE)
				main_phase = solver.Compose([sequence_phase, vars_phase])

				# Create the solution collector.
				collector = solver.LastSolutionCollector()

				# Add the interesting variables to the SolutionCollector.
				collector.Add(all_sequences)
				collector.AddObjective(obj_var)

				for i in all_machines:
					sequence = all_sequences[i]
					sequence_count = sequence.Size()
					for j in range(0, sequence_count):
						t = sequence.Interval(j)
						collector.Add(t.StartExpr().Var())
						collector.Add(t.EndExpr().Var())
				# Solve the problem.
				disp_col_width = 10
				if solver.Solve(main_phase, [objective_monitor, collector]):
					print("\nOptimal Schedule Length:", collector.ObjectiveValue(0), "\n")
					sol_line = ""
					sol_line_tasks = ""
					print("Optimal Schedule", "\n")

					for i in all_machines:
						seq = all_sequences[i]
						sol_line += "Machine " + str(i) + ": "
						sol_line_tasks += "Machine " + str(i) + ": "
						sequence = collector.ForwardSequence(0, seq)
						seq_size = len(sequence)

						for j in range(0, seq_size):
							t = seq.Interval(sequence[j])
							# Add spaces to output to align columns.
							sol_line_tasks += t.Name() + " " * (disp_col_width - len(t.Name()))

						for j in range(0, seq_size):
							t = seq.Interval(sequence[j])
							sol_tmp = "[" + str(collector.Value(0, t.StartExpr().Var())) + ","
							sol_tmp += str(collector.Value(0, t.EndExpr().Var())) + "] "
							# Add spaces to output to align columns.
							sol_line += sol_tmp + " " * (disp_col_width - len(sol_tmp))

						sol_line += "\n"
						sol_line_tasks += "\n"

					print(sol_line_tasks)
					print("Time Intervals for Tasks\n")
					print(sol_line)
