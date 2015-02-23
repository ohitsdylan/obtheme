# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import gtk
import os
from obtheme import VERSION
from xbm.editor import XBMEditor
from openbox.theme_elements import imageButtons

# FIXME class not used


class XBMWindow:
    def display_about(self, *args):
        about_msg = "XBM Editor %s\n\n GTK+ X BitMap editor \n\nCopyright \302\251 2009 Xyne " % VERSION

        label = gtk.Label(about_msg)
        label.set_justify(gtk.JUSTIFY_CENTER)

        dialog = gtk.Dialog(None, None, gtk.DIALOG_DESTROY_WITH_PARENT, ('_Close', 1))
        dialog.set_title("About XBM Editor")
        dialog.vbox.pack_start(label, False, True, 10)
        dialog.vbox.show_all()
        response = dialog.run()
        logging.debug(response)
        dialog.destroy()

    def display_help(self, *args):
        help_msg = '''Left-click to set a pixel, right-click to unset it.

Images will be saved along the themerc file.
'''

        textview = gtk.TextView()
        textview.get_buffer().set_text(help_msg)
        textview.set_editable(False)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textview.set_left_margin(5)
        textview.set_right_margin(5)

        textview_window = gtk.ScrolledWindow()
        textview_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        textview_window.add(textview)

        dialog = gtk.Dialog(None, None, gtk.DIALOG_DESTROY_WITH_PARENT, ('_Close', 1))
        dialog.set_title("XBM Editor Info")
        dialog.set_default_size(300, 250)
        dialog.vbox.pack_start(textview_window, True, True, 5)
        dialog.vbox.show_all()
        response = dialog.run()
        logging.debug(response)
        dialog.destroy()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("XBM Editor")
        self.window.connect("destroy", self.destroy)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.file_name = None
        self.unsaved = False
        self.theme_dir = os.getenv('HOME')+'/.themes/obtheme/openbox-3'
        self.callback = None

        accel_group = gtk.AccelGroup()
        self.window.add_accel_group(accel_group)

        file_menu_open = gtk.ImageMenuItem('_Open...')
        file_menu_open.connect("activate", self.open_xbm, 'open')
        file_menu_open.add_accelerator("activate",
                                       accel_group, ord('o'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        file_menu_open.set_image(gtk.image_new_from_stock(
            gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU))

        file_menu_save = gtk.ImageMenuItem('_Save')
        file_menu_save.connect("activate", self.save_xbm, 'save')
        file_menu_save.add_accelerator("activate",
                                       accel_group, ord('s'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        file_menu_save.set_image(gtk.image_new_from_stock(
            gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU))

        file_menu_save_as = gtk.ImageMenuItem('Save _As...')
        file_menu_save_as.connect("activate", self.save_xbm, 'save as')
        file_menu_save_as.add_accelerator("activate",
                                          accel_group, ord('s'),
                                          (gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK),
                                          gtk.ACCEL_VISIBLE)
        file_menu_save_as.set_image(gtk.image_new_from_stock(
            gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_MENU))

        file_menu_separator = gtk.SeparatorMenuItem()

        file_menu_quit = gtk.ImageMenuItem("_Quit")
        # file_menu_quit.connect("activate", gtk.main_quit)
        file_menu_quit.add_accelerator("activate",
                                       accel_group, ord('q'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        file_menu_quit.set_image(gtk.image_new_from_stock(
            gtk.STOCK_QUIT, gtk.ICON_SIZE_MENU))

        file_submenu = gtk.Menu()
        file_submenu.append(file_menu_open)
        file_submenu.append(file_menu_save)
        file_submenu.append(file_menu_save_as)
        file_submenu.append(file_menu_separator)
        file_submenu.append(file_menu_quit)
        file_submenu.show_all()

        file_menu = gtk.ImageMenuItem("_File")
        file_menu.set_submenu(file_submenu)
        file_menu.show()

        info_menu = gtk.ImageMenuItem('_Info')
        info_menu.connect("activate", self.display_help)
        info_menu.add_accelerator("activate",
                                  accel_group, ord('h'),
                                  gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        info_menu.set_image(gtk.image_new_from_stock(
            gtk.STOCK_INFO, gtk.ICON_SIZE_MENU))

        about_menu = gtk.ImageMenuItem('_About')
        about_menu.connect("activate", self.display_about)
        # about_menu.add_accelerator("activate",
        #                            accel_group, ord('h'),
        #                            gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
        about_menu.set_image(gtk.image_new_from_stock(
            gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU))

        help_submenu = gtk.Menu()
        help_submenu.append(info_menu)
        help_submenu.append(about_menu)
        help_submenu.show_all()

        help_menu = gtk.ImageMenuItem("_Help")
        help_menu.set_submenu(help_submenu)
        help_menu.show()

        menu_bar = gtk.MenuBar()
        menu_bar.append(file_menu)
        menu_bar.append(help_menu)

        open_button = gtk.ToolButton(stock_id=gtk.STOCK_OPEN)
        save_button = gtk.ToolButton(stock_id=gtk.STOCK_SAVE)
        save_as_button = gtk.ToolButton(stock_id=gtk.STOCK_SAVE_AS)

        open_button.connect("clicked", self.open_xbm, 'open')
        save_button.connect("clicked", self.save_xbm, 'save')
        save_as_button.connect("clicked", self.save_xbm, 'save as')

        toolbar = gtk.Toolbar()
        toolbar.insert(open_button, 0)
        toolbar.insert(save_button, 1)
        toolbar.insert(save_as_button, 2)

        editor = XBMEditor()
        editor.callback = self.save_preview

        cm = gtk.Button(label='-')
        cm.connect('clicked', self.col_minus)
        cl = gtk.Label('cols')
        cp = gtk.Button(label='+')
        cp.connect('clicked', self.col_plus)
        rm = gtk.Button(label='-')
        rm.connect('clicked', self.row_minus)
        rl = gtk.Label('rows')
        rp = gtk.Button(label='+')
        rp.connect('clicked', self.row_plus)

        self.cl = cl
        self.rl = rl

        buttonbox = gtk.HBox(True, 0)
        buttonbox.pack_start(cm, True, True, 0)
        buttonbox.pack_start(cl, True, True, 0)
        buttonbox.pack_start(cp, True, True, 0)
        buttonbox.pack_start(rm, True, True, 0)
        buttonbox.pack_start(rl, True, True, 0)
        buttonbox.pack_start(rp, True, True, 0)
        buttonbox.show_all()

        combobox = gtk.combo_box_new_text()
        combobox.append_text('')
        combobox.set_active(0)
        imagebutton_list = imageButtons.keys()
        imagebutton_list.sort()
        for key in imagebutton_list:
            combobox.append_text(key)
        combobox.connect('changed', self.load_imagebutton)
        self.combobox = combobox

        default_button = gtk.Button('default')
        default_button.connect("clicked", self.remove_image)

        hbox = gtk.HBox(False, 0)
        hbox.pack_start(combobox, True, True, 0)
        hbox.pack_start(default_button, False, False, 0)
        hbox.show_all()

        infopanel = gtk.ScrolledWindow()
        infopanel.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.info = gtk.TextView()
        self.info.set_wrap_mode(gtk.WRAP_WORD)
        self.info.set_left_margin(5)
        self.info.set_right_margin(5)
        self.info.set_size_request(200, 40)
        self.info.set_editable(False)
        infopanel.add(self.info)

        box = gtk.VBox(False, 0)
        box.pack_start(menu_bar, False, False, 0)
        box.pack_start(toolbar, False, False, 0)
        box.pack_start(editor, True, True, 0)
        box.pack_start(hbox, False, False, 0)
        box.pack_start(infopanel, False, False, 0)
        box.pack_start(buttonbox, False, False, 0)
        box.show_all()
        self.window.add(box)
        self.window.show_all()
        self.window.show()
        self.editor = editor
        self.set_labels()

    def destroy(self, widget, data=None):
        pass

    def get_default(self, name):
        fpath = '/usr/share/doc/openbox/xbm/' + name + '.xbm'
        if os.path.exists(fpath):
            int_default = fpath
        else:
            int_default = None
        for default in imageButtons[name]['default']:
            if default is not None:
                fpath = self.theme_dir + '/' + default + '.xbm'
                if os.path.exists(fpath):
                    return fpath
                else:
                    fpath = '/usr/share/doc/openbox/xbm/' + default + '.xbm'
                    if os.path.exists(fpath) and int_default is None:
                        int_default = fpath
        return int_default

    def load_imagebutton(self, combobox):
        name = combobox.get_active_text()
        if name == '':
            self.file_name = None
            self.info.get_buffer().set_text('')
            return
        self.info.get_buffer().set_text(imageButtons[name]['info'])
        fpath = self.theme_dir + '/' + name + '.xbm'
        if not os.path.exists(fpath):
            fpath = self.get_default(name)
        if fpath is not None:
            if self.editor.load_xbm(fpath):
                self.set_labels()
                self.file_name = fpath
            else:
                logging.error("Error: unable to open %s\n" % fpath)
        else:
            logging.error("Error: no default could be found for %s.xbm\n" % name)

    def remove_image(self, *args):
        name = self.combobox.get_active_text()
        if name == '':
            self.editor.clear()
        else:
            fpath = self.theme_dir + '/' + name + '.xbm'
            if os.path.exists(fpath):
                os.remove(fpath)
                self.load_imagebutton(self.combobox)

    def save_preview(self):
        self.unsaved = False
        name = self.combobox.get_active_text()
        if name != '':
            fpath = self.theme_dir + '/' + name + '.xbm'
            self.editor.save_xbm(fpath)
        if self.callback:
            self.callback()

    def set_labels(self):
        w, h = self.editor.get_dim()
        self.cl.set_text("cols(%d)" % (w))
        self.rl.set_text("rows(%d)" % (h))
        self.editor.draw_xbm()

    def col_minus(self, widget):
        w = self.editor.width
        if w > 1:
            self.editor.set_width(w-1)
            self.set_labels()

    def col_plus(self, widget):
        w = self.editor.width
        self.editor.set_width(w+1)
        self.set_labels()

    def row_minus(self, widget):
        h = self.editor.height
        if h > 1:
            self.editor.set_height(h-1)
            self.set_labels()

    def row_plus(self, widget):
        h = self.editor.height
        self.editor.set_height(h+1)
        self.set_labels()

    def open_xbm(self, widget, arg=None, *args):
        filter_all = gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")

        filter_xpm = gtk.FileFilter()
        filter_xpm.set_name("XBM")
        filter_xpm.add_pattern("*.xbm")
        name = self.file_name
        dialog = gtk.FileChooserDialog('Select an XBM file', None, gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.add_filter(filter_xpm)
        dialog.add_filter(filter_all)
        dialog.set_default_response(gtk.RESPONSE_OK)
        if name is not None:
            dialog.set_current_folder(os.path.dirname(name))
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            name = dialog.get_filename()
        else:
            name = None
        dialog.destroy()
        if name is not None:
            if self.editor.load_xbm(name):
                self.set_labels()
                self.file_name = name
                model = self.combobox.get_model()
                name = os.path.basename(name)
                self.combobox.set_active(0)
                for i in range(len(model)):
                    if model[i][0] == name:
                        self.combobox.set_active(i)
                        break
            else:
                logging.error("Error: unable to open %s\n" % name)

    def save_xbm(self, widget=None, arg=None, *args):
        name = self.file_name
        if name is None or arg == 'save as':
            if arg == 'save as':
                button = gtk.STOCK_SAVE
            else:
                button = gtk.STOCK_SAVE
            dialog = gtk.FileChooserDialog('Select an XBM file', None, gtk.FILE_CHOOSER_ACTION_SAVE,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, button, gtk.RESPONSE_OK))
            filter_all = gtk.FileFilter()
            filter_all.set_name("All files")
            filter_all.add_pattern("*")

            filter_xpm = gtk.FileFilter()
            filter_xpm.set_name("XBM")
            filter_xpm.add_pattern("*.xbm")
            dialog.add_filter(filter_xpm)
            dialog.add_filter(filter_all)
            if name is not None:
                dialog.set_current_folder(os.path.dirname(name))
                dialog.set_current_name(os.path.basename(name))
            dialog.set_default_response(gtk.RESPONSE_OK)
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                name = dialog.get_filename()
            dialog.destroy()
        if name is not None:
            self.file_name = name
            if self.editor.save_xbm(name):
                self.unsaved = False
                self.file_name = name
            else:
                self.save_xbm(None, 'save as')

    def main(self):
        gtk.main()
