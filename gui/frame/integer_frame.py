# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from openbox.theme_elements import themeElements


class IntegerFrame(gtk.Frame):
    def update_value(self, *arg):
        if self.callback and self.sensitive:
            self.callback(int(self.value.get_value()))

    def configure(self, name, value, theme):
        self.sensitive = False
        value = int(value)
        if 'ubound' in themeElements[name]:
            ubound = themeElements[name]['ubound']
            if value > ubound:
                value = ubound
        else:
            ubound = 100
        self.set_ubound(ubound)
        if 'lbound' in themeElements[name]:
            lbound = themeElements[name]['lbound']
            if value < lbound:
                value = lbound
        else:
            lbound = 0
        if 'default' in themeElements[name]:
            self.default = themeElements[name]['default']
        self.set_lbound(lbound)
        self.set_value(value)
        self.sensitive = True

    def reset(self, *args):
        self.value.set_value(float(self.default))

    def set_value(self, string):
        self.value.set_value(int(string))

    def get_string(self):
        return str(self.value.get_value())

    def set_lbound(self, lbound):
        self.value.lower = int(lbound)

    def set_ubound(self, ubound):
        self.value.upper = int(ubound)

    def __init__(self, **args):
        gtk.Frame.__init__(self, **args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("integer")
        self.default = 1
        self.callback = None

        self.value = gtk.Adjustment(1, 0, 100, 1, 1, 0)
        self.value.connect("value_changed", self.update_value)

        hbox = gtk.HBox(True, 5)
        self.add(hbox)
        boxargs = {'expand': False, 'fill': True, 'padding': 5}

        label = gtk.Label("value:")
        label.set_alignment(0.5, 0.5)
        hbox.pack_start(label, **boxargs)
        label.show()

        spinbutton = gtk.SpinButton(self.value, 0, 0)
        spinbutton.set_numeric(True)
        spinbutton.set_digits(0)
        spinbutton.set_alignment(0.5)
        hbox.pack_start(spinbutton, **boxargs)
        spinbutton.show()

        reset = gtk.Button(label="reset")
        reset.set_alignment(0.5, 0.5)
        reset.connect("clicked", self.reset)
        hbox.pack_start(reset, **boxargs)
        reset.show()

        hbox.show()

        self.update_value()
