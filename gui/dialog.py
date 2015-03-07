# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import gtk
import logging
logging.basicConfig(level=logging.DEBUG)


def dialog_yes_no(label, title):
    '''Show a Yes/No dialog
    Args:
        title and label
    Returns:
        user response
    '''
    label = gtk.Label(label)
    dialog = gtk.Dialog(title, None,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                         gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    dialog.vbox.pack_start(label)
    label.show()
    response = dialog.run()
    dialog.destroy()
    return response


def dialog_msg(label, msg, dlg_type):
    '''Show a message dialog
    Args:
        title and label
    '''
    label = gtk.Label(label)
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               dlg_type,
                               gtk.BUTTONS_OK)
    dialog.set_markup(msg)
    dialog.run()
    dialog.destroy()
