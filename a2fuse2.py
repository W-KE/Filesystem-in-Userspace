# !/usr/bin/env python
#Ke Wang
#kwan964

from __future__ import print_function, absolute_import, division

import logging

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from passthrough import Passthrough
from memory import Memory

class A2Fuse2(Memory, Passthrough):
    def __init__(self, root):
        Passthrough.__init__(self, root)
        Memory.__init__(self)

        self.source = ['/' + path for path in os.listdir(root)]

    def create(self, path, mode, fi=None):
        if path in self.source:
            return Passthrough.create(self, path, mode, fi)
        else:
            return Memory.create(self, path, mode)

    def getattr(self, path, fh=None):
        if path in self.source:
            return Passthrough.getattr(self, path, fh)
        else:
            return Memory.getattr(self, path, fh)

    def getxattr(self, path, name, position=0):
        if path in self.source:
            return Passthrough.getxattr(self, path, name, position)
        else:
            return Memory.getxattr(self, path, name, position)

    def open(self, path, flags):
        if path in self.source:
            return Passthrough.open(self, path, flags)
        else:
            return Memory.open(self, path, flags)

    def read(self, path, size, offset, fh):
        if path in self.source:
            return Passthrough.read(self, path, size, offset, fh)
        else:
            return Memory.read(self, path, size, offset, fh)

    def readdir(self, path, fh):
        if path == '/':
            dir1 = list(Passthrough.readdir(self, path, fh))
            dir2 = Memory.readdir(self, path, fh)
            return dir1 + dir2

        if path in self.source:
            return Passthrough.readdir(self, path, fh)
        else:
            return Memory.readdir(self, path, fh)

    def unlink(self, path):
        if path in self.source:
            return Passthrough.unlink(self, path)
        else:
            return Memory.unlink(self, path)

    def write(self, path, data, offset, fh):
        if path in self.source:
            return Passthrough.write(self, path, data, offset, fh)
        else:
            return Memory.write(self, path, data, offset, fh)

    def flush(self, path, fh):
        if path in self.source:
            return Passthrough.flush(self, path, fh)

def main(mountpoint, root):
    FUSE(A2Fuse2(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[2], sys.argv[1])