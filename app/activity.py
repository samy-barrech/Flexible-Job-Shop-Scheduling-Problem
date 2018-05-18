class Activity:
	def __init__(self, job, id_activity):
		self.__job = job
		self.__id_activity = id_activity
		self.__operations_to_be_done = []
		self.__operation_done = None

	# Display the activity nicer
	def __str__(self):
		output = "Job n°" + str(self.id_job) + " Activity n°" + str(self.__id_activity) + "\n"

		output += "Operations to be done\n"
		for operation in self.__operations_to_be_done:
			output += str(operation) + "\n"

		output += "Operation done\n"
		output += str(self.__operation_done) + "\n"

		return output

	# Return the job's id of the activity
	@property
	def id_job(self):
		return self.__job.id_job

	# Return the activity's id
	@property
	def id_activity(self):
		return self.__id_activity

	# Add an operation to the activity
	def add_operation(self, operation):
		self.__operations_to_be_done.append(operation)

	# Return if the activity is done
	@property
	def is_done(self):
		return not (self.__operation_done is None)

	# Return the list of all the operations yet to be done
	@property
	def next_operations(self):
		return self.__operations_to_be_done

	# Return the shortest operation available
	@property
	def shortest_operation(self):
		candidate_operation = None
		for operation in self.__operations_to_be_done:
			if candidate_operation is None or operation.duration < candidate_operation.duration:
				candidate_operation = operation
		return operation

	# Return the list of all the operations already done
	@property
	def operation_done(self):
		return self.__operation_done

	# Allow a machine to say to an activity that it finished an operation
	def terminate_operation(self, operation):
		# Remove the operation from the list of the operations yet to be done
		self.__operations_to_be_done = list(
			filter(lambda element: element.id_operation != operation.id_operation, self.__operations_to_be_done))
		# Append the operation to the list of the operations already done
		self.__operation_done = operation
		self.__job.activity_is_done(self)

	@property
	def shop_time(self):
		return self.operation_done.duration if self.is_done else max(self.__operations_to_be_done,
																	 key=lambda operation: operation.duration)

	@property
	def is_feasible(self):
		return self.__job.check_if_previous_activity_is_done(self.__id_activity)

	@property
	def is_pending(self):
		return len(list(filter(lambda element: element.is_pending, self.__operations_to_be_done))) > 0

	def get_operation(self, id_operation):
		for operation in self.__operations_to_be_done:
			if operation.id_operation == id_operation:
				return operation
