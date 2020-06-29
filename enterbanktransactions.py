import accutil
from automateddialog import *
from bwinstance import *
from collections import namedtuple
import csv
import datetime
from dateutil.parser import parse
from os import path
import sys

class EnterBankTransactions(AutomatedDialog):
    def __init__(self, txn_csv):
        self.ref_image = 'enterbanktransactions.png'
        self.txn_csv = txn_csv
        super().__init__()

    def run(self):
        self.import_txns()
        self.set_ref_location()
        self.select_company()
        self.open()
        self.enter_txns()
        self.close()

    def import_txns(self):
        data = list(csv.reader(open(self.txn_csv)))
        # company name needs to be on line index 0
        self.company = data[0][0]
        # all other transaction data on line index 1 and below
        # transaction format
        Transaction = namedtuple('Transaction', ['txn_type', 'cash_acct', 'transfer_dest', 'date', 'desc', 'amount', 'acct'])
        txn_data = accutil.remove_blank_lines(data[1:])
        print(txn_data)
        self.txns = []
        for record in txn_data:
            self.txns.append(Transaction._make(record))

    # Want to move this to BWInstance because it is general.
    def select_company(self):
        self.click_company_button()
        if self.company == 'Mint Creek':
            self.select_mint_creek()
        elif self.company == 'About Frames':
            self.select_about_frames()
        else:
            raise Exception('Invalid company')
        self.select_company_click_ok()
        
    def click_company_button(self):
        self.click(244, 39)

    def select_mint_creek(self):
        self.click(174, 24)
        
    def select_about_frames(self):
        self.click(151, -105)
        
    def select_company_click_ok(self):
        self.click(279, 112)

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
            self.select_transfer()
            self.enter_cash_acct(record.cash_acct)
            self.enter_transfer_dest(record.transfer_dest)
            self.enter_date(record.date)
            self.enter_amount(record.amount)
            self.enter_desc(record.desc)
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
        pyautogui.moveTo(820, 418, duration=1)
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
        logfile_name = '_'.join([entry_date, "EnterBankTransactions", "log"])
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
        
