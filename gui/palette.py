# -*- coding: utf-8 -*-

from __future__ import absolute_import
import gtk
import math
from utils.color_utils import (str_to_color, color_to_str)


class Palette(gtk.Frame):

    def __init__(self, theme, *args):
        gtk.Frame.__init__(self, *args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("palette")

        self.color_set = set()
        self.used_set = set()
        self.color_list = []
        self.swatch_map = {}
        self.selected = None
        self.colorseldlg = None
        self.theme = theme
        self.swatch_dim = 25

        self.area = gtk.DrawingArea()
        self.area.set_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)
        self.area.connect("expose_event", self.expose)
        self.area.connect("button_press_event", self.button_press)
        self.area.drag_dest_set(0, [], 0)
        self.area.drag_source_set(gtk.gdk.BUTTON1_MASK, [], 0)
        self.area.connect("drag_motion", self.drag_motion)
        self.area.connect("drag_drop", self.drag_drop)
        self.area.connect("drag_begin", self.drag_begin)
        self.area.connect("drag_data_get", self.drag_data_get)

        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.sw.add_with_viewport(self.area)
        self.area.show()

        self.menu = gtk.Menu()
        self.menu.set_title('Palette')
        menu_simplify = gtk.ImageMenuItem('_Simplify')
        self.menu.append(menu_simplify)
        menu_simplify.connect('activate', self.simplify)
        menu_simplify.show()

        self.add(self.sw)
        self.show_all()

        self.update_dimensions()

    def simplify(self, *args):
        self.color_set = set()
        self.theme.update_palette()

    def update(self):
        self.color_list = list(self.color_set)
        self.color_list.sort()
        self.draw_swatches()

    def set_theme_palette(self, palette):
        self.used_set = palette
        self.color_set.update(palette)
        self.update()

    def import_palette(self, palette):
        self.color_set.update(palette)
        self.update()

    def add_color(self, color, used=False):
        self.color_set.add(color)
        if used:
            self.used_set.add(color)
        self.update()

    def remove_color(self, color):
        if color in self.color_set:
            self.color_set.remove(color)
            self.update()

    def replace_color(self, old, new):
        if new not in self.color_set:
            self.color_set.add(new)
        if old in self.color_set:
            self.color_set.remove(old)
        self.theme.replace_color(old, new)
        self.update()

    def get_width(self):
        x1, y1, w1, h1 = self.sw.get_allocation()
        x2, y2, w2, h2 = self.sw.get_vscrollbar().get_allocation()
        w = w1 - w2
        if w < self.swatch_dim:
            return self.swatch_dim
        return w

    def update_dimensions(self):
        self.width = self.get_width()
        columns = self.width/self.swatch_dim
        rows = int(math.ceil(float(len(self.color_set))/columns))
        self.height = rows * self.swatch_dim
        w = self.get_width()/self.swatch_dim
        self.area.set_size_request(w, self.height)
        return

    def map_swatch(self, x, y):
        for color in self.swatch_map.keys():
            if x >= self.swatch_map[color]['x1'] \
               and x <= self.swatch_map[color]['x2'] \
               and y >= self.swatch_map[color]['y1'] \
               and y <= self.swatch_map[color]['y2']:
                return color
        return None

    def get_color(self, default='#000000'):
        if self.colorseldlg is None:
            self.colorseldlg = gtk.ColorSelectionDialog({}.format(
                "choose a replacement color"))
        colorsel = self.colorseldlg.colorsel
        colorsel.set_current_color(str_to_color(default))
        response = self.colorseldlg.run()
        if response--gtk.RESPONSE_OK:
            new_color = color_to_str(colorsel.get_current_color())
        else:
            new_color = None
        self.colorseldlg.hide()
        return new_color

    def button_press(self, area, event):
        if event.button == 1:
            self.selected = self.map_swatch(event.x, event.y)
            if event.type == gtk.gdk._2BUTTON_PRESS:
                if self.selected:
                    new_color = self.get_color(self.selected)
                    if new_color is not None and \
                       new_color is not self.selected:
                        self.replace_color(self.selected, new_color)
                else:
                    self.add_color(self.get_color())
        elif event.button == 3:
            self.menu.popup(None, None, None, event.button, event.time)

    def get_value(self):
        return self.selected

    def drag_color(self, widget, context, selection, info, time):
        # context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drag_motion(self, widget, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drag_drop(self, widget, context, x, y, time):
        source_widget = context.get_source_widget()
        new_color = None
        if source_widget.__class__.__name__ == 'ColorButton':
            new_color = source_widget.get_value()
        else:
            source_widget = source_widget.get_parent()
            if source_widget.__class__.__name__ == 'ThemeFileSelector':
                path = source_widget.get_selected()
                self.theme.import_palette(path)
                return
            else:
                source_widget = source_widget.get_parent().get_parent()
            if source_widget.__class__.__name__ == 'Palette':
                new_color = source_widget.get_value()
        old_color = self.map_swatch(x, y)
        if new_color is not None:
            if old_color is not None and old_color != new_color:
                self.replace_color(old_color, new_color)
            elif old_color is None:
                self.add_color(new_color)
        context.finish(True, False, time)
        return True

    def drag_begin(self, widget, context, *args):
        # context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drag_data_get(self, widget, context, x, y, time):
        return True

    def expose(self, area, event):
        self.update_dimensions()
        self.draw_swatches()
        return True

    def draw_swatches(self):
        i = 0
        w = self.swatch_dim
        divisor = self.width/w
        self.swatch_map = {}
        gc = self.area.window.new_gc()
        gc.set_rgb_fg_color(str_to_color('#eeeeee'))
        self.area.window.draw_rectangle(gc, True, *self.area.get_allocation())
        for color in self.color_list:
            self.swatch_map[color] = {}
            y, x = divmod(i, divisor)
            self.draw_swatch(x*w, y*w, w, color, gc)
            i += 1
        return

    def draw_swatch(self, x, y, w, color, gc=None):
        if gc is None:
            gc = self.area.window.new_gc()
        gc.set_rgb_fg_color(str_to_color('#000000'))
        self.area.window.draw_rectangle(gc, False, x, y, w, w)
        x1 = x+1
        y1 = y+1
        w1 = w-2
        gc.set_rgb_fg_color(str_to_color(color))
        self.area.window.draw_rectangle(gc, True, x1, y1, w1, w1)
        if color not in self.used_set:
            gc.set_rgb_fg_color(str_to_color('#eeeeee'))
            self.area.window.draw_polygon(gc, True,
                                          [(x1, y1),
                                           (x1+w1/2, y1),
                                           (x1, y1+w1/2)])
            gc.set_rgb_fg_color(str_to_color('#000000'))
            self.area.window.draw_line(gc, x1+w1/2, y1, x1, y1+w1/2)
        self.swatch_map[color]['x1'] = x1
        self.swatch_map[color]['x2'] = x1+w1
        self.swatch_map[color]['y1'] = y1
        self.swatch_map[color]['y2'] = y1+w1
        # if color == self.selected:
        #  pass
        return
