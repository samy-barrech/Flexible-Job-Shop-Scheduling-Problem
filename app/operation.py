class Operation:
	def __init__(self, id_operation, id_machine, duration):
		self.__id_operation = id_operation
		self.__duration = duration
		self.__id_machine = id_machine
		self.__time = None
		self.__is_pending = False
		self.__place_of_arrival = None

	# Display the operation nicer
	def __str__(self):
		output = "Operation n°" + str(self.__id_operation) + " -> Machine: " + str(
			self.__id_machine) + ", Duration: " + str(self.__duration)

		if not (self.__time is None):
			output += ", Started at time " + str(self.__time)

		return output

	# Return the operation's id
	@property
	def id_operation(self):
		return self.__id_operation

	# Return if an operation is done at time t
	def is_done(self, t):
		return not (self.__time is None) and self.__time + self.__duration <= t

	# Return if a machine is already treating the operation
	@property
	def is_pending(self):
		return self.__is_pending

	# Set the pending status
	@is_pending.setter
	def is_pending(self, value):
		self.__is_pending = value

	# Return the slot of the machine allocated for the treatment of the operation
	@property
	def place_of_arrival(self):
		return self.__place_of_arrival

	# Set the slot of the machine allocated for the treatment of the operation
	@place_of_arrival.setter
	def place_of_arrival(self, value):
		self.__place_of_arrival = value

	# Return the machine's id who has to do the operation
	@property
	def id_machine(self):
		return self.__id_machine

	# Return the operation's duration
	@property
	def duration(self):
		return self.__duration

	# Return at which time the operation started or None
	@property
	def time(self):
		return self.__time

	# Set the time at which the operation started
	@time.setter
	def time(self, value):
		if value < 0:
			raise ValueError("Time < 0 is not possible")
		self.__time = value
