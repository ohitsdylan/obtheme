# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
from openbox.theme_elements import themeElements


class ThemeElementSelector(gtk.ScrolledWindow):
    def select(self, listview, *args):
        selection = listview.get_selection()
        (model, iter) = selection.get_selected()
        element = model.get_value(iter, 0)
        if self.callback:
            self.callback(element)

    def __init__(self, **args):
        gtk.ScrolledWindow.__init__(self, **args)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.callback = None

        self.liststore = gtk.ListStore(str, str)
        elements = themeElements.keys()
        elements.sort()
        for element in elements:
            self.liststore.append([element, themeElements[element]['type']])

        self.listview = gtk.TreeView(self.liststore)
        self.listview.set_rules_hint(True)
        self.listview.connect('cursor-changed', self.select, self.listview)

        i = 0
        for col in ('element', 'type'):
            tvcol = gtk.TreeViewColumn(col)
            cell = gtk.CellRendererText()
            tvcol.pack_start(cell, True)
            tvcol.add_attribute(cell, 'text', i)
            tvcol.set_sort_column_id(i)
            self.listview.append_column(tvcol)
            i += 1

        self.listview.set_reorderable(True)
        self.set_size_request(500, 100)

        self.add(self.listview)
        self.show_all()
