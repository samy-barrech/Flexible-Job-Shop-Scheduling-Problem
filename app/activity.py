class Activity:
	def __init__(self, job, id_activity):
		self.__job = job
		self.__id_activity = id_activity
		self.__operations_to_be_done = []
		self.__operations_done = []

	# Display the activity nicer
	def __str__(self):
		output = "Job n°" + str(self.id_job) + " Activity n°" + str(self.__id_activity) + "\n"

		output += "Operations to be done\n"
		for operation in self.__operations_to_be_done:
			output += str(operation) + "\n"

		output += "Operations done\n"
		for operation in self.__operations_done:
			output += str(operation) + "\n"

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
		return len(self.operations_to_be_done) == 0

	# Return the list of all the operations yet to be done
	@property
	def operations_to_be_done(self):
		return self.__operations_to_be_done

	# Return the list of all the operations already done
	@property
	def operations_done(self):
		return self.__operations_done

	# Allow a machine to say to an activity that it finished an operation
	def terminate_operation(self, operation):
		# Remove the operation from the list of the operations yet to be done
		self.__operations_to_be_done = list(filter(lambda element: element.id_operation != operation.id_operation, self.__operations_to_be_done))
		# Append the operation to the lsit of the operations already done
		self.__operations_done.append(operation)
		# If there is no operation yet to be done anymore, signal to the job that the activity is done
		if len(self.__operations_to_be_done) == 0:
			self.__job.activity_is_done(self)

	@property
	def next_operations(self):
		return list(filter(lambda operation: not operation.is_pending, self.__operations_to_be_done))
