# -- encoding:utf - 8 --

import sys

from datetime import datetime
from datetime import timedelta

reload(sys)
sys.setdefaultencoding('utf-8')

days_delay = {1:2, 2:2, 3:7, 4:100, 5:365}

class review_time(object):
	def __init__(self, string_time):
		self.strftime = self.__from_string(string_time)

	@classmethod
	def from_standard(cls, standard_time):
		string_time = standard_time.now().strftime('%Y-%m-%d %H:%M:%S')
		strftime = cls(string_time)
		return strftime

	@classmethod
	def now(cls):
		#TODO! (NOT ELEGENT!)
		string_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		return cls(string_time)


	def is_due(self):
		'''return true or false to judge whether the time is over now~'''
		return bool(self.strftime < datetime.now())

	def days_to_today(self):
		'''return the days from the delayed days'''
		days_delay = datetime.now() - self.strftime
		days_delay = str(days_delay.days)#the label needs it to be str instead of int
		return days_delay

	def review_days(self, times):
		'''parameter time is the times that to be reviewed
		   return the string time next date to be reviewed'''
		standard_time = self.strftime + timedelta(days=days_delay[times])
		return self.__to_string(standard_time)


	def __to_string(self, standard_time):
		'''convet from standar to string time'''
		string_time = standard_time.strftime('%Y-%m-%d %H:%M:%S')
		return string_time

	def __from_string(self, string_time):
		'''convert from string to standard time'''
		strftime = datetime.strptime(string_time, '%Y-%m-%d %H:%M:%S')
		return strftime


if __name__ == '__main__':
	print(review_time.now().review_days(times=1))
