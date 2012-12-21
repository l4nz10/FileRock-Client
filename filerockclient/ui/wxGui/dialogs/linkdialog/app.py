# -*- coding: ascii -*-
#  ______ _ _      _____            _       _____ _ _            _
# |  ____(_) |    |  __ \          | |     / ____| (_)          | |
# | |__   _| | ___| |__) |___   ___| | __ | |    | |_  ___ _ __ | |_
# |  __| | | |/ _ \  _  // _ \ / __| |/ / | |    | | |/ _ \ '_ \| __|
# | |    | | |  __/ | \ \ (_) | (__|   <  | |____| | |  __/ | | | |_
# |_|    |_|_|\___|_|  \_\___/ \___|_|\_\  \_____|_|_|\___|_| |_|\__|
#
# Copyright (C) 2012 Heyware s.r.l.
#
# This file is part of FileRock Client.
#
# FileRock Client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FileRock Client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FileRock Client. If not, see <http://www.gnu.org/licenses/>.
#

"""
This is the app module.




----

This module is part of the FileRock Client.

Copyright (C) 2012 - Heyware s.r.l.

FileRock Client is licensed under GPLv3 License.

"""

#!/usr/bin/env python
# generated by wxGlade 0.6.3 on Sun Jul  1 16:35:09 2012

import wx, threading
from LinkDialog import LinkDialog

class LinkingDialog(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.somethingToWaitOn=threading.Event()
        dialog_3 = LinkDialog(None, -1, "")
        self.SetTopWindow(dialog_3)
        dialog_3.setSync(self.somethingToWaitOn)
        dialog_3.Show()

        return 1

# end of class LinkingDialog

if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = LinkingDialog(0)
    app.MainLoop()
    app.somethingToWaitOn.wait()