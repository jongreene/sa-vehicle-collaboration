import math

def canTraverse(power, mass, theta, mu):
	velocity = power / (m * 9.8 * (math.sin(theta) + mu * math.cos(theta)))

	return velocity > 0

# https://robotics.stackexchange.com/questions/7796/calculating-required-torque
