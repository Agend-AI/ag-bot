import re

GET_OPTION = re.compile(r'\d')
GET_DAYNAME = re.compile(r'\w+-?\s?\w+')
GET_DATA = re.compile(r'(\d{2}).(\d{2}).(\d{4})')
GET_DATA_NA = re.compile(r'(\d{4}).(\d{2}).(\d{2})')
GET_NUMBER = re.compile(r'(\+\d{12,13})')
GET_SEPARATOR = re.compile(r'\D')

def format_number(number):
    number = number.strip().replace('\\', '')
    return number