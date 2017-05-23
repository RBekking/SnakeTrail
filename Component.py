#
#
#!python3.exe
# Tested with python 3.6.1

class Component:
    def __init__(self):
        self.value_refers_to = ''
        self.common_data = {}
        self.parameter_dict = {}

    def __str__(self):
        return_string = ''
        for key, val in self.common_data.items():
            return_string += '%s: %s, ' % (key, val)

        for key, val in self.parameter_dict.items():
            return_string += '%s: %s, ' % (key, val)

        return return_string

class AltiumComponent(Component):
    def __init__(self, value_refers_to, library_ref, footprint_ref, library_path, footprint_path, pin_count):
        self.library_ref = library_ref
        self.footprint_ref = footprint_ref
        self.library_path = library_path
        self.footprint_path = footprint_path
        self.pin_count = pin_count
        self.value_refers_to = value_refers_to

        self.common_data = {
            'Part Number' :                 '',
            'Manufacturer 1':               '',
            'Manufacturer Part Number 1':   '',
            'Supplier 1':                   '',
            'Supplier Part Number 1':       '',
            'Value':                        '',
            'Description':                  '',
            'ComponentLink1Description':    '',
            'ComponentLink1URL':            '',
            'Library Ref':                  '',
            'Footprint Ref':                '',
            'Library Path':                 '',
            'Footprint Path':               '',
            'Pin Count':                    '',
            'MOQ':                          '',
            'Unit Price':                   '',
            'Stock':                        '',
            '_Verified SCH':                '',
            '_Verified PCB':                ''
        }
        self.parameter_dict = {}

    def create(self, crawler_data):
        # mfr, mfr_part_num, sup, sup_part_num, description, datasheet_link, moq, unit_price, stock, parameter_list
        self.common_data['Library Ref']                 = self.library_ref
        self.common_data['Footprint Ref']               = self.footprint_ref
        self.common_data['Library Path']                = self.library_path
        self.common_data['Footprint Path']              = self.footprint_path
        self.common_data['Pin Count']                   = self.pin_count
        self.common_data['Value']                       = self.value_refers_to

        self.common_data['Part Number']                 = crawler_data[0] + '_' + crawler_data[1]
        self.common_data['Manufacturer 1']              = crawler_data[0]
        self.common_data['Manufacturer Part Number 1']  = crawler_data[1]
        self.common_data['Supplier 1']                  = crawler_data[2]
        self.common_data['Supplier Part Number 1']      = crawler_data[3]
        self.common_data['Description']                 = crawler_data[4]
        self.common_data['ComponentLink1Description']   = 'Datasheet'
        self.common_data['ComponentLink1URL']           = crawler_data[5]
        self.common_data['MOQ']                         = crawler_data[6]
        self.common_data['Unit Price']                  = crawler_data[7]
        self.common_data['Stock']                       = crawler_data[8]
        self.parameter_dict                             = crawler_data[9]

        return self.common_data, self.parameter_dict
