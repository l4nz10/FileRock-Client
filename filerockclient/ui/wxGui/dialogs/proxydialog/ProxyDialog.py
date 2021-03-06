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
Proxy Dialog module

----

This module is part of the FileRock Client.

Copyright (C) 2012 - Heyware s.r.l.

FileRock Client is licensed under GPLv3 License.

"""

import wx


# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

import os

from filerockclient.ui.wxGui import Messages
from filerockclient.ui.wxGui.constants import IMAGE_PATH


ENABLED = True
DISABLED = False

PROXY_LABELS = [
                'SOCKS4',
                'SOCKS5',
                'HTTP/HTTPS'
               ]

PROXY_LABEL_TO_VALUES = {
                         PROXY_LABELS[0]: 'SOCKS4',
                         PROXY_LABELS[1]: 'SOCKS5',
                         PROXY_LABELS[2]: 'HTTP'
                        }

PROXY_VALUE_TO_LABEL = {
                         'SOCKS4': PROXY_LABELS[0],
                         'SOCKS5': PROXY_LABELS[1],
                         'HTTP': PROXY_LABELS[2]
                        }



class SpinCtrl(wx.SpinCtrl):
    def __init__(self, *args, **kwds):
        super(SpinCtrl, self).__init__(*args, **kwds)
        self.default_value = 0
        self.Bind(wx.EVT_KILL_FOCUS, self.updateValue)
    
    def SetValue(self, value):
        int_value = 0
        try:
            int_value=int(value)
        except:
            pass
        return super(SpinCtrl, self).SetValue(int_value)
    
    def GetValue(self):
        str_value = '0'
        try:
            str_value = str(super(SpinCtrl, self).GetValue())
        except:
            pass
        return str_value
    
    def updateValue(self, env):
        try:
            value_to_set = int(self.GetValue())
        except:
            value_to_set = 1
        self.SetValue(value_to_set)
            

class CtrlText(wx.TextCtrl):

    def __init__(self, *args, **kwds):
        super(CtrlText, self).__init__(*args, **kwds)
        self.default_value = ""
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)

    def onKeyUp(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.SetValue(self.default_value)


class DirPickerCtrl(wx.DirPickerCtrl):
    def __init__(self, *args, **kwds):
        super(DirPickerCtrl, self).__init__(*args, **kwds)
        self.default_value = ""
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)

    def GetValue(self):
        return self.GetPath()

    def SetValue(self, value):
        return self.SetPath(value)

    def onKeyUp(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.SetValue(self.default_value)


class CheckBox(wx.CheckBox):
    def __init__(self, value, *args, **kwds):
        super(CheckBox, self).__init__(*args, **kwds)
        self.default_value = ""
        self.SetValue(value)

    def GetValue(self):
        if super(CheckBox, self).GetValue():
            return u"True"
        else:
            return u"False"

    def SetValue(self, value):
        if value == u"True":
            super(CheckBox, self).SetValue(True)
        else:
            super(CheckBox, self).SetValue(False)

class ReplicaComboBox(wx.ComboBox):
    def __init__(self, *args, **kwds):
        super(ReplicaComboBox, self).__init__(*args, **kwds)
        self.Insert(Messages.CONFIG_NOT_AVAILABLE ,0)
        self.Disable()

    def SetValue(self, value):
        if value is not None:
            return wx.ComboBox.SetValue(self, value)
        self.SetSelection(0)
        return None

class ComboBox(wx.ComboBox):
    def __init__(self, *args, **kwds):
        super(ComboBox, self).__init__(*args, **kwds)
        self.default_value = ""

    def GetValue(self, *args, **kwargs):
        return PROXY_LABEL_TO_VALUES[super(ComboBox, self).GetValue(*args, **kwargs)]

    def SetValue(self, value):
        if value in PROXY_VALUE_TO_LABEL.keys():
            return super(ComboBox, self).SetValue(PROXY_VALUE_TO_LABEL[value])

UserDefinedOptions = "User Defined Options"

WIDGETS = {
    UserDefinedOptions: {
        'proxy_type': lambda parent, val: ComboBox(parent,
                                                   -1,
                                                   val,
                                                   choices=PROXY_LABELS,
                                                   style=wx.CB_READONLY
                                                   ),
        'proxy_host': lambda parent, val: CtrlText(parent, -1, val),
        'proxy_port': lambda parent, val: SpinCtrl(parent,
                                                   -1,
                                                   val,
                                                   style=wx.SP_HORIZONTAL,
                                                   min=0,
                                                   max=655360),
        'proxy_rdns': lambda parent, val: CheckBox(val, parent),
        'proxy_username': lambda parent, val: CtrlText(parent, -1, val),
        'proxy_password': lambda parent, val: CtrlText(parent, -1, val)
    }
}
# end wxGlade

class ProxyDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ProxyDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX
        wx.Dialog.__init__(self, *args, **kwds)
        self.button_ok = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ProxyDialog.__set_properties
        self.SetTitle("Proxy Settings")
        # end wxGlade
        pathname = os.path.join(IMAGE_PATH, 'other/FileRock.ico')
        _icon = wx.Icon(pathname, wx.BITMAP_TYPE_ICO)
        self.SetIcon(_icon)

    def __do_layout(self):
        # begin wxGlade: ProxyDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.button_ok, 0, wx.TOP|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade
        self.container = sizer_2
        self.init_config()
# end of class ProxyDialog

    def init_config(self):
        self.sections_grid = {}
        self.sections_panel = {}
        self.options = {}
        self.labels = {
                       'proxy_type': u'Proxy type',
                       'proxy_host': u'Host',
                       'proxy_port': u'Port',
                       'proxy_rdns': u'Resolve DNS',
                       'proxy_username': u'Username',
                       'proxy_password': u'Password'
        }

        self.tooltips = {
                        'proxy_type': u'Proxy type',
                        'proxy_host': u'Host',
                        'proxy_port': u'Port',
                        'proxy_rdns': u'Resolve DNS',
                        'proxy_username': u'Username',
                        'proxy_password': u'Password'
        }


        self.visible_keys = {UserDefinedOptions: ['proxy_type',
                                                  'proxy_host',
                                                  'proxy_port',
                                                  'proxy_rdns',
                                                  'proxy_username',
                                                  'proxy_password'
                                                 ]}


        self.key_order = [(UserDefinedOptions, 'proxy_type'),
                          (UserDefinedOptions, 'proxy_host'),
                          (UserDefinedOptions, 'proxy_port'),
                          (UserDefinedOptions, 'proxy_rdns'),
                          (UserDefinedOptions, 'proxy_username'),
                          (UserDefinedOptions, 'proxy_password')
                         ]

        self.add_section('Configuration')

    def add_section(self, label):
        self.container.Insert(0,self.create_panel(label), 1, wx.ALL | wx.EXPAND, 0)

    def create_panel(self, label):
        panel = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL)
        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer = wx.FlexGridSizer(6, 2, 5, 20)
        grid_sizer.AddGrowableCol(1)
        sizer_21.Add(grid_sizer, 1, wx.ALL | wx.VERTICAL, 4)
        panel.SetSizer(sizer_21)
        self.sections_grid[label] = grid_sizer
        self.sections_panel[label] = panel
        return panel

    def updateConfig(self, cfg):
        self.cfg = cfg
        for section, option in self.key_order:
            if section in self.visible_keys.keys() \
            and option in self.visible_keys[section]\
            and section in self.cfg\
            and option in self.cfg[section]:
                if section not in self.options:
                    self.options[section] = {}
#                    self.add_section(Messages.PANEL3_USER_SECTION_TITLE)
                if section != 'NOCFG':
                    value = self.cfg[section][option]
                else:
                    value = None
                self.insertupdate_setting(section, option, value)
        self.Fit()
        size = self.GetMinSize()
        size[1]=-1
        self.SetMaxSize(size)

    def collectValues(self, onlyifnew=False):
        cfg = {}
        somethingsnew = False
        for section in self.options:
            cfg[section] = {}
            for option in self.options[section]:
                value = self.options[section][option].GetValue()
                default_value = self.options[section][option].default_value
                cfg[section][option] = value
                if value != default_value:
                    somethingsnew = True
        if onlyifnew and not somethingsnew:
            return {}
        else:
            return cfg

    def getConfig(self):
        cfg = self.collectValues(True)
        if 'NOCFG' in cfg:
            cfg.pop('NOCFG')
        return cfg

    def insertupdate_setting(self, section, key, value):
        if key not in self.visible_keys[section]:
            return
        if key not in self.options[section]:
            self.add_option(section, key, value)
        self.options[section][key].SetValue(value)
        self.options[section][key].default_value = value

    def insertupdate_System_setting(self, section, key, value):
#        self.system_list_ctrl.insertupdate_key_value(section, key, value)
        pass

    def insertupdate_Client_setting(self, section, key, value):
        pass

    def create_static_text(self, parent, key):
        staticText = wx.StaticText(parent, -1, self.labels[key])
        font = staticText.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        staticText.SetFont(font)
        return staticText

    def create_ctrl_text(self, parent, label, value, path=False):
        if path:
            ctrlText = DirPickerCtrl(parent, -1, value)
        else:
            ctrlText = CtrlText(parent, -1, value)
        if label in self.tooltips:
            ctrlText.SetToolTipString(self.tooltips[label])
        return ctrlText

    def add_option(self, section, key, value, path=False, checkbox=False):
        parent = self.sections_panel['Configuration']
        grid = self.sections_grid['Configuration']
        staticText = self.create_static_text(parent, key)
        self.options[section][key] = WIDGETS[section][key](parent, value)
        if key in self.tooltips:
            self.options[section][key].SetToolTipString(self.tooltips[key])
        self.add_options_to_grid(grid, staticText, self.options[section][key])

    def add_options_to_grid(self, grid, staticText, ctrlText):
        grid.Add(staticText, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL, 2)
        grid.Add(ctrlText, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2)

