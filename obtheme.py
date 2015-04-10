#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009  Xyne
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# (version 2) as published by the Free Software Foundation.
#
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from __future__ import absolute_import

import logging
logging.basicConfig(level=logging.DEBUG)

# METADATA
# Version: 0.7
VERSION = '0.7'

import pygtk
pygtk.require('2.0')
import gtk
import gobject


import os
import os.path
import re
import shutil
import subprocess

from utils.general_utils import (read_file, write_file, clear_dir)
from openbox.theme_elements import themeElements, get_config_file
from gui.frame.integer_frame import IntegerFrame
from gui.frame.color_frame import ColorFrame
from gui.frame.justification_frame import JustificationFrame
from gui.frame.texture_frame import TextureFrame
from gui.frame.text_shadow import TextShadowStringFrame
from gui.theme.theme import Theme
from gui.theme.theme_element_selector import ThemeElementSelector
from gui.theme.theme_file_selector import ThemeFileSelector
from gui.dialog import dialog_msg
from utils import fuse_utils as fuse_obj
from xbm.window import XBMWindow

gobject.threads_init()
gtk.gdk.threads_init()

# main window size
# customize to your taste
WIN_WIDTH = 1100
WIN_HEIGHT = 700


class ObTheme:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("ObTheme")
        self.window.set_default_size(WIN_WIDTH, WIN_HEIGHT)
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete_event", self.delete_event)
        self.window.set_position(gtk.WIN_POS_CENTER)

        self.src_dir = '/tmp/obtheme_preview'
        self.preview_themerc_dir = "{}{}".format(os.getenv('HOME'),
                                                 '/.themes/obtheme/openbox-3')
        config_home = os.getenv('XDG_CONFIG_HOME')
        if not config_home:
            config_home = "{}{}".format(os.getenv('HOME'), '/.config')
            logging.warning("The environment variable 'XDG_CONFIG_HOME' is not set\n"
                            "Defaulting to {}.\n".format(config_home))
        self.openbox_config_path = get_config_file(config_home)
        if not self.openbox_config_path:
            raise OSError("Missing Openbox file. Bail out.")

        self.theme = Theme()
        self.theme.callback = self.refresh

        self.selection = None
        self.previous_theme = None
        self.file_name = None
        self.unsaved = False
        self.preview_mode = False
        self.themerc = None

        menu_list = self.setupMenu()
        menu_bar = gtk.MenuBar()
        menu_bar.append(menu_list['file'])
        menu_bar.append(menu_list['theme'])
        menu_bar.append(menu_list['tools'])
        menu_bar.append(menu_list['help'])

        self.frames = {}
        integer = IntegerFrame()
        self.frames['integer'] = integer
        integer.callback = self.update

        color = ColorFrame()
        self.frames['color'] = color
        color.callback = self.update

        text_shadow_string = TextShadowStringFrame()
        self.frames['text shadow string'] = text_shadow_string
        text_shadow_string.callback = self.update

        justification = JustificationFrame()
        self.frames['justification'] = justification
        justification.callback = self.update

        texture = TextureFrame()
        self.frames['texture'] = texture
        texture.callback = self.update

        infopanel = gtk.ScrolledWindow()
        infopanel.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        infolabel = gtk.Label(' information:')
        infolabel.set_alignment(0, 1)
        self.info = gtk.TextView()
        self.info.set_wrap_mode(gtk.WRAP_WORD)
        self.info.set_left_margin(5)
        self.info.set_right_margin(5)
        self.info.set_size_request(400, 50)
        self.info.set_editable(False)
        infopanel.add(self.info)

        theme_element_selector = ThemeElementSelector()
        theme_element_selector.callback = self.select
        themelist = ThemeFileSelector()
        themelist.callback = self.open_from_list

        hpane = gtk.HPaned()
        hpane.add1(theme_element_selector)
        hpane.add2(themelist)
        hpane.show_all()

        vpane = gtk.VPaned()
        vpane.add1(infopanel)
        vpane.add2(hpane)
        vpane.show_all()

        table = gtk.Table(rows=7, columns=4, homogeneous=False)
        i = 0
        j = 0
        table.attach(integer, i, i+2, j, j+1)
        i += 2
        table.attach(texture, i, i+1, j, j+3)
        i = 0
        j += 1
        table.attach(color, i, i+1, j, j+1)
        i += 1
        table.attach(justification, i, i+1, j, j+1)
        i = 0
        j += 1
        table.attach(text_shadow_string, i, i+2, j, j+1)
        table.show_all()

        hbox = gtk.HBox()
        hbox.pack_start(table, False, False, 2)
        hbox.pack_start(self.theme.palette, True, True, 2)
        hbox.show_all()

        vbox = gtk.VBox()
        vbox.pack_start(menu_bar, False, False, 2)
        vbox.pack_start(hbox, False, False, 2)
        vbox.pack_start(infolabel, False, False, 2)
        vbox.pack_start(vpane, True, True, 2)
        vbox.show_all()

        self.select(None)
        self.window.add(vbox)
        self.window.show_all()
        self.window.show()

    def setupMenu(self):

        accel_group = gtk.AccelGroup()
        self.window.add_accel_group(accel_group)

        file_menu_open = gtk.ImageMenuItem(gtk.STOCK_OPEN)
        file_menu_open.connect("activate", self.open_theme, 'open')
        file_menu_open.add_accelerator("activate",
                                       accel_group, ord('o'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        file_menu_open.set_image(gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_MENU))

        file_menu_save = gtk.ImageMenuItem(gtk.STOCK_SAVE)
        file_menu_save.connect("activate", self.save_theme, 'save')
        file_menu_save.add_accelerator("activate",
                                       accel_group, ord('s'),
                                       gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        file_menu_save.set_image(gtk.image_new_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_MENU))

        file_menu_save_as = gtk.ImageMenuItem(gtk.STOCK_SAVE_AS)
        file_menu_save_as.connect("activate", self.save_theme, 'save as')
        file_menu_save_as.add_accelerator("activate",
                                          accel_group, ord('s'),
                                          (gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK), gtk.ACCEL_VISIBLE)
        file_menu_save_as.set_image(gtk.image_new_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_MENU))

        # file_menu_install_as = gtk.ImageMenuItem('Install As...')
        # file_menu_install_as.connect("activate", self.install,'install as')
        # file_menu_install_as.add_accelerator("activate",accel_group,ord('i'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
        # file_menu_install_as.set_image(gtk.image_new_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_MENU))

        # file_menu_import = gtk.ImageMenuItem('_Import...')
        # file_menu_import.connect("activate", self.open_theme, 'import')
        # file_menu_import.add_accelerator("activate",accel_group,ord('i'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
        # file_menu_import.set_image(gtk.image_new_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_MENU))

        file_menu_separator = gtk.SeparatorMenuItem()

        file_menu_quit = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        file_menu_quit.connect("activate", self.quit_app)
        # file_menu_quit.add_accelerator("activate",
        #                                accel_group, ord('q'),
        #                                gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # file_menu_quit.set_image(gtk.image_new_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_MENU))

        file_submenu = gtk.Menu()
        file_submenu.append(file_menu_open)
        file_submenu.append(file_menu_save)
        file_submenu.append(file_menu_save_as)
        # file_submenu.append(file_menu_install_as)
        # file_submenu.append(file_menu_import)
        file_submenu.append(file_menu_separator)
        file_submenu.append(file_menu_quit)
        file_submenu.show_all()

        file_menu = gtk.ImageMenuItem('_File')
        file_menu.set_submenu(file_submenu)
        file_menu.show()

        theme_menu_import = gtk.ImageMenuItem('_Import...')
        theme_menu_import.connect("activate", self.open_theme, 'import')
        theme_menu_import.add_accelerator("activate", accel_group, ord('i'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # theme_menu_import.set_image(gtk.image_new_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_MENU))

        theme_menu_preview = gtk.CheckMenuItem('_Preview')
        theme_menu_preview.connect("toggled", self.toggle_preview_mode)
        theme_menu_preview.add_accelerator("activate", accel_group, ord('p'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # theme_menu_preview.set_image(gtk.image_new_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_MENU))
        self.preview_mode_checkbox = theme_menu_preview

        # theme_menu_restore = gtk.ImageMenuItem('_Restore')
        # theme_menu_restore.connect("activate", self.restore)
        # theme_menu_restore.add_accelerator("activate",accel_group,ord('r'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
        # theme_menu_restore.set_image(gtk.image_new_from_stock(gtk.STOCK_REVERT_TO_SAVED, gtk.ICON_SIZE_MENU))

        theme_submenu = gtk.Menu()
        theme_submenu.append(theme_menu_import)
        theme_submenu.append(theme_menu_preview)
        # theme_submenu.append(theme_menu_restore)
        theme_submenu.show_all()

        theme_menu = gtk.ImageMenuItem("_Theme")
        theme_menu.set_submenu(theme_submenu)
        theme_menu.show()

        info_menu = gtk.ImageMenuItem(gtk.STOCK_INFO)
        info_menu.connect("activate", self.display_help)
        info_menu.add_accelerator("activate", accel_group, ord('h'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        info_menu.set_image(gtk.image_new_from_stock(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU))

        about_menu = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        about_menu.connect("activate", self.display_about)
        # about_menu.add_accelerator("activate",accel_group,ord('h'),gtk.gdk.CONTROL_MASK,gtk.ACCEL_VISIBLE)
        about_menu.set_image(gtk.image_new_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU))

        help_submenu = gtk.Menu()
        help_submenu.append(info_menu)
        help_submenu.append(about_menu)
        help_submenu.show_all()

        help_menu = gtk.ImageMenuItem(gtk.STOCK_HELP)
        help_menu.set_submenu(help_submenu)
        help_menu.show()

        xbm_menu = gtk.ImageMenuItem('_XBM Editor')
        xbm_menu.connect("activate", self.open_xbm_editor)
        # xbm_menu.connect("activate", os.system('python xbm-editor'))
        xbm_menu.add_accelerator("activate", accel_group, ord('x'), gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)
        # xbm_menu.set_image(gtk.image_new_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU))

        tools_submenu = gtk.Menu()
        tools_submenu.append(xbm_menu)
        tools_submenu.show_all()

        tools_menu = gtk.ImageMenuItem("Too_ls")
        tools_menu.set_submenu(tools_submenu)
        tools_menu.show()

        return {
            'file': file_menu,
            'theme': theme_menu,
            'tools': tools_menu,
            'help': help_menu
        }

    def quit_app(self, *args):
        self.window.destroy()
        self.unmount_preview_dir()
        gtk.main_quit()

    def display_about(self):
        about_msg = "ObTheme {}\n\n GTK+ Openbox theme editor \n\nCopyright \302\251 2009 Xyne ".format(VERSION)

        label = gtk.Label(about_msg)
        label.set_justify(gtk.JUSTIFY_CENTER)

        dialog = gtk.Dialog(None, None, gtk.DIALOG_DESTROY_WITH_PARENT, ('_Close', 1))
        dialog.set_title("About ObTheme")
        dialog.vbox.pack_start(label, False, True, 10)
        dialog.vbox.show_all()
        response = dialog.run()
        logging.debug(response)
        dialog.destroy()

    def display_help(self):
        help_msg = '''Most things in ObTheme are hopefully self-explanatory. Here are a few things which might not be:

The Palette
The palette displays the global set of colors as a set of swatches. Full swatches are colors used by the currently loaded theme. If you change a color in the palette, all elements in the theme which use that color will be updated to use the new one.

Double-click a swatch to open the color selection dialogue and change the color.
Swatches and color buttons can be dragged onto each other to replace colors.
Right-click the palette to bring up the context menu. "Simplify" will remove all unused colors from the palette.
Drag a theme from the theme list onto the palette to add its colors to the palette.

The Theme List
Double-left-click a theme to open it.
Double-right-click a theme to import it.
The difference between opening and importing is that importing does not set the current file name to the loaded theme.

Preview Mode
Theme->"Preview" will display a live version of the theme so you can see changes immediately.

Review the Openbox theme specification at http://openbox.org/wiki/Help:Themes for further information.
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
        dialog.set_title("ObTheme Info")
        dialog.set_default_size(600, 500)
        dialog.vbox.pack_start(textview_window, True, True, 5)
        dialog.vbox.show_all()
        response = dialog.run()
        logging.debug(response)
        dialog.destroy()

    def select(self, element, *args):
        if element in themeElements:
            typ = themeElements[element]['type']
            has_default = True if 'default' in themeElements[element] else False
            if has_default:
                text = "Default: {}\n".format(themeElements[element]['default'])
            else:
                text = ''
            if 'info' in themeElements[element]:
                text += themeElements[element]['info']
            self.info.get_buffer().set_text(text)
            self.selection = element
            value = self.theme.get_value(element.lower())
        else:
            typ = None
            self.selection = None

        for frame in self.frames.keys():
            if typ == frame:
                self.frames[frame].set_sensitive(True)
                if value is not None:
                    self.frames[frame].configure(element, value, self.theme)
            else:
                self.frames[frame].set_sensitive(False)

    def refresh(self, themerc):
        self.themerc = themerc
        if self.selection:
            self.select(self.selection)
        if self.preview_mode:
            self.save_and_reconfigure()

    def get_themerc(self):
        if not self.themerc:
            self.themerc = str(self.theme)
        return self.themerc

    def update(self, string):
        if self.selection is not None:
            self.theme.set_value(self.selection, string)
            self.unsaved = True

    def delete_event(self, widget, event, data=None):
        if self.unsaved:
            label = gtk.Label("Would you like to save the theme file?")
            dialog = gtk.Dialog(None, None, gtk.DIALOG_DESTROY_WITH_PARENT, ('Discard', 0, 'Cancel', 1, 'Save', 2))
            dialog.vbox.pack_start(label, True, True, 5)
            label.show()
            response = dialog.run()
            dialog.destroy()
            if response == 1:
                return True
            elif response == 2:
                self.save_theme()
        self.unmount_preview_dir()
        self.restore()
        return False

    def install(self, widget, arg=None, *args):
        if arg == 'install as':
            label = gtk.Label("Choose a name for this theme.")
            entry = gtk.Entry()
            dialog = gtk.Dialog(None, None, gtk.DIALOG_DESTROY_WITH_PARENT, ('Cancel', 0, 'Install', 1))
            dialog.vbox.pack_start(label, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.vbox.show_all()
            response = dialog.run()
            if response == 1:
                name = entry.get_text()
                dpath = os.getenv('HOME')+'/.themes/'+name+'/openbox-3'
                if not os.path.exists(dpath):
                    os.makedirs(dpath)
                self.file_name = dpath + '/themerc'
                self.save_theme()
            dialog.destroy()

    def destroy(self, widget, data=None):
        self.unmount_preview_dir()
        gtk.main_quit()

    def set_title(self, title=None, *args):
        if title:
            self.window.set(title)
        elif self.file_name:
            self.window.set_title(self.file_name)

    def open_from_list(self, path, button):
        self.theme.load_file(path)
        if button == 1:
            self.set_title()
            self.file_name = path

    def open_theme(self, widget, arg=None, *args):
        name = self.file_name
        dialog = gtk.FileChooserDialog('Select an Openbox theme file', None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        if name is not None:
            dialog.set_current_folder(os.path.dirname(name))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            name = dialog.get_filename()
        else:
            name = None
        dialog.destroy()
        if name is not None:
            self.theme.load_file(name)
            if arg != 'import':
                self.set_title()
                self.file_name = name
            for item in os.listdir(self.preview_themerc_dir):
                if item[-4:] == '.xbm':
                    os.remove(self.preview_themerc_dir+'/'+item)
            dpath = os.path.dirname(name)
            for item in os.listdir(dpath):
                if item[-4:] == '.xbm':
                    shutil.copyfile(dpath+'/'+item, self.preview_themerc_dir+'/'+item)

    def save_theme(self, widget=None, arg=None, *args):
        name = self.file_name
        if name is None or arg == 'save as':
            button = gtk.STOCK_SAVE_AS if arg == 'save as' else gtk.STOCK_SAVE
            dialog = gtk.FileChooserDialog('Select an Openbox theme file', None,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    button, gtk.RESPONSE_OK))
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
            result = self.theme.save_file(name)
            if result is True:
                self.set_title()
                self.unsaved = False
                dpath = os.path.dirname(name)
                if os.path.exists(self.preview_themerc_dir):
                    if not os.path.exists(dpath):
                        os.makedirs(dpath)
                    for item in os.listdir(self.preview_themerc_dir):
                        if item[-4:] == '.xbm':
                            shutil.copyfile(self.preview_themerc_dir+'/'+item, dpath+'/'+item)
            else:
                dialog_msg("Error",
                           "Could not save file!\n\n{}".format(result),
                           gtk.MESSAGE_WARNING)

    def get_theme(self, theme):
        rc_xml = read_file(self.openbox_config_path)
        m = re.search(r'<theme>.*?<name>(.*?)<\/name>', rc_xml, re.S)
        if m:
            return m.group(1)
        else:
            return None

    def set_theme(self, theme):
        rc_xml = read_file(self.openbox_config_path)
        m = re.search(r'(^.*?<theme>.*?<name>)(.*?)(<\/name>.*$)',
                      rc_xml, re.S)
        if m:
            prev_theme = m.group(2)
            if theme == prev_theme:
                return True
            if prev_theme != 'obtheme':
                self.previous_theme = prev_theme
            rc_xml = m.group(1) + theme + m.group(3)
            if write_file(self.openbox_config_path, rc_xml):
                logging.debug("Changed theme in rc.xml: {} -> {}"
                             .format(prev_theme, theme))
                self.reconfigure()
                return True
        logging.error("Unable to parse theme element of {}\n".format(rc_xml))
        return False

    def save_preview(self):
        if os.path.exists(self.preview_themerc_dir):
            write_file(self.preview_themerc_dir+'/themerc', self.get_themerc())
        else:
            logging.warning("Could not find path {}"
                            .format(self.preview_themerc_dir))

    def save_and_reconfigure(self):
        self.save_preview()
        self.reconfigure()

    def reconfigure(self):
        if self.preview_mode:
            try:
                subprocess.call(['openbox', '--reconfigure'])
            except OSError as e:
                self.restore()
                logging.error("Unable to reconfigure openbox: {}"
                              .format(e))
            except Exception as e1:
                logging.error("Unexpected error: {}".format(e1))
                raise

    def toggle_preview_mode(self, widget):
        if widget.get_active():
            self.preview()
        else:
            self.restore()
        self.preview_mode = widget.get_active()

    def preview(self, *args):
        if self.preview_dir_is_mounted():
            self.save_preview()
            self.set_theme('obtheme')
            self.preview_mode = True
        else:
            self.restore()

    def restore(self, *args):
        if self.previous_theme is not None:
            self.set_theme(self.previous_theme)
            self.previous_theme = None
        self.preview_mode = False
        self.preview_mode_checkbox.set_active(False)

    def unmount_preview_dir(self):
        if self.preview_dir_is_mounted():
            subprocess.call(['fusermount', '-u', self.preview_themerc_dir])

    def preview_dir_is_mounted(self):
        mtab = read_file('/etc/mtab')
        return mtab.find(self.preview_themerc_dir) > -1

    def main(self):
        gtk.main()

    def open_xbm_editor(self, *args):
        # os.system('./xbm-editor &')
        editor = XBMWindow()
        editor.callback = self.reconfigure


if __name__ == "__main__":
    DEBUG = os.environ.get('OB_DEBUG', False)
    obt = ObTheme()
    fusedir = obt.preview_themerc_dir
    src = obt.src_dir
    if not obt.preview_dir_is_mounted():
        if os.fork() == 0:
            if not os.path.exists(fusedir):
                os.makedirs(fusedir)
            clear_dir(fusedir)
            if not os.path.exists(src):
                os.makedirs(src)
            clear_dir(src)
            fuse_obj.main(fusedir, src)
        else:
            obt.main()
    else:
        obt.main()
#  xbm = XBMWindow()
#  xbm.main()
