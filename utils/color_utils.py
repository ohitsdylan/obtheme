# -*- coding: utf-8 -*-

import gtk


def color_to_str(color):
    red = round((color.red / 65535.0) * 255)
    green = round((color.green / 65535.0) * 255)
    blue = round((color.blue / 65535.0) * 255)
    return "#%02X%02X%02X" % (red, green, blue)


def str_to_color(string):
    return gtk.gdk.color_parse(string)
