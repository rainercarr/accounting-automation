from automateddialog import *
from bwinstance import *
from collections import namedtuple
import csv
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
        # company name needs to be on line index 1
        self.company = data[1][0]
        Transaction = namedtuple('Transaction', ['txn_type', 'cash_acct', 'date', 'desc', 'amount', 'acct'])
        # all other transaction data on line index 2
        txn_data = data[2:]
        print(txn_data)
        self.txns = []
        for record in txn_data:
            self.txns.append(Transaction._make(record))

    # May want to move this to BWInstance because it is general.
    def select_company(self):
        self.click_company_button()
        if self.company == 'Mint Creek':
            self.select_mint_creek()
        elif self.company == 'About Frames':
            self.select_about_frames()
        else:
            raise Error('Invalid company')
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
        
    def select_deposit(self):
        pyautogui.moveTo(867, 392)
        pyautogui.click(867, 392)
        pyautogui.moveTo(815, 405)
        pyautogui.click(815, 405)
        
    def select_charge(self):
        pyautogui.moveTo(867, 392)
        pyautogui.click(867, 392)
        pyautogui.moveTo(820, 418)
        pyautogui.click(820, 418)

    def enter_cash_acct(self, cash_acct):
        pyautogui.moveTo(820, 418, duration=1)
        pyautogui.click(820, 418)
        pyautogui.typewrite(cash_acct)
        
    def enter_date(self, date):
        pyautogui.moveTo(1117, 472)
        pyautogui.doubleClick(1117, 472)
        pyautogui.typewrite(date)
        
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

    def close(self):
        pyautogui.moveTo(1230, 347)
        pyautogui.click(1230, 347)
    
if __name__ == '__main__':
    data_file = sys.argv[1]
    username, password = sys.argv[2:4]
    bw = BWInstance(username, password)
    e = EnterBankTransactions(data_file)
    bw.close()
        
