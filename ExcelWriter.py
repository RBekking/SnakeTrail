#
#
#!python3.exe
# Tested with python 3.6.1

from openpyxl import Workbook
from openpyxl import load_workbook

class ExcelWriter:
    def __init__(self, filename):
        self.wb = Workbook()
        self.ws = wb.active
        self.filename = filename

    def __del__(self):
        self.wb.save(self.filename)

    def save(self, object):
        print(object)
