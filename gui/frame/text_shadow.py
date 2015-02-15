# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from gtk import FILL, EXPAND
from openbox.theme_elements import themeElements


class TextShadowStringFrame(gtk.Frame):

    def __init__(self, **args):
        gtk.Frame.__init__(self, **args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("text shadow")
        self.callback = None

        self.default = 'shadow=n'
        self.default_tint = 50
        self.default_offset = 1

        self.display = gtk.Entry(max=0)
        self.display.set_editable(False)

        self.shadow = gtk.CheckButton("on/off")
        self.shadow.connect("toggled", self.update_value, "check button 1")

        self.shadowtint = gtk.Adjustment(self.default_tint, -100, 100, 1, 1, 0)
        self.shadowtint.connect("value_changed", self.update_value)
        shadowtint_label = gtk.Label("shadow tint:")
        shadowtint_label.set_alignment(0, 0)
        shadowtint_spin = gtk.SpinButton(self.shadowtint, 0, 0)
        shadowtint_spin.set_numeric(True)
        shadowtint_spin.set_digits(0)

        self.shadowoffset = gtk.Adjustment(self.default_offset, -2, 2, 1, 1, 0)
        self.shadowoffset.connect("value_changed", self.update_value)
        shadowoffset_label = gtk.Label("shadow offset:")
        shadowoffset_label.set_alignment(0, 0)
        shadowoffset_spin = gtk.SpinButton(self.shadowoffset, 0, 0)
        shadowoffset_spin.set_numeric(True)
        shadowoffset_spin.set_digits(0)

        reset = gtk.Button(label="reset")
        reset.connect("clicked", self.reset)

        table = gtk.Table(2, 2)
        i = 0
        table.attach(self.display, 0, 2, i, i+1, FILL, EXPAND, 5, 5)
        i += 1
        table.attach(shadowtint_label, 0, 1, i, i+1, FILL, EXPAND, 5, 5)
        table.attach(shadowtint_spin, 1, 2, i, i+1, FILL, EXPAND, 5, 5)
        i += 1
        table.attach(shadowoffset_label, 0, 1, i, i+1, FILL, EXPAND, 5, 5)
        table.attach(shadowoffset_spin, 1, 2, i, i+1, FILL, EXPAND, 5, 5)
        i += 1
        table.attach(self.shadow, 0, 1, i, i+1, FILL, EXPAND, 5, 5)
        table.attach(reset, 1, 2, i, i+1, FILL, EXPAND, 5, 5)
        table.show_all()

        self.add(table)
        self.show_all()
        self.update_value()

    def update_value(self, *args):
        if self.shadow.get_active():
            self.value = "shadow=y:shadowtint={}:shadowoffset={}".format(
                self.shadowtint.get_value(), self.shadowoffset.get_value())
        else:
            self.value = "shadow=n"

        self.display.set_text(self.value)
        if self.callback and self.sensitive:
            self.callback(self.value)

    def configure(self, name, string, theme):
        self.sensitive = False
        self.set_value_by_str(string)
        if 'default' in themeElements[name]:
            self.default = themeElements[name]['default']
            self.sensitive = True

    def reset(self, *args):
        self.shadowtint.set_value(self.default_tint)
        self.shadowoffset.set_value(self.default_offset)
        self._set_value_by_str(self.default)

    def set_value_by_str(self, string):
        self.reset()
        self._set_value_by_str(string)

    def _set_value_by_str(self, string):
        string = string.lower()
        for substr in string.split(":"):
            (name, value) = substr.split("=", 1)
            if name == "shadow":
                if value == "y":
                    self.shadow.set_active(True)
                else:
                    self.shadow.set_active(False)
            elif name == "shadowtint":
                self.shadowtint.set_value(int(value))
            elif name == "shadowoffset":
                self.shadowoffset.set_value(int(value))
        self.update_value

    def get_string(self):
        return self.value
