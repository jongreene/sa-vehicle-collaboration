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

	def canTraverse(self, angle):
		if self.max is not 'None':
			return angle < float(self.max)

		if self.type == 'all':
			return self.all_wheel_drive(angle)
		
		elif self.type == 'front':
			return self.front_wheel_drive(angle)

		elif self.type =='rear':
			return self.rear_wheel_drive(angle)

		else:
			return False

	# all equations for vehicle climbing taken from 
	# http://www.thecartech.com/subjects/auto_eng/Max_gradient.pdf
	def all_wheel_drive(self, angle):
		return angle < math.atan(self.mu)

	def front_wheel_drive(self, angle):
		return angle < math.atan((self.mu * self.l_r)/(self.l + self.mu * self.h))

	def rear_wheel_drive(self, angle):
		return angle < math.atan((self.mu * self.l_f)/(self.l - self.mu*self.h))
