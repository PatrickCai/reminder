# -- encoding:utf - 8 --

import sys
import wx 


reload(sys)
sys.setdefaultencoding('utf-8')

class review_item(object):
	def __init__(self, ID, review_name, times, due_days, due_time):
		self.ID = ID
		self.review_name = review_name
		self.times = times
		self.due_days = due_days
		self.due_time = due_time
