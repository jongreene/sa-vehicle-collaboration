import math

class Vehicle:
	def __init__(self, mu=0.8):
		self.mu = mu

	# https://robotics.stackexchange.com/questions/7796/calculating-required-torque
	def canTraverse(self, angle):
		max_incline = math.atan(self.mu)
		return angle < max_incline
