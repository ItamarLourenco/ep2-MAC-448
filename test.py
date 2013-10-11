#!/usr/bin/env python

class test(object):
	"""docstring for test"""
	def __init__(self, arg):
		self.arg = arg

	def testing (self):
		self.arg2 = "heyhey"

		print self.arg, self.arg2

t = test("uepa")

t.testing