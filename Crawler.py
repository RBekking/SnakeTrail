#
#
#!python3.exe
# Tested with python 3.6.1

from lxml import html
from lxml import etree
import requests
from Component import AltiumComponent
import time

class Crawler:
    def __init__(self, homepage, filters, maxcomponents=0):
        self.__current_page = 1
        self.__current_row = 1
        self.__cumulative_row = 0

        self.data_xpaths = {
            'max_pages':    '',
            'num_rows':     '',
            'next_page':    ''
            }

        self.homepage = homepage
        self.filters = filters
        self.maxcomponents = maxcomponents
        self.parse_tree = html.fromstring(requests.get(self.homepage, self.filters).content)


    def parse_row(self, row_number):
        pass

    def get_max_pages(self):
        try:
            return int(self.parse_tree.xpath(self.data_xpaths['max_pages'])[0])
        except:
            return 1

    def get_rows(self):
        try:
            return len(self.parse_tree.xpath(self.data_xpaths['num_rows']))
        except:
            return 1

    def get_next_page(self):
        try:
            return self.parse_tree.xpath(self.data_xpaths['next_page'])[0]
        except:
            return ''

    def next_page(self):
        if self.__current_page < self.get_max_pages():
            self.__current_page += 1
            self.parse_tree = html.fromstring(requests.get(self.get_next_page(), self.filters).content)
            return True
        else:
            return False

    def fetch(self, how_many_per_session=0):
        if how_many_per_session == 0:
            how_many_per_session = self.maxcomponents

        return_value = []
        num_rows = self.get_rows()

        if num_rows == 0:
            print('[%s] Nothing to do...' % time.asctime(time.localtime()))
            return []

        line_counter = self.__cumulative_row
        while (self.__cumulative_row - line_counter) < how_many_per_session:
            if self.__cumulative_row >= self.maxcomponents:
                break
            self.__cumulative_row += 1

            return_value.append(self.parse_row(self.__current_row))
            self.__current_row += 1

            if self.__current_row >= num_rows:
                self.__current_row = 1
                self.next_page()

        return return_value


class FarnellCrawler(Crawler):
    def __init__(self, homepage, filters, maxcomponents=0):
        super().__init__(homepage, filters, maxcomponents)
        self.data_xpaths = {
            'max_pages':    '//span[@class="paginNext pageLink"]/a/@data-rel',
            'num_rows':     '//table[@id="sProdList"]/tbody/tr',
            'next_page':    '//a[@class="nextLinkPara "]/@href'
            }

    def parse_row(self, row_number):
        mfr             = None
        mfr_part_num    = None
        sup             = None
        sup_part_num    = None
        description     = None
        datasheet_link  = None
        moq             = None
        unit_price      = None
        stock           = None
        parameter_dict  = {}

        data_root = '//table[@id="sProdList"]/tbody/tr[%d]' % row_number

        try:
            mfr                         = self.parse_tree.xpath(data_root + '//td[@class="description"]/input/@value')[0]
            mfr_part_num                = self.parse_tree.xpath(data_root + '/td[@class="productImage mftrPart"]/input/@value')[0]
            sup                         = 'Farnell'
            sup_part_num                = self.parse_tree.xpath(data_root + '//p[@class="sku"]/a/@title')[0].strip()
            description                 = self.parse_tree.xpath(data_root + '//td[@class="description"]/a/p[2]/text()')[0]
            datasheet_link              = self.parse_tree.xpath(data_root + '//a[@class="prodDetailsAttachment"]/@href')[0]
            moq                         = self.parse_tree.xpath(data_root + '//span[@class="qty"]/text()')[0]
            unit_price                  = self.parse_tree.xpath(data_root + '//span[@class="qty_price_range"]/text()')[0]
            stock                       = self.parse_tree.xpath(data_root + '//span[@
