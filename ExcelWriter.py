#!python3.exe
# Tested with python 3.6.1

import xlsxwriter

class ExcelWriter:
    def __init__(self, filename):
        self.__first_run    = True
        self.last_row       = 1
        self.filename       = filename
        self.workbook       = xlsxwriter.Workbook(self.filename)
        self.worksheet      = self.workbook.add_worksheet()

    def close(self):
        self.workbook.close()

    def save_header(self, object):
        row = 0
        col = 0

        print("%s,%s" % (object[0][0].keys(), object[0][1].keys()))
        print('-' * 200)

            #self.worksheet.write(row, col, self.header[col])

        # Write commponent-specific columns
        #for j in range(object[0].num_parameters):
        #    self.worksheet.write(row, col + 1 + j, object[0].parameter_list[j][0])

    def save(self, object):
        row = self.last_row
        col = 0

        if self.__first_run:
            # Only write the column names one time at the top of the file
            self.save_header(object)
            self.__first_run = False

        #
        # for i in range(len(object)):
        #     for line in object:
        #         self.last_row += 1
        #         for i in range(len(line)):
        #             self.worksheet.write(self.last_row, col + i, line[i])
        #         for j in range(len(line[9])):
        #             self.worksheet.write(self.last_row, col + 18 + j, object[i].parameter_list[j][1])
