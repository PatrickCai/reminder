#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import wx 

import xerox

import widget as mw
import review_xml as rxml
import review_list as rlist
reload(sys)
sys.setdefaultencoding('utf-8')

class Frame(wx.Frame):
	def __init__(self, parent=None, id=-1, title=None, 
				 style=wx.CLOSE_BOX, ):
		wx.Frame.__init__(self, parent, id, title,
						  style=style, size=(550, 300))
		self.main_panel = wx.Panel(self, -1, size=(550,300))
	#create the widgets!

		#static text
		self.static_text_content = ['content:', 'times:', 'due:']
		number_of_contents = len(self.static_text_content)
		static_text_widgets_list = []
		for itimes in range(number_of_contents):
			static_text_widgets_list.append(wx.StaticText(self.main_panel, -1, label=self.static_text_content[itimes],
														  style=wx.ALIGN_CENTRE,))

		# content detail
		self.review_content = wx.TextCtrl(self.main_panel, -1, size=(160, -1))
		self.review_times = wx.StaticText(self.main_panel, -1, label='0',
									 style=wx.ALIGN_CENTRE)
		self.review_due_days = wx.StaticText(self.main_panel, -1, label='0',
										style=wx.ALIGN_CENTRE)
		content_detail_widgets_list = list([self.review_content, self.review_times, self.review_due_days])

		#control button
		self.add_button = mw.Button(self.main_panel, 'Add', )
		self.complete_button = mw.Button(self.main_panel, 'Complete')
		self.delete_button = mw.Button(self.main_panel, 'Delete')
		control_button_list = list([self.add_button, self.complete_button, self.delete_button])

		# alert mess age & next page & setting
		self.alert_message = mw.AlertMessage(self.main_panel, label=u'',
									  style=wx.ALIGN_CENTRE)
		self.next_button = mw.Button(self.main_panel, 'Next', size=(60, -1))
		self.setting_button = mw.Button(self.main_panel, 'Setting', size=(60, -1))


	#for view!
		#set the vertical gap,horizontal gap
		sizer_vgap =  30
		sizer_hgap = 10
		sizer_border = 10
		border_flag = wx.BOTTOM

		static_sizer = wx.GridSizer(rows=3, cols=1, vgap=sizer_vgap)
		for widget in static_text_widgets_list:
			static_sizer.Add(widget, )

		content_sizer = wx.GridSizer(rows=3, cols=1, vgap=25)
		for widget in content_detail_widgets_list:
			content_sizer.Add(widget,)

		button_sizer = wx.GridSizer(rows=3, cols=1, vgap=sizer_vgap)
		for widget in control_button_list:
			button_sizer.Add(widget, )

		left_sizer = wx.GridSizer(rows=1, cols=3)
		left_sizer.Add(static_sizer, 0)
		left_sizer.Add(content_sizer, 0, flag=wx.LEFT, border=-50)
		left_sizer.Add(button_sizer, 0, flag=wx.LEFT, border=30)

		right_sizer = wx.GridSizer(rows=3, cols=1)
		right_sizer.Add(self.alert_message, flag=wx.TOP, border=40)
		right_sizer.Add(self.next_button, flag=wx.TOP, border=40)
		right_sizer.Add(self.setting_button, flag=wx.TOP, border=30)

		overall_sizer = wx.GridSizer(rows=1, cols=2,)
		overall_sizer.Add(left_sizer, flag=wx.LEFT|wx.TOP, border=60)
		overall_sizer.Add(right_sizer, flag=wx.LEFT, border=180 )
 
		self.main_panel.SetSizer(overall_sizer)
		self.main_panel.Fit()

	#Initializing!
		#check the update
		self.rl = rlist.review_list()
		self.rl.check_update()
		#set the content into the panel
		self.rl.fetch_review_items()
		self.change_content_detail()


	#for controlling!
		self.add_button.Bind(wx.EVT_BUTTON, self.add_item)
		self.complete_button.Bind(wx.EVT_BUTTON, self.complete_dlg)
		self.delete_button.Bind(wx.EVT_BUTTON, self.delete_dlg)
		self.next_button.Bind(wx.EVT_BUTTON, self.debug_info)

	def add_item(self, event):
		review_name = xerox.paste()
		self.rl.add_item(review_name)
		self.alert_message.show_message("Added!")

	def complete_dlg(self, event):
		'''Pop out a dialog to choose whether the review item is completed or not'''
		if self.rl.first_item:
			dlg = wx.Dialog(None, -1, size=(300, 130),)
			complete_choice = wx.Button(dlg, wx.ID_OK, "Complete!", pos=(180, 40))
			once_again = wx.Button(dlg, wx.ID_CANCEL, "Once again!", pos=(40, 40))
			retcode = dlg.ShowModal()
			if retcode == wx.ID_OK:
				self.complete_item()
			else:
				self.once_again()
			dlg.Destroy()
		else:
			self.alert_message.show_message("No item!")


	def complete_item(self):
		self.rl.complete_item()
		self.change_content_detail()
		self.alert_message.show_message("Completed!")

	def once_again(self):
		self.rl.once_again()
		self.change_content_detail()
		self.alert_message.show_message("Two days later!")

	def change_content_detail(self):
		if self.rl.first_item:
			self.review_content.SetLabel(self.rl.first_item.review_name)
			self.review_times.SetLabel(self.rl.first_item.times)
			self.review_due_days.SetLabel(self.rl.first_item.due_days)
		else:
			self.review_content.SetLabel("")
			self.review_times.SetLabel('0')
			self.review_due_days.SetLabel('0')

	def delete_dlg(self, event):
		if self.rl.first_item:
			dlg = wx.wx.Dialog(None, -1, size=(300, 130))
			delete_ok = wx.Button(dlg, wx.ID_OK, "OK", pos=(180, 40))
			cancel_button = wx.Button(dlg, wx.ID_CANCEL, "CANCEL", pos=(40, 40))
			retcode = dlg.ShowModal()
			if retcode == wx.ID_OK:
				self.delete_item()
			dlg.Destroy()
		else:
			self.alert_message.show_message("No item!")

	def delete_item(self): 
		self.rl.delete_item()
		self.change_content_detail()
		self.alert_message.show_message("Deleted!")

	def debug_info(self, event):
		self.rl.debug_info()

class App(wx.App):
	def __init__(self, redirect=False, filename=None):
		wx.App.__init__(self,redirect,filename)

	def OnInit(self):
		self.frame = Frame(parent=None, id=-1, title=u'复习' )
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

	def OnExit(self):
		pass

if __name__ == '__main__':
	app = App(redirect=True)
	app.MainLoop()
