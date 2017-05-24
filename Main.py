#!python3.exe
# Tested with python 3.6.1

import sys
import re
import math

from Crawler        import FarnellCrawler
from Component      import AltiumComponent
from ExcelWriter    import ExcelWriter

list_E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
list_E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]

def number_to_postfix(number, ohm='ohm', kohm='kohm', megohm='Mohm'):
    # Change 10.0 to 10 and keep 1.2 the way it is
    if number >= 1000000:
        number /= 1000000
        number = str(number).replace('.0', '') + megohm
    elif number >= 1000:
        number /= 1000
        number = str(number).replace('.0', '') + kohm
    else:
        number = number = str(number).replace('.0', '') + ohm

    return number

def generate_resistor_values(e_list, min, max):
    return_value = list()

    for decimals in [1, 10, 100, 1000, 10000, 100000, 1000000]:
        for entry in e_list:
            value = round(entry * decimals, 1)
            if value >= min and value <= max:
                return_value.append(number_to_postfix(value))

    return return_value

filters = {
    #'resistance': '|'.join(generate_resistor_values(list_E12, 10000, 22000)),
    #'resistance': '470kohm',
    'brand': 'multicomp',
    'resistor-case-style': '0603-1608-metric-',
    'resistance-tolerance': 'posneg-1pc',
    'range': 'exc-obs|inc-in-stock|exc-direct-ship',
    'packaging': 'cut-tape'
}

smd_resistor_page = 'http://nl.farnell.com/w/c/passive-components/resistors-fixed-value/chip-smd-resistors'
Farnell = FarnellCrawler(smd_resistor_page, filters, 10)
ResistorTable = ExcelWriter('ResistorTable.xlsx')

while True:
    response = Farnell.fetch(2)
    if not response: break
    Resistors = [AltiumComponent('=Resistance', 'Resistor', 'RESC1608X06N (0603)', 'Schematic\Symbols_ElektorStyle.SchLib', 'PCB resistors.PcbLib', 2).create(line) for line in response]
    ResistorTable.save(Resistors)

print('Done...')
