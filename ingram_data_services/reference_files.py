# -*- coding: utf-8 -*-


class ReferenceFile:

    FORMAT_DELIMITED = "delimited"
    FORMAT_FIXED = "fixed"

    def __init(self, path, _type):
        self.path = path
        self.type = _type

    # def download
