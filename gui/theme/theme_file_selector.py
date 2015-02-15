# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import gtk


class ThemeFileSelector(gtk.ScrolledWindow):

    def select(self, treeview, event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            x = int(event.x)
            y = int(event.y)
            pthinfo = treeview.get_path_at_pos(x, y)
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.set_cursor(path, col, 0)
                selection = treeview.get_selection()
                (model, iter) = selection.get_selected()
                path = model.get_value(iter, 1)
                # self.popup.popup( None, None, None, event.button, time)
                if self.callback:
                    self.callback(path, event.button)

    def get_selected(self):
        selection = self.listview.get_selection()
        (model, iter) = selection.get_selected()
        return model.get_value(iter, 1)
        # selection = listview.get_selection()
        # (model,iter) = selection.get_selected()
        # self.selected =  model.get_value(iter, 1)

    def get_themes(self):
        themes = {}
        theme_dir_path = os.getenv('HOME')+'/.themes'
        if os.path.exists(theme_dir_path):
            for theme in os.listdir(theme_dir_path):
                if theme == 'obtheme':
                    continue
                themerc_path = "%s/%s/openbox-3/themerc" % (theme_dir_path, theme)
                if os.path.exists(themerc_path):
                    themes[theme] = themerc_path
        theme_dir_path = '/usr/share/themes'
        if os.path.exists(theme_dir_path):
            for theme in os.listdir(theme_dir_path):
                themerc_path = "%s/%s/openbox-3/themerc" % (theme_dir_path, theme)
                if os.path.exists(themerc_path):
                    themes[theme] = themerc_path
        return themes

    def __init__(self, **args):
        gtk.ScrolledWindow.__init__(self, **args)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.themes = self.get_themes()
        self.selected = None
        self.callback = None

        self.liststore = gtk.ListStore(str, str)
        names = self.themes.keys()
        names.sort()
        for name in names:
            self.liststore.append([name, self.themes[name]])

        self.listview = gtk.TreeView(self.liststore)
        # self.listview.set_rules_hint(True)
        # self.listview.connect('cursor-changed', self.get_selected, self.listview)
        self.listview.connect('button_press_event', self.select)

        i = 0
        for col in ('theme', 'path'):
            tvcol = gtk.TreeViewColumn(col)
            cell = gtk.CellRendererText()
            tvcol.pack_start(cell, True)
            tvcol.add_attribute(cell, 'text', i)
            tvcol.set_sort_column_id(i)
            self.listview.append_column(tvcol)
            i += 1

        self.listview.set_reorderable(True)
        self.set_size_request(100, 100)

        self.add(self.listview)
        self.show_all()
