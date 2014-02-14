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
		review_items = rxml().xml_to_items()
		self.first_item = None if len(review_items)== 0 else review_items[0]
		self.rest_review_items = [] if len(review_items) < 2 else review_items[1:]

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








