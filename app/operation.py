class Operation:
	def __init__(self, id_operation, id_machine, duration):
		self.__id_operation = id_operation
		self.__duration = duration
		self.__id_machine = id_machine
		self.__time = None
		self.__is_pending = False
		self.__place_of_arrival = None

	def __str__(self):
		output = "Operation n°" + str(self.__id_operation) + " -> Machine: " + str(self.__id_machine) + ", Duration: " + str(self.__duration)

		if not(self.__time is None):
			output += ", Started at time " + str(self.__time)

		return output

	@property
	def id_operation(self):
		return self.__id_operation

	@property
	def is_done(self):
		return self.__is_pending

	@property
	def is_pending(self):
		return self.__is_pending

	@is_pending.setter
	def is_pending(self, value):
		self.__is_pending = value

	@property
	def place_of_arrival(self):
		return self.__place_of_arrival

	@place_of_arrival.setter
	def place_of_arrival(self, value):
		self.__place_of_arrival = value

	@property
	def id_machine(self):
		return self.__id_machine

	@property
	def duration(self):
		return self.__duration

	@property
	def time(self):
		return self.__time

	@time.setter
	def time(self, value):
		if value < 0:
			raise ValueError("Time < 0 is not possible")
		self.__time = value

