import math

class Vehicle:
	def __init__(self, power, mass, mu=0.8):
		self.power = power
		self.mass = mass
		self.mu = mu

	# https://robotics.stackexchange.com/questions/7796/calculating-required-torque
	def canTraverse(self, angle):
		#return (self.power / (self.mass * 9.8 * (math.sin(angle) + self.mu * math.cos(angle)))) > 0
		max_incline = 20
		return math.degrees(angle) < max_incline
