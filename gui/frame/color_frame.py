# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from gui.color_button import ColorButton


class ColorFrame(gtk.Frame):

    def __init__(self, **args):
        gtk.Frame.__init__(self, **args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("color")
        self.callback = None

        self.button = ColorButton()
        self.button.connect("color-set", self.update_value)
        self.add(self.button)
        self.button.show()

    def update_value(self, *args):
        if self.callback and self.sensitive:
            self.callback(self.button.get_value())

    def configure(self, name, value, theme):
        self.sensitive = False
        self.button.set_value(value)
        self.sensitive = True
