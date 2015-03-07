# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import logging
logging.basicConfig(level=logging.DEBUG)

# Warning: on my Lubuntu Openbox configuration this file it's called
# 'lubuntu-rc.xml'. This might happen on other configurations too, I guess.
OPENBOX_CONFIG_FILE = '/openbox/lubuntu-rc.xml'


def get_config_file(config_dir):
    fullpath = "{}{}".format(config_dir, OPENBOX_CONFIG_FILE)
    if not os.path.exists(fullpath):
        msg = u"Could not locate Openbox config file in '{}'"\
            .format(fullpath)
        logging.error(msg)
        return None
    return fullpath

themeElements = {
    'border.color': {
        'type': 'color',
        'default': '#000000',
        'info': "This property is obsolete and only present for backwards "
        "compatibility.\n See also: window.active.border.color, "
        "window.inactive.border.color, menu.border.color\n"
    },
    'border.width': {
        'type': 'integer',
        'default': '1',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the border drawn around window frames.\nSee also: window.active.border.color, window.inactive.border.color\n"
    },
    'menu.border.color': {
        'type': 'color',
        'default': 'window.active.border.color',
        'info': "Specifies the border color for menus.\nSee also: menu.border.width\n"
    },
    'menu.border.width': {
        'type': 'integer',
        'default': 'border.width',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the border drawn around menus.\nSee also: menu.border.color\n"
    },
    'menu.items.active.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for the selected menu entry (whether or not it is disabled). When it is parentrelative, then it uses the menu.items.bg which is underneath it.\nSee also: menu.items.bg\n"
    },
    'menu.items.active.disabled.text.color': {
        'type': 'color',
        'default': 'menu.items.disabled.text.color',
        'info': "Specifies the text color for disabled menu entries when they are selected.\n"
    },
    'menu.items.active.text.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the text color for normal menu entries when they are selected.\n"
    },
    'menu.items.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for menus.\nSee also: menu.items.active.bg\n"
    },
    'menu.items.disabled.text.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the text color for disabled menu entries.\n"
    },
    'menu.items.font': {
        'type': 'text shadow string',
        'default': 'shadow=n',
        'info': "Specifies the shadow for all menu entries.\n"
    },
    'menu.items.text.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the text color for normal menu entries.\n"
    },
    'menu.overlap': {
        'type': 'integer',
        'default': '0',
        'lbound': -100,
        'ubound': 100,
        'info': "This property is obsolete and only present for backwards compatibility.\nSee also: menu.overlap.x, menu.overlap.y\n"
    },
    'menu.overlap.x': {
        'type': 'integer',
        'default': 'menu.overlap',
        'lbound': -100,
        'ubound': 100,
        'info': "Specifies how sub menus should overlap their parents. A positive value moves the submenu over top of their parent by that amount. A negative value moves the submenu away from their parent by that amount. (As of version 3.4.7)\nSee also: menu.overlap.y\n"
    },
    'menu.overlap.y': {
        'type': 'integer',
        'default': 'menu.overlap',
        'lbound': -100,
        'ubound': 100,
        'info': "Specifies how sub menus should be positioned relative to their parents. A positive value moves the submenu vertically down by that amount, a negative value moves it up by that amount. (As of version 3.4.7)\nSee also: menu.overlap.x\n"
    },
    'menu.separator.color': {
        'type': 'color',
        'default': 'menu.items.text.color',
        'info': "The color of menu line separators. (As of version 3.4.7)\nSee also: menu.items.text.color\n"
    },
    'menu.separator.padding.height': {
        'type': 'integer',
        'default': '3',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the space on the top and bottom of menu line separators. (As of version 3.4.7)\nSee also: menu.separator.padding.width\n"
    },
    'menu.separator.padding.width': {
        'type': 'integer',
        'default': '6',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the space on the left and right side of menu line separators. (As of version 3.4.7)\nSee also: menu.separator.padding.height\n"
    },
    'menu.separator.width': {
        'type': 'integer',
        'default': '1',
        'lbound': 1,
        'ubound': 100,
        'info': "Specifies the size of menu line separators. (As of version 3.4.7)\n"
    },
    'menu.title.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for menu headers. When it is parentrelative, then it uses the menu.items.bg which is underneath it.\nSee also: menu.items.bg\n"
    },
    'menu.title.text.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the text color for menu headers.\n"
    },
    'menu.title.text.font': {
        'type': 'text shadow string',
        'default': 'shadow=n',
        'info': "Specifies the shadow for all menu headers.\n"
    },
    'menu.title.text.justify': {
        'type': 'justification',
        'default': 'Left',
        'info': "Specifies how text is aligned in all menu headers.\n"
    },
    'osd.bg': {
        'type': 'texture',
        'default': 'window.active.title.bg',
        'parentrelative': False,
        'info': "Specifies the background for on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\n"
    },
    'osd.border.color': {
        'type': 'color',
        'default': 'window.active.border.color',
        'info': "Specifies the border color for on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\nSee also: osd.border.width\n"
    },
    'osd.border.width': {
        'type': 'integer',
        'default': 'border.width',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the border drawn on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\nSee also: osd.border.color\n"
    },
    'osd.hilight.bg': {
        'type': 'texture',
        'default': 'window.active.label.bg, if it is not parentrelative. Otherwise, window.active.title.bg',
        'parentrelative': False,
        'info': "Specifies the texture for the selected desktop in the desktop cycling (pager) dialog.\n"
    },
    'osd.label.bg': {
        'type': 'texture',
        'default': 'window.active.label.bg',
        'parentrelative': 1,
        'info': "Specifies the background for text in on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\n"
    },
    'osd.label.text.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the text color for on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\n"
    },
    'osd.label.text.font': {
        'type': 'text shadow string',
        'default': 'shadow=n',
        'info': "Specifies the text shadow for on-screen-dialogs, such as the focus cycling (Alt-Tab) dialog.\n"
    },
    'osd.unhilight.bg': {
        'type': 'texture',
        'default': 'window.inactive.label.bg, if it is not parentrelative. Otherwise, window.inactive.title.bg',
        'parentrelative': False,
        'info': "Specifies the texture for unselected desktops in the desktop cycling (pager) dialog.\n"
    },
    'padding.height': {
        'type': 'integer',
        'default': 'padding.width',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the padding size, used for spacing out elements in the window decorations. This can be used to give a theme a more compact or a more relaxed feel. This specifies padding in only the vertical direction.\nSee also: padding.width\n"
    },
    'padding.width': {
        'type': 'integer',
        'default': '3',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the padding size, used for spacing out elements in the window decorations. This can be used to give a theme a more compact or a more relaxed feel. This specifies padding in the horizontal direction (and vertical direction if padding.height is not explicitly set).\nSee also: padding.height\n"
    },
    'window.active.border.color': {
        'type': 'color',
        'default': 'border.color',
        'info': "Specifies the border color for the focused window.\nSee also: border.width, window.inactive.border.color\n"
    },
    'window.active.button.disabled.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when they are disabled for the window. This element is for the focused window. When it is parentrelative, then it uses the window.active.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.disabled.bg\n"
    },
    'window.active.button.disabled.image.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the color of the images in titlebar buttons when they are disabled for the window. This element is for the focused window.\nSee also: window.inactive.button.disabled.image.color\n"
    },
    'window.active.button.hover.bg': {
        'type': 'texture',
        'default': 'window.active.button.unpressed.bg',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when the mouse is over them. This element is for the focused window. When it is parentrelative, then it uses the window.active.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.hover.bg\n"
    },
    'window.active.button.hover.image.color': {
        'type': 'color',
        'default': 'window.active.button.unpressed.image.color',
        'info': "Specifies the color of the images in titlebar buttons when the mouse is over top of the button. This element is for the focused window.\nSee also: window.inactive.button.hover.image.color\n"
    },
    'window.active.button.pressed.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when they are being pressed by the user. This element is for the focused window. When it is parentrelative, then it uses the window.active.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.pressed.bg\n"
    },
    'window.active.button.pressed.image.color': {
        'type': 'color',
        'default': 'window.active.button.unpressed.image.color',
        'info': "Specifies the color of the images in titlebar buttons when they are being pressed by the user. This element is for the focused window.\nSee also: window.inactive.button.pressed.image.color\n"
    },
    'window.active.button.toggled.bg': {
        'type': 'texture',
        'default': 'window.active.button.pressed.bg',
        'parentrelative': 1,
        'info': "This property is obsolete and only present for backwards compatibility.\n"
    },
    'window.active.button.toggled.hover.bg': {
        'type': 'texture',
        'default': 'window.active.button.toggled.unpressed.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons if the user is pressing them with the mouse while they are toggled - such as when a window is maximized. This element is for the focused window. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.toggled.hover.bg\n"
    },
    'window.active.button.toggled.hover.image.color': {
        'type': 'color',
        'default': 'window.active.button.toggled.unpressed.image.color',
        'info': "Specifies the color of the images in the titlebar buttons when the mouse is hovered over them while they are in the toggled state - such as when a window is maximized. This element is for the focused window.\nSee also: window.inactive.button.toggled.hover.image.color\n"
    },
    'window.active.button.toggled.image.color': {
        'type': 'color',
        'default': 'window.active.button.pressed.image.color',
        'info': "This property is obsolete and only present for backwards compatibility.\n"
    },
    'window.active.button.toggled.pressed.bg': {
        'type': 'texture',
        'default': 'window.active.button.pressed.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons if the user is pressing them with the mouse while they are toggled - such as when a window is maximized. This element is for the focused window. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.toggled.pressed.bg\n"
    },
    'window.active.button.toggled.pressed.image.color': {
        'type': 'color',
        'default': 'window.active.button.pressed.image.color',
        'info': "Specifies the color of the images in the titlebar buttons if they are pressed on with the mouse while they are in the toggled state - such as when a window is maximized. This element is for the focused window.\nSee also: window.inactive.button.toggled.pressed.image.color\n"
    },
    'window.active.button.toggled.unpressed.bg': {
        'type': 'texture',
        'default': 'window.active.button.toggled.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons when they are toggled - such as when a window is maximized. This element is for the focused window. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.toggled.unpressed.bg\n"
    },
    'window.active.button.toggled.unpressed.image.color': {
        'type': 'color',
        'default': 'window.active.button.toggled.image.color',
        'info': "Specifies the color of the images in titlebar buttons when the button is toggled - such as when a window is maximized. This element is for the focused window.\nSee also: window.inactive.button.toggled.unpressed.image.color\n"
    },
    'window.active.button.unpressed.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons in their default, unpressed, state. This element is for the focused window. When it is parentrelative, then it uses the window.active.title.bg which is underneath it.\nSee also: titlebar colors, window.active.title.bg, window.inactive.button.unpressed.bg\n"
    },
    'window.active.button.unpressed.image.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the color of the images in titlebar buttons in their default, unpressed, state. This element is for the focused window.\nSee also: window.inactive.button.unpressed.image.color\n"
    },
    'window.active.client.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the color of the inner border for the focused window, drawn around the window but inside the other decorations.\nSee also: window.client.padding.width, window.inactive.client.color\n"
    },
    'window.active.grip.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for the focused window's grips. The grips are located at the left and right sides of the window's handle. When it is parentrelative, then it uses the window.active.handle.bg which is underneath it.\nSee also: window.handle.width, window.inactive.grip.bg, window.active.handle.bg\n"
    },
    'window.active.handle.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for the focused window's handle. The handle is the window decorations placed on the bottom of windows.\nSee also: window.handle.width, window.inactive.handle.bg\n"
    },
    'window.active.label.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for the focused window's titlebar label. The label is the container for the window title. When it is parentrelative, then it uses the window.active.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.label.bg, window.active.title.bg\n"
    },
    'window.active.label.text.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the color of the titlebar text for the focused window.\nSee also: window.inactive.label.text.color\n"
    },
    'window.active.label.text.font': {
        'type': 'text shadow string',
        'default': 'shadow=n',
        'info': "Specifies the shadow for the focused window's title.\nSee also: window.inactive.label.text.font\n"
    },
    'window.active.title.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for the focused window's titlebar.\nSee also: window.inactive.title.bg\n"
    },
    'window.active.title.separator.color': {
        'type': 'color',
        'default': 'window.active.border.color',
        'info': "Specifies the border color for the border between the titlebar and the window, for the focused window.\nSee also: window.inactive.title.separator.color\n"
    },
    'window.client.padding.height': {
        'type': 'integer',
        'default': 'window.client.padding.width',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the top and bottom sides of the inner border. The inner border is drawn around the window, but inside the other decorations.\nSee also: window.active.client.color, window.inactive.client.color window.client.padding.width\n"
    },
    'window.client.padding.width': {
        'type': 'integer',
        'default': 'padding.width',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the left and right sides of the inner border. The inner border is drawn around the window, but inside the other decorations.\nSee also: window.active.client.color, window.inactive.client.color window.client.padding.height\n"
    },
    'window.handle.width': {
        'type': 'integer',
        'default': '6',
        'lbound': 0,
        'ubound': 100,
        'info': "Specifies the size of the window handle. The window handle is the piece of decorations on the bottom of windows. A value of 0 means that no handle is shown.\nSee also: window.active.handle.bg, window.inactive.handle.bg, window.active.grip.bg, window.inactive.grip.bg\n"
    },
    'window.inactive.border.color': {
        'type': 'color',
        'default': 'window.active.border.color',
        'info': "Specifies the border color for all non-focused windows.\nSee also: border.width, window.active.border.color\n"
    },
    'window.inactive.button.disabled.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when they are disabled for the window. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.disabled.bg\n"
    },
    'window.inactive.button.disabled.image.color': {
        'type': 'color',
        'default': '#000000',
        'info': "Specifies the color of the images in titlebar buttons when they are disabled for the window. This element is for non-focused windows.\nSee also: window.active.button.disabled.image.color\n"
    },
    'window.inactive.button.hover.bg': {
        'type': 'texture',
        'default': 'window.inactive.button.unpressed.bg',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when the mouse is over them. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.hover.bg\n"
    },
    'window.inactive.button.hover.image.color': {
        'type': 'color',
        'default': 'window.inactive.button.unpressed.image.color',
        'info': "Specifies the color of the images in titlebar buttons when the mouse is over top of the button. This element is for non-focused windows.\nSee also: window.active.button.hover.image.color\n"
    },
    'window.inactive.button.pressed.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons when they are being pressed by the user. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.pressed.bg\n"
    },
    'window.inactive.button.pressed.image.color': {
        'type': 'color',
        'default': 'window.inactive.button.unpressed.image.color',
        'info': "Specifies the color of the images in titlebar buttons when they are being pressed by the user. This element is for non-focused windows.\nThis color is also used for pressed color when the button is toggled.\nSee also: window.active.button.pressed.image.color\n"
    },
    'window.inactive.button.toggled.bg': {
        'type': 'texture',
        'default': 'window.inactive.button.pressed.bg',
        'parentrelative': 1,
        'info': "This property is obsolete and only present for backwards compatibility.\n"
    },
    'window.inactive.button.toggled.hover.bg': {
        'type': 'texture',
        'default': 'window.inactive.button.toggled.unpressed.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons if the user is pressing them with the mouse while they are toggled - such as when a window is maximized. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.toggled.hover.bg\n"
    },
    'window.inactive.button.toggled.hover.image.color': {
        'type': 'color',
        'default': 'window.inactive.button.toggled.unpressed.image.color',
        'info': "Specifies the color of the images in the titlebar buttons when the mouse is hovered over them while they are in the toggled state - such as when a window is maximized. This element is for non-focused windows.\nSee also: window.active.button.toggled.hover.image.color\n"
    },
    'window.inactive.button.toggled.image.color': {
        'type': 'color',
        'default': 'window.active.button.pressed.image.color',
        'info': "This property is obsolete and only present for backwards compatibility.\n"
    },
    'window.inactive.button.toggled.pressed.bg': {
        'type': 'texture',
        'default': 'window.inactive.button.pressed.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons if the user is pressing them with the mouse while they are toggled - such as when a window is maximized. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.toggled.pressed.bg\n"
    },
    'window.inactive.button.toggled.pressed.image.color': {
        'type': 'color',
        'default': 'window.inactive.button.pressed.image.color',
        'info': "Specifies the color of the images in the titlebar buttons if they are pressed on with the mouse while they are in the toggled state - such as when a window is maximized. This element is for non-focused windows.\nSee also: window.active.button.toggled.pressed.image.color\n"
    },
    'window.inactive.button.toggled.unpressed.bg': {
        'type': 'texture',
        'default': 'window.inactive.button.toggled.bg',
        'parentrelative': 1,
        'info': "Specifies the default background for titlebar buttons when they are toggled - such as when a window is maximized. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.toggled.unpressed.bg\n"
    },
    'window.inactive.button.toggled.unpressed.image.color': {
        'type': 'color',
        'default': 'window.inactive.button.toggled.image.color',
        'info': "Specifies the color of the images in titlebar buttons when the button is toggled - such as when a window is maximized. This element is for non-focused windows.\nSee also: window.active.button.toggled.unpressed.image.color\n"
    },
    'window.inactive.button.unpressed.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for titlebar buttons in their default, unpressed, state. This element is for non-focused windows. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.inactive.title.bg, window.active.button.unpressed.bg\n"
    },
    'window.inactive.button.unpressed.image.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the color of the images in titlebar buttons in their default, unpressed, state. This element is for non-focused windows.\nSee also: window.active.button.unpressed.image.color\n"
    },
    'window.inactive.client.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the color of the inner border for non-focused windows, drawn around the window but inside the other decorations.\nSee also: window.client.padding.width, window.active.client.color\n"
    },
    'window.inactive.grip.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for non-focused windows' grips. The grips are located at the left and right sides of the window's handle. When it is parentrelative, then it uses the window.inactive.handle.bg which is underneath it.\nSee also: window.handle.width, window.active.grip.bg, window.inactive.handle.bg\n"
    },
    'window.inactive.handle.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for non-focused windows' handles. The handle is the window decorations placed on the bottom of windows.\nSee also: window.handle.width, window.active.handle.bg\n"
    },
    'window.inactive.label.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': 1,
        'info': "Specifies the background for non-focused windows' titlebar labels. The label is the container for the window title. When it is parentrelative, then it uses the window.inactive.title.bg which is underneath it.\nSee also: titlebar colors, window.active.label.bg, window.inactive.title.bg\n"
    },
    'window.inactive.label.text.color': {
        'type': 'color',
        'default': '#FFFFFF',
        'info': "Specifies the color of the titlebar text for non-focused windows.\nSee also: window.active.label.text.color\n"
    },
    'window.inactive.label.text.font': {
        'type': 'text shadow string',
        'default': 'shadow=n',
        'info': "Specifies the shadow for non-focused windows' titles.\nSee also: window.active.label.text.font\n"
    },
    'window.inactive.title.bg': {
        'type': 'texture',
        'default': 'none',
        'parentrelative': False,
        'info': "Specifies the background for non-focused windows' titlebars.\nSee also: window.active.title.bg\n"
    },
    'window.inactive.title.separator.color': {
        'type': 'color',
        'default': 'window.inactive.border.color',
        'info': "Specifies the border color for the border between the titlebar and the window, for non-focused windows.\nSee also: window.active.title.separator.color\n"
    },
    'window.label.text.justify': {
        'type': 'justification',
        'default': 'Left',
        'info': "Specifies how window titles are aligned in the titlebar for both the focused and non-focused windows.\n"
    }
}

imageButtons = {
    'max': {
        'default': [None],
        'info': "Maximize button in its default, unpressed state.\n"
    },
    'max_toggled': {
        'default': ['max', None],
        'info': "Maximize button when it is in toggled state.\n"
    },
    'max_pressed': {
        'default': ['max', None],
        'info': "Maximized button when pressed.\n"
    },
    'max_disabled': {
        'default': ['max', None],
        'info': "Maximized button when disabled.\n"
    },
    'max_hover': {
        'default': ['max', None],
        'info': "Maximized button when mouse is over it.\n"
    },
    'max_toggled_pressed': {
        'default': ['max_toggled', 'max', None],
        'info': "Maximized button when pressed, in toggled state.\n"
    },
    'max_toggled_hover': {
        'default': ['max_toggled', 'max', None],
        'info': "Maximized button when mouse is over it, in toggled state.\n"
    },

    'iconify': {
        'default': [None],
        'info': "Iconify button in its default, unpressed state.\n"
    },
    'iconify_pressed': {
        'default': ['iconify', None],
        'info': "Iconify button when pressed.\n"
    },
    'iconify_disabled': {
        'default': ['iconify', None],
        'info': "Iconify button when disabled.\n"
    },
    'iconify_hover': {
        'default': ['iconify', None],
        'info': "Iconify button when mouse is over it.\n"
    },

    'close': {
        'default': [None],
        'info': "Close button in its default, unpressed state.\n"
    },
    'close_pressed': {
        'default': ['close', None],
        'info': "Close button when pressed.\n"
    },
    'close_disabled': {
        'default': ['close', None],
        'info': "Close button when disabled.\n"
    },
    'close_hover': {
        'default': ['close', None],
        'info': "Close button when mouse is over it.\n"
    },

    'desk': {
        'default': [None],
        'info': "All-desktops button in its default, unpressed state.\n"
    },
    'desk_toggled': {
        'default': ['desk', None],
        'info': "All-desktops button when it is in toggled state.\n"
    },
    'desk_pressed': {
        'default': ['desk', None],
        'info': "All-desktops button when pressed.\n"
    },
    'desk_disabled': {
        'default': ['desk', None],
        'info': "All-desktops button when disabled.\n"
    },
    'desk_hover': {
        'default': ['desk_toggled', 'desk', None],
        'info': "All-desktops button when mouse is over it.\n"
    },
    'desk_toggled_pressed': {
        'default': ['desk_toggled', 'desk', None],
        'info': "All-desktops button when pressed, in toggled state.\n"
    },

    'shade': {
        'default': [None],
        'info': "Shade button in its default, unpressed state.\n"
    },
    'shade_toggled': {
        'default': ['shade', None],
        'info': "Shade button when it is in toggled state.\n"
    },
    'shade_pressed': {
        'default': ['shade', None],
        'info': "Shade button when pressed.\n"
    },
    'shade_disabled': {
        'default': ['shade', None],
        'info': "Shade button when disabled.\n"
    },
    'shade_hover': {
        'default': ['shade', None],
        'info': "Shade button when mouse is over it.\n"
    },
    'shade_toggled_pressed': {
        'default': ['shade_toggled', 'shade', None],
        'info': "Shade button when pressed, in toggled state.\n"
    },
    'shade_toggled_hover': {
        'default': ['shade_toggled', 'shade', None],
        'info': "Shade button when mouse is over it, in toggled state.\n"
    },

    'bullet': {
        'default': [None],
        'info': "The bullet shown in a menu for submenu entries.\n"
    }
}
