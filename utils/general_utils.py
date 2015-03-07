# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import logging
import shutil
import re
from utils.color_utils import (color_to_str, str_to_color)


def format_ob_color_str(string):
    if string.startswith('rgb:'):
        string = string.replace('rgb:', '#')
        string = string.replace('/', '')

    # this is to handle color names
    if not string.startswith('#'):
        string = color_to_str(str_to_color(string))

    if len(string) == 4:
        string = re.sub(r'([\da-fA-F])', '\g<1>0', string)

    return string


def multiply_color(color, f):
    r = int(color[1:3], 16) * f
    if r > 255:
        r = 255
    g = int(color[3:5], 16) * f
    if g > 255:
        g = 255
    b = int(color[5:7], 16) * f
    if b > 255:
        b = 255
    return "#%02X%02X%02X" % (r, g, b)


def read_file(path):
    f = open(path, 'r')
    contents = f.read()
    f.close()
    return contents


def write_file(path, contents):
    '''Write contents to file
    Args:
        path
        contents
    '''
    try:
        f = open(path, 'w')
    except IOError as e:
        logging.error(u'Could not write theme content in {}: {}'
                      .format(path, e))
        return e
    else:
        f.write(contents)
        f.close()
        logging.debug(u'Wrote theme content in {}'
                      .format(path))
        return True


def which(program):
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def clear_dir(dpath):
    if os.path.exists(dpath):
        for item in os.listdir(dpath):
            if dpath[-1:] == '/':
                spath = dpath+item
            else:
                spath = dpath+'/'+item
            if os.path.isdir(spath):
                shutil.rmtree(spath)
            else:
                os.remove(spath)
