# -- encoding:utf - 8 --

import sys
import wx 

reload(sys)
sys.setdefaultencoding('utf-8')

class Button(wx.Button):
	def __init__(self, panel, label, size=wx.DefaultSize):
		wx.Button.__init__(self, panel, -1, label=label, size=size)

class AlertMessage(wx.StaticText):
	def __init__(self, panel, label, style):
		wx.StaticText.__init__(self, panel, -1, label=label, style=style)
	def show_message(self, message):
		self.message = message
		self.SetLabel(self.message)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, lambda event:self.SetLabel(''), self.timer)
		self.timer.Start(1000)

