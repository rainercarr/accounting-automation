'''
This is a class of useful functions that could be handy throughout accounting automation tasks
'''
import datetime
from dateutil.parser import parse

'''
takes any text date format generally encountered, for example:
4-Mar-20, 2020/03/04, 3/4/20
and converts it to the project standard mm/dd/yyyy
'''
def get_clean_date(date):
    date_obj = parse(date)
    return to_standard_date(date_obj)

'''
returns year_month for a given text date (can be in any format)
4-Mar-20 -> 2020_03
3/4/20 -> 2020_03
'''
def get_year_month(date):
    datetime_obj = parse(date)
    return datetime.datetime.strftime(datetime_obj, '%Y_%m')

# gets today's date in mm/dd/yyyy text format
def get_todays_date():
    return to_standard_date(datetime.datetime.today())

def to_standard_date(datetime_obj):
    return datetime.datetime.strftime(datetime_obj, '%m/%d/%Y')

# removes blank lines of a table, produced by opening a csv
def remove_blank_lines(table):
    cleaned_table = []
    for row in table:
        for col in row:
            if col != '':
                cleaned_table.append(row)
                break
    return cleaned_table
        
