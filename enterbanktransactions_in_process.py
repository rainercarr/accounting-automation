import accutil
from automateddialog import *
from bwinstance import *
from collections import namedtuple
from copy import copy
import csv
import datetime
from dateutil.parser import parse
import json
from os import path
from random import randint
from recordclass import recordclass # mutable record class (mutable equivalent of namedtuple)
from selectcompany import *
import sys

class EnterBankTransactions(AutomatedDialog):
    def __init__(self, txn_csv):
        self.ref_image = 'enterbanktransactions.png'
        self.txn_csv = txn_csv
        super().__init__()

    def run(self):
        self.import_txns()
        self.set_ref_location()
        SelectCompany(self.company)
        self.open()
        self.enter_txns()
        self.close()
    
    def import_txns(self):
        # get filename from 
        self.load_statement_metadata()
        self.load_statement_format()
        self.load_statement()
        self.standardize_txn_format()
        self.set_txns_cash_acct()
        self.load_rules()
        self.apply_rules_to_txns()
        self.sort_txns()
        
    # get metadata about statement from filename
    def load_statement_metadata(self):
        fp = self.txn_csv.rstrip('.csv')
        filename_stem = ""
        split_char = ""
        if '\\' in fp:
            split_char = '\\'
        elif '/' in fp:
            split_char = '/'
        if split_char != "":
            filename_stem = fp.split(split_char)[-1:][0]
        else:
            filename_stem = fp
        filename_attrs = filename_stem.split('_')
        StatementMetadata = recordclass('StatementMetadata', ['year', 'month', 'bank', 'cash_acct', 'company_1', 'company_2'])
        self.statement = StatementMetadata._make(filename_attrs)
        self.company = self.statement.company_1 + ' ' + self.statement.company_2
    
    def load_statement_format(self):
        bankcsvs = json.load(open('./config/bankcsvs.json', 'r'))
        self.stat_format = json.load(open(bankcsvs[self.statement.bank]))
        # print(type(self.stat_format))

    def load_statement(self):
        data = list(csv.reader(open(self.txn_csv)))
        # remove blank rows
        txn_data = accutil.remove_blank_lines(data[1:])
        self.Transaction = recordclass('Transaction', self.stat_format['fields'])
        self.txns = []
        for record in txn_data:
            # add blank columns if needed for format
            while len(record) < len(self.stat_format['fields']):
                record.append('')
            # add as Transaction
            self.txns.append(self.Transaction._make(record))
        # print(self.txns)

    # makes changes to each record as specified in bank statement format json file
    def standardize_txn_format(self):
        for txn in self.txns:
            for field, entry in zip(txn.__fields__, txn):
                if field in self.stat_format['field_translations']:
                    if entry in self.stat_format['field_translations'][field]:
                        changes = self.stat_format['field_translations'][field][entry]
                        for change in changes:
                            change_field = change[0]
                            change_value = change[1]
                            setattr(txn, change_field, change_value)
                            
    def set_txns_cash_acct(self):
        for txn in self.txns:
            txn.transfer_dest = txn.cash_acct = self.statement.cash_acct
    
    def load_rules(self):
        # import ./config/rules.csv
        self.rules = list(csv.reader(open('./config/rules.csv')))
        Rule = namedtuple('Rule', ['match_type', 'desc', 'new_txn_type', 'new_desc', 'new_acct'])
        # convert each rule in list to a namedtuple
        for i in range(len(self.rules)):
            self.rules[i] = Rule._make(self.rules[i])

    def apply_rules_to_txns(self):
        for txn in self.txns:
            for rule in self.rules:
                if rule.match_type == 'beginning':
                    if txn.desc.startswith(rule.desc):
                        self.apply_rule(rule, txn)
                elif rule.match_type == 'contains':
                    if rule.desc in txn.desc:
                        self.apply_rule(rule, txn)
    
    def apply_rule(self, rule, txn):
        for field in rule._fields:
            if field.startswith("new_"):
                new_field_contents = getattr(rule, field)
                if new_field_contents != "":
                    setattr(txn, field[4:], new_field_contents)        
        # modify tuple in ways that apply

    def sort_txns(self):
        #export txns that need to be manually entered
        manual_entries = [[self.company]]
        match_accts = [[self.company]]
        auto_enter = []
        print(self.get_standard_fields())
        for txn in self.txns:
            if txn.txn_type.endswith("Manual") or txn.txn_type == 'Transfer':
                manual_entries.append(txn)
            elif not self.has_required_fields(txn):
                match_accts.append(txn)
            else:
                auto_enter.append(txn)
        # write manual entries to CSV in standard format
        batch_identifier = str(hex(randint(0, 2**23 - 1)))
        self.export_txns(manual_entries, 'Enter_Manually_' + batch_identifier)
        self.export_txns(match_accts, 'Match_Accounts_' + batch_identifier)
        # leave auto-enterable transactions in self.txns
        self.txns = auto_enter

    def has_required_fields(self, txn):
        for field in self.get_standard_fields():
            if getattr(txn, field) == "":
                return False
        return True
        #export txns that need to be matched with accounts
        #retain only txns that can be entered
    
    def get_standard_fields(self):
        bankcsvs = json.load(open('./config/bankcsvs.json', 'r'))
        standard = json.load(open(bankcsvs['standard']))
        return standard['fields']

    def txns_to_standard_format(self, list_of_records):
        standard_format_list = []
        for record in list_of_records:
            if isinstance(record, self.Transaction):
                standard_format_txn = [getattr(record, field) for field in self.get_standard_fields()]
                standard_format_list.append(standard_format_txn)
            else:
                standard_format_list.append(record)
        return standard_format_list

    def export_txns(self, list_of_records, description):
        # if there is actual data, not just the company name header
        if len(list_of_records) > 1:
            directory = './data/'
            standard_formatted_txns = self.txns_to_standard_format(list_of_records)
            txn_list_metadata = copy(self.statement)
            # make sure filename is marked as standard
            txn_list_metadata.bank = 'standard'
            filename = directory + "_".join(txn_list_metadata) + '_' + description + ".csv"
            with open(filename, 'w', newline='') as f:
                wr = csv.writer(f)
                wr.writerows(standard_formatted_txns) 

    # WARNING: Enter Bank Transactions window always opens in same location,
    # so any actions inside it have an absolute location!
    # Change in future to improve compatibility with multiple host computers
    def open(self):    
        #click CM
        self.click(20, 3)
        #mouseover Transactions
        self.move(38, 28)
        #mouseover Enter Bank Transactions
        self.move(169, 76)
        self.click(169, 76)
        time.sleep(5) # wait for slow dialog to open

    def enter_txns(self):
        for record in self.txns:
            self.enter_txn(record)
        
    def enter_txn(self, record):
        if record.txn_type == 'Transfer':
            self.enter_transfer_in_form(record)
        else:
            if record.txn_type == 'Deposit':
                self.select_deposit()
            elif record.txn_type == 'Charge':
                self.select_charge()    
            self.enter_cash_acct(record.cash_acct)
            self.enter_date(record.date)
            self.enter_amount(record.amount)
            self.enter_desc(record.desc)
            self.enter_acct(record.acct)
        self.post()
        self.ok_post_prior_month()
        self.log_record_entry(record)

    # we don't want to enter transfers unless we can verify that they're not entered twice.
    def enter_transfer_in_form(self, record):
        self.select_transfer()
        self.enter_cash_acct(record.cash_acct)
        self.enter_transfer_dest(record.transfer_dest)
        self.enter_date(record.date)
        self.enter_amount(record.amount)
        self.enter_desc(record.desc)
        
    def select_deposit(self):
        self.select_transaction_type()
        pyautogui.moveTo(815, 405)
        pyautogui.click(815, 405)
        
    def select_charge(self):
        self.select_transaction_type()
        pyautogui.moveTo(820, 418)
        pyautogui.click(820, 418)

    def select_transfer(self):
        self.select_transaction_type()
        pyautogui.moveTo(828, 455)
        pyautogui.click(828, 455)

    def select_transaction_type(self):
        pyautogui.moveTo(867, 392)
        pyautogui.click(867, 392)
        
    def enter_cash_acct(self, cash_acct):
        pyautogui.moveTo(820, 418, duration=1)3/2/2020
        pyautogui.click(820, 418)
        pyautogui.typewrite(cash_acct)

    def enter_transfer_dest(self, transfer_dest):
        pyautogui.click(1048, 418)
        pyautogui.typewrite(transfer_dest)
        
    def enter_date(self, date):
        pyautogui.moveTo(1117, 472)
        pyautogui.doubleClick(1117, 472)
        pyautogui.typewrite(accutil.get_clean_date(date))
        
    def enter_amount(self, amount):
        pyautogui.moveTo(836, 471)
        pyautogui.click(836, 471)
        pyautogui.typewrite(amount)
        
    def enter_desc(self, desc):
        pyautogui.moveTo(848, 502)
        pyautogui.click(848, 502)
        pyautogui.typewrite(desc)
        
    def enter_acct(self, acct):
        # account number field
        pyautogui.moveTo(760, 564, duration=0.5)
        pyautogui.click(760, 564)
        pyautogui.typewrite(acct)
        # click amount field
        pyautogui.moveTo(1078, 563, duration=0.5)
        pyautogui.click(1078, 563)
        # click Accept
        pyautogui.moveTo(1155, 542, duration=0.5)
        pyautogui.click(1155, 542)
        
    def post(self):
        pyautogui.moveTo(1043, 701)
        pyautogui.click(1043, 701)
        time.sleep(3)
        
    def ok_post_prior_month(self):
        pyautogui.moveTo(889, 592)
        pyautogui.click(889, 592)

    def log_record_entry(self, record):
        entry_date = accutil.get_year_month(record.date)
        logfile_name = entry_date + '_EnterBankTransactions_log'
        filepath = self.log_folder + logfile_name + '.csv'
        file = None
        if not path.isfile(filepath):
            file = open(filepath, 'w', newline='')
            file.close()
        file = open(filepath, 'a', newline='')
        csvwriter = csv.writer(file)
        entry = list(record) + [accutil.get_todays_date()] 
        csvwriter.writerow(entry)

    def close(self):
        pyautogui.moveTo(1230, 347)
        pyautogui.click(1230, 347)
        
'''
To run, type at command line:
python enterbanktransactions.py data_file username password
'''
if __name__ == '__main__':
    data_file = sys.argv[1]
    username, password = sys.argv[2:4]
    # bw = BWInstance(username, password)
    e = EnterBankTransactions(data_file)
    # bw.close()
        
