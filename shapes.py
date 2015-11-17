class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Dimension:
	def __init__(self, width, height):
		self.width = width
		self.height = height

class Rectangle:
	'''
	x, y represents the top-left corner of the rectangle. Both width and height extend towards positive.
	'''
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def intersects_rectangle(self, other):
		not_intersecting = self.x + self.width < other.x or \
		self.x > other.x + other.width or \
		self.y + self.height < other.y or \
		self.y > other.y + other.height
		return not not_intersecting

class LineSegment:
	def __init__(self, x1, x2, y):
		self.x1 = x1
		self.x2 = x2
		self.y = y

	def intersects_rectangle(self, other):
		not_intersecting_in_y = self.y < other.y or self.y > other.y + other.height
		return (not not_intersecting_in_y) and (other.x <= self.x1 and other.x + other.width >= self.x1) and (other.x <= self.x2 and other.x + other.width >= self.x2)
