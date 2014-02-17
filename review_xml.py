# -- encoding:utf - 8 --

import sys
import wx 
import pdb

from functools import wraps

from lxml import etree

from review_time import review_time as rtime
from review_item import review_item as ritem

reload(sys)
sys.setdefaultencoding('utf-8')


class review_xml(object):
	def __init__(self):
		self.__root = None

	def parse_xml(func):
		'''Decorators for parsing the xml first'''
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			self.__tree = etree.parse('review_list.xml')
			self.__root = self.__tree.getroot()
			ret = func(self, *args, **kwargs)			
			return ret
		return wrapper


	@parse_xml
	def check_update(self):
		'''check whether there are some review items due, 
		    and update the isDue to True if it's due'''
		IDs = self.__root.xpath("reviewList[isDue='False']/ID")
		due_times = self.__root.xpath("reviewList[isDue='False']/dueTime")
		due_IDs = []
		#check 
		for ID, due_time in zip(IDs, due_times):
			if rtime(due_time.text).is_due():
				due_IDs.append(ID.text)
		#update
		for due_ID in due_IDs:
			is_due = self.__root.find("reviewList[ID='%s']/isDue"%(due_ID))
			is_due.text = 'True'
		self.__write_xml()

	@parse_xml
	def xml_to_items(self):
		'''return the list of review_items that should be reviewed now!'''
		review_xmls = self.__root.xpath("reviewList[isDue='True']")
		review_items = []
		for review_xml in review_xmls:
			review_find = lambda x:review_xml.find("%s"%(x)).text
			ID = review_find("ID")
			review_name = review_find("reviewName")
			times = review_find("times")
			due_time = review_find("dueTime")
			due_days = rtime(due_time).days_to_today()#convert from the due time to the days that delay
			review_item = ritem(ID=ID, review_name=review_name, times=times,
								due_days=due_days, due_time=due_time)
			review_items.append(review_item)
		#sort the review_items according to its delay days(should be detailed to seconds)
		review_items = sorted(review_items, key=lambda x:x.due_time, )
		return review_items

	@parse_xml
	def add_item(self, review_name):
		'''return the added item , add the review item into the review xml'''
		#add the item into the xmls
		try :
			ID = str(int(self.__root.find("reviewList[last()]/ID").text) + 1)
		except AttributeError:
			ID = 1 #In case there are no data in xml(which will never happen)
		due_time = rtime.now().review_days(times=1)
		reviewList = etree.SubElement(self.__root, "reviewList")
		times = "1" #first review
		isDue = "False"
		def add_element(xml_name, from_attr):
			xml_attr = etree.SubElement(reviewList, xml_name)
			xml_attr.text = from_attr

		for xml_name, from_name in zip(["ID", "reviewName", "times", "dueTime", "isDue"], 
										[ID, review_name, times, due_time, isDue]) :
			add_element(xml_name, from_name)
		self.__write_xml()
		

	@parse_xml
	def complete_item(self, item_ID):
		reviewList = self.__root.find("reviewList[ID='%s']"%(item_ID))
		#change the name if necessary
		review_name = reviewList.find("reviewName").text
		if review_name.endswith('(Again!)'):
			reviewList.find("reviewName").text = review_name[:-8]
		#change the times
		times = reviewList.find("times").text 
		reviewList.find("times").text = str(int(times)+1)
		times = int(times)+1
		#change the due date
		reviewList.find("dueTime").text = rtime.now().review_days(times=times)
		#change the isDue to False
		reviewList.find("isDue").text = "False"
		self.__write_xml()

	@parse_xml
	def once_again(self, item_ID):
		reviewList = self.__root.find("reviewList[ID='%s']"%(item_ID))
		review_name = reviewList.find("reviewName").text 
		if not review_name.endswith("(Again!)"):
			reviewList.find("reviewName").text = '%s(Again!)'%(review_name)
		reviewList.find("dueTime").text = rtime.now().review_days(times=1)#times means after two days should it be reviewed
		reviewList.find("isDue").text = "False"
		self.__write_xml()

	@parse_xml
	def delete_item(self, item_ID):
		reviewList = self.__root.find("reviewList[ID='%s']"%(item_ID))
		reviewList.getparent().remove(reviewList)
		self.__write_xml()		

	def __write_xml(self):
		'''write the xml into the file'''
		self.__tree.write(open("review_list.xml", "w+"), encoding='utf-8', pretty_print=True)










if __name__ == '__main__':
	rx = review_xml()
	rx.complete_item("2")
