#!/usr/bin/env python
# generated by wxGlade 0.6.3 on Fri Nov  2 11:23:09 2012

import wx
from ProxyDialog import ProxyDialog

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        dialog_1 = ProxyDialog(None, -1, "")
        self.SetTopWindow(dialog_1)
        dialog_1.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
