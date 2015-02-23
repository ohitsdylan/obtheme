# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk
import re
import logging
from gtk import FILL, EXPAND
from utils.general_utils import multiply_color
from openbox.theme_elements import themeElements
from gui.color_button import ColorButton


class TextureFrame(gtk.Frame):

    def update_value(self, *args):
        attributes = {}
        texture = self.texture.get_active_text()
        if texture == 'ParentRelative':
            string = texture
        elif texture == 'Solid':
            string = texture
            attributes['color'] = self.color.get_value()
        elif texture == 'Gradient':
            gradient = self.gradient.get_active_text()
            string = "%s %s" % (texture, gradient)
            color = self.color.get_value()
            colorTo = self.colorTo.get_value()
            attributes['color'] = color
            attributes['colorTo'] = colorTo

            if gradient == 'SplitVertical':
                colorSplitTo = self.colorSplitTo.get_value()
                colorToSplitTo = self.colorToSplitTo.get_value()
                if self.colorSplitTo_tb.get_active() and colorSplitTo != multiply_color(color, 5/4.0):
                    attributes['color.splitTo'] = colorSplitTo
                if self.colorToSplitTo_tb.get_active() and colorToSplitTo != multiply_color(colorTo, 17/16.0):
                    attributes['colorTo.splitTo'] = colorToSplitTo
        else:
            return

        if self.interlaced.get_active():
            string += ' ' + 'Interlaced'
            attributes['interlace.color'] = self.interlacedColor.get_value()

        border = self.border.get_active_text()
        if border == 'None':
            string += ' ' + 'Flat'
        elif border == 'Flat':
            string += ' ' + 'Flat Border'
            attributes['border.color'] = self.borderColor.get_value()
        elif border == 'Raised' or border == 'Sunken':
            string += ' ' + border
            attributes['border.color'] = self.borderColor.get_value()
            if self.highlight.get_value() != 128:
                attributes['highlight'] = int(self.highlight.get_value())
            if self.shadow.get_value() != 64:
                attributes['shadow'] = int(self.shadow.get_value())
            if self.bevelButton2.get_active():
                string += ' ' + 'Bevel2'

        for name, value in attributes.iteritems():
            string += "\n.%s: %s" % (name, value)

        if self.callback and self.sensitive:
            self.callback(string)

    def configure(self, name, string, theme):
        self.sensitive = False
        attributes = {}
        if 'parentrelative' in themeElements[name]:
            self.set_parentrelative(themeElements[name]['parentrelative'])
        else:
            self.set_parentrelative(True)
        for line in string.split("\n"):
            m = re.search(r'^\.([^:]+?)\s*:\s*(\S+)\s*$', line)
            if m:
                attribute = m.group(1).lower()
                value = m.group(2)
                if attribute == 'color':
                    self.color.set_value(value)
                elif attribute == 'colorto':
                    self.colorTo.set_value(value)
                elif attribute == 'color.splitto':
                    self.colorSplitTo.set_value(value)
                elif attribute == 'colorto.splitto':
                    self.colorToSplitTo.set_value(value)
                elif attribute == 'interlace.color':
                    self.interlacedColor.set_value(value)
                elif attribute == 'border.color':
                    self.borderColor.set_value(value)
                elif attribute == 'highlight':
                    self.highlight.set_value(float(value))
                elif attribute == 'shadow':
                    self.shadow.set_value(float(value))
                attributes[attribute] = True
            else:
                for word in re.split('\s+', line):
                    word = word.lower()
                    if word == 'solid' \
                            or word == 'gradient' \
                            or word == 'parentrelative':
                        model = self.texture.get_model()
                        for i in range(len(model)):
                            if model[i][0].lower() == word:
                                self.texture.set_active(i)
                                break
                    elif word == 'diagonal' \
                            or word == 'crossdiagonal' \
                            or word == 'pyramid' \
                            or word == 'horizontal' \
                            or word == 'mirrorhorizontal' \
                            or word == 'vertical' \
                            or word == 'splitvertical':
                        model = self.gradient.get_model()
                        for i in range(len(model)):
                            if model[i][0].lower() == word:
                                self.gradient.set_active(i)
                                break
                    elif word == 'flat' \
                            or word == 'raised' \
                            or word == 'sunken':
                        model = self.border.get_model()
                        for i in range(len(model)):
                            if model[i][0].lower() == word:
                                self.border.set_active(i)
                                break
                    elif word == 'interlaced':
                        self.interlaced.set_active(True)
                    elif word == 'bevel2':
                        self.bevelButton2.set_active(True)

        if self.border.get_active_text() == 'Flat':
            if 'border.color' not in attributes:
                model = self.border.get_model()
                for i in range(len(model)):
                    if model[i][0] == 'None':
                        self.border.set_active(i)
                        break
        if 'color.splitto' not in attributes:
            self.colorSplitTo.set_value(multiply_color(self.color.get_value(), 5/4.0))
        if 'colorTo.splitto' not in attributes:
            self.colorToSplitTo.set_value(multiply_color(self.colorTo.get_value(), 17/16.0))
        self.sensitive = True

    def update_texture(self, *args):
        texture = self.texture.get_active_text()
        if texture == 'Solid':
            self.gradient.set_sensitive(False)
            self.color.set_sensitive(True)
            self.colorTo.set_sensitive(False)
            self.colorSplitTo.set_sensitive(False)
            self.colorToSplitTo.set_sensitive(False)
        elif texture == 'Gradient':
            self.gradient.set_sensitive(True)
            self.color.set_sensitive(True)
            self.colorTo.set_sensitive(True)
            self.update_gradient()
        elif texture == 'ParentRelative':
            self.gradient.set_sensitive(False)
            self.color.set_sensitive(False)
            self.colorTo.set_sensitive(False)
            self.colorSplitTo.set_sensitive(False)
            self.colorToSplitTo.set_sensitive(False)
        self.update_value()

    def update_gradient(self, *args):
        gradient = self.gradient.get_active_text()
        if gradient == 'SplitVertical':  # gradient == 'MirrorHorizontal'
            self.colorSplitTo.set_sensitive(self.colorSplitTo_tb.get_active())
            self.colorToSplitTo.set_sensitive(self.colorToSplitTo_tb.get_active())
        else:
            self.colorSplitTo.set_sensitive(False)
            self.colorToSplitTo.set_sensitive(False)
        self.update_value()

    def update_interlaced(self, *args):
        if self.interlaced.get_active():
            self.interlacedColor.set_sensitive(True)
        else:
            self.interlacedColor.set_sensitive(False)
        self.update_value()

    def set_parentrelative(self, value):
        model = self.texture.get_model()
        string = 'ParentRelative'
        if value and model[0][0] != string:
            self.texture.prepend_text(string)
        elif value is not True and model[0][0] == string:
            self.texture.set_active(1)
            self.texture.remove_text(0)

    def update_border(self, *args):
        border = self.border.get_active_text()
        if border == 'None':
            self.borderColor.set_sensitive(False)
            self.highlightButton.set_sensitive(False)
            self.shadowButton.set_sensitive(False)
            self.bevelButton1.set_sensitive(False)
            self.bevelButton2.set_sensitive(False)
        elif border == 'Flat':
            self.borderColor.set_sensitive(True)
            self.highlightButton.set_sensitive(False)
            self.shadowButton.set_sensitive(False)
            self.bevelButton1.set_sensitive(False)
            self.bevelButton2.set_sensitive(False)
            self.update_gradient()
        elif border == 'Raised' or border == 'Sunken':
            self.borderColor.set_sensitive(True)
            self.highlightButton.set_sensitive(True)
            self.shadowButton.set_sensitive(True)
            self.bevelButton1.set_sensitive(True)
            self.bevelButton2.set_sensitive(True)
        self.update_value()

    def reset(self, *args):
        #     model = self.texture.get_model()
        #     for i in range(len(model)):
        #       if model[i][0].lower() == 'solid':
        #         self.texture.set_active(i)
        #         break
        #     model = self.gradient.get_model()
        #     for i in range(len(model)):
        #       if model[i][0].lower() == 'vertical':
        #         self.gradient.set_active(i)
        #         break
        #     model = self.border.get_model()
        #     for i in range(len(model)):
        #       if model[i][0].lower() == 'raised':
        #         self.border.set_active(i)
        #         break
        #     self.color.set_value('#000000')
        #     self.borderColor.set_value('#000000')
        self.colorSplitTo_tb.set_active(False)
        self.colorToSplitTo_tb.set_active(False)
        self.interlaced.set_active(False)
        self.highlight.set_value(128)
        self.shadow.set_value(64)
        self.bevelButton1.set_active(True)
        self.update_value()

    def __init__(self, **args):
        gtk.Frame.__init__(self, **args)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.set_label_align(1, 0.5)
        self.set_label("texture")
        self.callback = None

        self.texture = gtk.combo_box_new_text()
        self.texture.append_text('ParentRelative')
        self.texture.append_text('Solid')
        self.texture.append_text('Gradient')
        self.texture.set_active(1)
        self.texture.connect('changed', self.update_texture)
        self.texture.show()
        textureLabel = gtk.Label('texture')
        textureLabel.set_alignment(0, 0.5)

        self.gradient = gtk.combo_box_new_text()
        self.gradient.append_text('Diagonal')
        self.gradient.append_text('CrossDiagonal')
        self.gradient.append_text('Pyramid')
        self.gradient.append_text('Horizontal')
        self.gradient.append_text('MirrorHorizontal')
        self.gradient.append_text('Vertical')
        self.gradient.append_text('SplitVertical')
        self.gradient.set_active(5)
        self.gradient.connect('changed', self.update_gradient)
        self.gradient.show()
        gradientLabel = gtk.Label('gradient')
        gradientLabel.set_alignment(0, 0.5)

        self.color = ColorButton()
        self.color.connect("color-set", self.update_value)
        colorLabel = gtk.Label('color')
        colorLabel.set_alignment(0, 0.5)

        self.colorTo = ColorButton()
        self.colorTo.connect("color-set", self.update_value)
        colorToLabel = gtk.Label('colorTo')
        colorToLabel.set_alignment(0, 0.5)

        self.colorSplitTo = ColorButton()
        self.colorSplitTo.connect("color-set", self.update_value)
        self.colorSplitTo_tb = gtk.CheckButton("color.splitTo")
        self.colorSplitTo_tb.connect("toggled", self.update_gradient)
        self.colorSplitTo_tb.set_active(False)
        self.colorSplitTo_tb.set_alignment(0, 0.5)

        self.colorToSplitTo = ColorButton()
        self.colorToSplitTo.connect("color-set", self.update_value)
        self.colorToSplitTo_tb = gtk.CheckButton("colorTo.splitTo")
        self.colorToSplitTo_tb.connect("toggled", self.update_gradient)
        self.colorToSplitTo_tb.set_active(False)
        self.colorToSplitTo_tb.set_alignment(0, 0.5)

        self.interlaced = gtk.CheckButton("interlaced")
        self.interlaced.connect("toggled", self.update_interlaced)
        self.interlacedColor = ColorButton()
        self.interlacedColor.connect("color-set", self.update_value)
        self.interlacedColor.set_sensitive(False)

        colortable = gtk.Table(rows=2, columns=2, homogeneous=False)
        i = 0
        colortable.attach(textureLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.texture, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.attach(gradientLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.gradient, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.attach(colorLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.color, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.attach(colorToLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.colorTo, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.attach(self.colorSplitTo_tb, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.colorSplitTo, 1, 2, i, i+1, FILL, EXPAND, 0, 0)

        i += 1
        colortable.attach(self.colorToSplitTo_tb, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.colorToSplitTo, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.attach(self.interlaced, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        colortable.attach(self.interlacedColor, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        colortable.show_all()

        self.border = gtk.combo_box_new_text()
        self.border.append_text('None')
        self.border.append_text('Flat')
        self.border.append_text('Raised')
        self.border.append_text('Sunken')
        self.border.set_active(2)
        self.border.connect('changed', self.update_border)
        borderLabel = gtk.Label('border')
        borderLabel.set_alignment(0, 0.5)

        self.bevelButton1 = gtk.RadioButton(None, "Bevel1")
        self.bevelButton2 = gtk.RadioButton(self.bevelButton1, "Bevel2")
        self.bevelButton1.connect("toggled", self.update_interlaced)

        self.borderColor = ColorButton()
        self.borderColor.connect("color-set", self.update_value)
        borderColorLabel = gtk.Label('border color')
        borderColorLabel.set_alignment(0, 0.5)

        self.highlight = gtk.Adjustment(128, 0, 65535, 1, 256, 0)
        self.shadow = gtk.Adjustment(64, 0, 256, 1, 16, 0)
        self.highlight.connect("value_changed", self.update_value)
        self.shadow.connect("value_changed", self.update_value)

        self.highlightButton = gtk.SpinButton(self.highlight, 0, 0)
        self.highlightButton.set_numeric(True)
        self.highlightButton.set_digits(0)
        highlightLabel = gtk.Label('highlight')
        highlightLabel.set_alignment(0, 0.5)

        self.shadowButton = gtk.SpinButton(self.shadow, 0, 0)
        self.shadowButton.set_numeric(True)
        self.shadowButton.set_digits(0)
        shadowLabel = gtk.Label('shadow')
        shadowLabel.set_alignment(0, 0.5)

        reset = gtk.Button(label="reset")
        reset.set_alignment(0.5, 0.5)
        reset.connect("clicked", self.reset)

        bordertable = gtk.Table(rows=2, columns=2, homogeneous=False)
        i = 0
        bordertable.attach(borderLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        bordertable.attach(self.border, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        bordertable.attach(borderColorLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        bordertable.attach(self.borderColor, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        bordertable.attach(highlightLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        bordertable.attach(self.highlightButton, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        bordertable.attach(shadowLabel, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        bordertable.attach(self.shadowButton, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        bordertable.attach(self.bevelButton1, 0, 1, i, i+1, FILL, EXPAND, 5, 0)
        bordertable.attach(self.bevelButton2, 1, 2, i, i+1, FILL, EXPAND, 0, 0)
        i += 1
        bordertable.attach(reset, 0, 2, i, i+1, FILL, FILL, 5, 0)
        bordertable.show_all()

        hbox = gtk.HBox(False, 5)
        hbox.pack_start(colortable, False, False, 5)
        hbox.pack_start(bordertable, False, False, 5)
        hbox.show()
        self.add(hbox)
        self.update_texture()
