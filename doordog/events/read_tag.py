import wx
import wx.lib.newevent

# New event for tags reading
OnReadTagEvent, EVT_ON_READ_TAG_EVENT = wx.lib.newevent.NewEvent()
OnReadTagCommandEvent, EVT_ON_READ_TAG_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()