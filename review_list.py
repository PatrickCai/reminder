# -- encoding:utf - 8 --

import sys
import wx 

from review_xml import review_xml as rxml

reload(sys)
sys.setdefaultencoding('utf-8')

class review_list(object):
	def __init__(self):
		self.first_item = None
		self.rest_review_items = []


	def check_update(self):
		rxml().check_update()

	def fetch_review_items(self):
		'''return the first item to be reviewed and other review items_list to be reviewed'''
		self.review_items = rxml().xml_to_items()
		self.first_item = None if len(self.review_items)== 0 else self.review_items[0]
		self.rest_review_items = [] if len(self.review_items) < 2 else self.review_items[1:]

	def add_item(self, review_name):
		'''return nothing ,add the item into the review xml'''
		rxml().add_item(review_name)
		rxml().check_update()

	def complete_item(self):
		'''Push the completed item into the xml, change the rl status'''
		rxml().complete_item(self.first_item.ID)
		self.check_update()
		self.fetch_review_items()

	def once_again(self):
		rxml().once_again(self.first_item.ID)
		self.check_update()
		self.fetch_review_items()

	def delete_item(self):
		rxml().delete_item(self.first_item.ID)
		self.check_update()	
		self.fetch_review_items()

	def debug_info(self):
		self.check_update()
		self.fetch_review_items()
		print("There are %s items to be reviewed"%(len(self.review_items)))
		def print_info(review_name, review_times, due_time): 
			print(u"The (%s) item has been reviewed for %s times its due time is %s"%(review_name, review_times, due_time))
		if self.first_item:
			print_info(self.first_item.review_name, self.first_item.times, self.first_item.due_time)
		if self.rest_review_items:
			for item in self.rest_review_items:
				print_info(item.review_name, item.times, item.due_time)










