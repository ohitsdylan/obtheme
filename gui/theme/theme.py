# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re
from types import StringType
from openbox.theme_elements import themeElements
from gui.palette import Palette
from utils.general_utils import (write_file, format_ob_color_str)


class Theme():

    def __init__(self, *args):
        self.elements = {}
        self.palette = Palette(self)
        self.themerc = ''
        self.callback = None

    def get_theme(self, name):
        theme = {}
        f = open(name, 'r')
        for line in f:
            m = re.search(r'^\s*([A-Za-z\.\*]+)\s*:\s*(.+?)\s*$', line)
            if m:
                name = m.group(1)
                value = m.group(2)
                if name.find('*') > -1:
                    glob_pattern = name
                    glob_was_successful = False
                    i = glob_pattern.find('.bg.')
                    if i > -1:
                        glob_pattern = name[0:i+3]
                        suffix = name[i+3:]
                    else:
                        suffix = ''
                    glob_pattern = glob_pattern.replace('.', '\.')
                    glob_pattern = glob_pattern.replace('*', '.*')
                    for element in themeElements.keys():
                        m = re.search("^(%s)$" % glob_pattern, element)
                        if m:
                            match = m.group(1)
                            theme = self.parse_element(match + suffix, value, theme)
                            glob_was_successful = True
                    if not glob_was_successful:
                        print "Warning: failed to match globbing pattern: " + name
                else:
                    theme = self.parse_element(name, value, theme)
        f.close()
        return theme

    def parse_element(self, name, value, theme):
        recognized = True if name in themeElements else False
        if recognized and themeElements[name]['type'] == 'color':
            value = format_ob_color_str(value)
        if recognized and themeElements[name]['type'] == 'texture' and name in theme:
            theme[name] += "\n" + value
            return theme
        elif recognized:
            theme[name] = value
            return theme
        i = name.find('.bg.')
        if i > -1:
            texture = name[0:i+3]
            texture_attr = name[i+3:]
            if texture in themeElements and themeElements[texture]['type'] == 'texture':
                if texture_attr.lower().find('color') > -1:
                    value = format_ob_color_str(value)
                if texture in theme:
                    theme[texture] += "\n%s: %s" % (texture_attr, value)
                else:
                    theme[texture] = "%s: %s" % (texture_attr, value)
                return theme
        print "Warning: ignoring unrecognized theme element \"%s\"" % name
        return theme

    def load_file(self, name):
        self.elements = self.get_theme(name)
        self.update_palette()
        self.report_change('loaded '+name)

    def __str__(self, *args):
        text = "# openbox themerc edited with obtheme\n"
        if len(self.elements) > 0:
            elements = self.elements.keys()
            elements.sort()
            for name in elements:
                if self.is_default(name):
                    continue
                value = self.elements[name]
                if isinstance(value, StringType) and value.find("\n") > -1:
                    for line in value.split("\n"):
                        i = line.find(':')
                        if i > -1:
                            attr = line[:i]
                            attr_val = line[i+2:]
                            text += "%s%s: %s\n" % (name, attr, attr_val)
                        else:
                            text += "%s: %s\n" % (name, line)
                else:
                    text += "%s: %s\n" % (name, value)
        return text

    def save_file(self, file_name):
        text = self.__str__()
        return write_file(file_name, text)

    def is_default(self, element):
        if element not in self.elements:
            return True
        value = self.elements[element]
        if value == '':
            return True
        if element in themeElements and 'default' in themeElements[element]:
            default = themeElements[element]['default']
            if default.lower() == 'none':
                return False
            elif default.find('.') > -1:
                return (self.get_value(default) == value)
        return False

    def get_value(self, element):
        if element in self.elements:
            return self.elements[element]
        elif element in themeElements and 'default' in themeElements[element]:
            default = themeElements[element]['default']
            if default.lower() == 'none':
                return ''
            elif default.find('.') > -1:
                return self.get_value(default)
            else:
                return default
        else:
            return ''

    def extract_colors(self, key, value):
        colors = []
        if key[-6:].lower() == '.color':
            colors.append(value)
        elif isinstance(value, StringType) and value.find("\n") > -1:
            for line in value.split("\n"):
                m = re.search(r'\s*^\S*\.color(?:To)?\s*:\s*(.*?)\s*$', line)
                if m:
                    colors.append(m.group(1))
        return colors

    def set_value(self, key, value):
        # if key not in self.elements:
        #     print "new key:", key
        self.elements[key] = value
        for color in self.extract_colors(key, value):
            self.palette.add_color(color, True)
        self.report_change("set %s -> %s" % (key, value))

    def get_palette(self, theme):
        palette = set()
        for key, value in theme.iteritems():
            for color in self.extract_colors(key, value):
                palette.add(color)
        return palette

    def update_palette(self):
        self.palette.set_theme_palette(self.get_palette(self.elements))
        self.report_change("updated palette")

    def import_palette(self, path):
        theme = self.get_theme(path)
        palette = self.get_palette(theme)
        self.palette.import_palette(palette)

    def replace_color(self, old, new):
        replaced = False
        for key, value in self.elements.iteritems():
            if (key[-6:].lower() == '.color' and value == old) \
                    or (key in themeElements and themeElements[key]['type'] == 'texture' and value.find(old) > -1):
                self.elements[key] = value.replace(old, new)
                if not replaced:
                    replaced = True
        if replaced:
            self.palette.add_color(new, True)
            self.report_change("replaced %s with %s" % (old, new))

    def report_change(self, what=None):
        # print what
        themerc = self.__str__()
        if themerc != self.themerc:
            self.themerc = themerc
            if self.callback:
                self.callback(themerc)
