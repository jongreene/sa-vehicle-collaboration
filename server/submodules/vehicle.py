import math

class Vehicle:
	def __init__(self, opts):
		self.mu = float(opts['mu'])
		self.weight = float(opts['weight'])
		self.width = float(opts['dimensions']['width'])
		self.length = float(opts['dimensions']['length'])
		self.type = opts['drive-type']
		self.l = float(opts['dimensions']['wheel-base'])
		self.l_f = float(opts['dimensions']['CoM-front'])
		self.l_r = float(opts['dimensions']['CoM-rear'])
		self.h = float(opts['dimensions']['CoM-height'])
		self.max = opts['max-hill-rads']
		self.clearance = float(opts['dimensions']['min-clearance'])

		if self.max != 'None':
			return

		if self.type == 'all':
			self.max = self.all_wheel_drive()

		elif self.type == 'front':
			self.max = self.front_wheel_drive()

		elif self.type =='rear':
			self.max = self.rear_wheel_drive()

	def canTraverse(self, angle, rise):
		if self.max != 'None':
			return abs(angle) < float(self.max)

		if self.clearance > abs(rise):
			return True

		return False

	# all equations for vehicle climbing taken from
	# http://www.thecartech.com/subjects/auto_eng/Max_gradient.pdf
	def all_wheel_drive(self):
		return math.atan(self.mu)

	def front_wheel_drive(self):
		return math.atan((self.mu * self.l_r)/(self.l + self.mu * self.h))

	def rear_wheel_drive(self):
		return math.atan((self.mu * self.l_f)/(self.l - self.mu*self.h))
