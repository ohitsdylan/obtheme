# -*- coding: utf-8 -*-

from utils.color_utils import (color_to_str, str_to_color)
import gtk


class ColorButton(gtk.ColorButton):

    def __init__(self, *args):
        gtk.ColorButton.__init__(self, *args)
        self.drag_dest_set(0, [], 0)
        self.connect("drag_motion", self.drag_motion)
        self.connect("drag_drop", self.drag_drop)

    def drag_motion(self, widget, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drag_drop(self, widget, context, x, y, time):
        source_widget = context.get_source_widget()
        if source_widget.__class__.__name__ == 'ColorButton':
            color = source_widget.get_value()
            self.set_value(color)
        else:
            source_widget = source_widget.get_parent().get_parent().get_parent()
            if source_widget.__class__.__name__ == 'Palette':
                color = source_widget.get_value()
                if color:
                    self.set_value(color)
        context.finish(True, False, time)
        self.emit('color-set')
        return True

    def get_value(self):
        return color_to_str(self.get_color())

    def set_value(self, string):
        return self.set_color(str_to_color(string))
