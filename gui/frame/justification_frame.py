# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk


class JustificationFrame(gtk.Frame):
    def update_value(self, *args):
        value = self.combobox.get_active_text()
        if self.callback and self.sensitive:
            self.callback(value)

    def configure(self, name, value, theme):
        self.sensitive = False
        value = value.lower()
        model = self.combobox.get_model()
        for i in range(len(model)):
            if model[i][0].lower() == value:
                self.combobox.set_active(i)
                break
        self.sensitive = True

    def __init__(self, **args):
        gtk.Frame.__init__(self, **args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("justification")
        self.callback = None

        self.combobox = gtk.combo_box_new_text()
        self.add(self.combobox)
        self.combobox.append_text('Left')
        self.combobox.append_text('Center')
        self.combobox.append_text('Right')
        self.combobox.connect('changed', self.update_value)
        self.combobox.set_active(0)
        self.combobox.show()
