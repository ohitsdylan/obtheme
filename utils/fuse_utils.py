# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import time
import errno
import fuse
import stat
from fuse import Fuse, Stat


class MyStat(Stat):
    def __init__(self):
        self.st_mode = stat.S_IFDIR | 0755
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 2
        self.st_uid = os.getuid()
        self.st_gid = os.getgid()
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class SimpleDir(Fuse):
    fuse.fuse_python_api = (0, 2)

    def __init__(self, *args, **kw):
        Fuse.__init__(self, *args, **kw)
        self.flags = 0
        self.multithreaded = 0
        self.files = {}
        # self.files['themerc'] = ''

    def getattr(self, path):
        st = MyStat()
        st.st_atime = int(time())
        st.st_mtime = st.st_atime
        st.st_ctime = st.st_atime
        if path == '/':
            pass
        elif path[1:] in self.files:
            st.st_mode = stat.S_IFREG | 0666
            st.st_nlink = 1
            st.st_size = len(self.files[path[1:]])
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        dirents = ['.', '..']
        if path == '/':
            dirents.extend(self.files.keys())
        for r in dirents:
            yield fuse.Direntry(r)

    def read(self, path, size, offset):
        if path[1:] in self.files:
            return self.files[path[1:]][offset:offset+size]
        else:
            return -errno.ENOENT

    def write(self, path, buf, offset):
        l = len(buf)
        if path[1:] in self.files:
            if offset == 0:
                self.files[path[1:]] = ''
            self.files[path[1:]] += buf
            return l
        else:
            return -errno.ENOENT

    def mknod(self, path, mode, dev):
        if len(path) > 1:
            self.files[path[1:]] = ''
        return 0

    def unlink(self, path):
        if path[1:] in self.files:
            del self.files[path[1:]]
        return 0

    def open(self, path, flags):
        return 0

    def truncate(self, path, size):
        return 0

    def chown(self, *args):
        return 0

    def utime(self, path, times):
        return 0

    def mkdir(self, path, mode):
        return 0

    def rmdir(self, path):
        return 0

    def rename(self, pathfrom, pathto):
        return 0

    def fsync(self, path, isfsyncfile):
        return 0

    def release(self, path, flags):
        return 0
