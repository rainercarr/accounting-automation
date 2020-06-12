from collections import namedtuple
import csv
import pyautogui
import subprocess
import sys
import time

def pyautogui_setup():
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

# The goal of this program is to enter bank transactions
# This takes up the lion's share of my time with entering months

# Import Bank Transaction CSV file in the following format
# Deposit/Charge, Cash Account ID, Date (MM/DD/YYYY), Description, Amount, Bookkeeping Account ID

def initial_warning():
    warning = '''
    WARNING: all windows other than the terminal must be minimized. Please take the next few seconds to do that.
    '''
    print(warning)
    time.sleep(5)
    
def import_txns(filename):
    data = list(csv.reader(open(filename)))
    # company name needs to be on line index 1
    company = data[1][0]
    Transaction = namedtuple('Txn', ['txn_type', 'cash_acct', 'date', 'desc', 'amount', 'acct'])
    # all other transaction data on line index 2
    txn_data = data[2:3]
    print(txn_data)
    txns = []
    for record in txn_data:
        txns.append(Transaction._make(record))
    return company, txns

def open_bw_gold(username, password):
    subprocess.Popen(['Z:\Sage\BWProg\\BWLauncher.exe'])
    time.sleep(15)
    enter_username(username)
    enter_password(password)
    login_click_ok()
    time.sleep(5)

def enter_username(username):
    pyautogui.moveTo(620, 197)
    pyautogui.doubleClick(620, 197)
    pyautogui.typewrite(username)
    
def enter_password(password):
    pyautogui.moveTo(653, 225)
    pyautogui.click(653, 225)
    pyautogui.typewrite(password)
    
def login_click_ok():
    pyautogui.moveTo(846, 132)
    pyautogui.click(846, 132)

def select_company(company):
    pyautogui.moveTo(733, 224)
    pyautogui.click(733, 224)
    if company == 'Mint Creek':
        pyautogui.moveTo(663, 209)
        pyautogui.click(663, 209)
    elif company == 'About Frames':
        pyautogui.moveTo(640, 80)
        pyautogui.click(640, 80)
    pyautogui.moveTo(768, 297)
    pyautogui.click(768, 297)
    time.sleep(1)

# this can fail if the BW window location is moved by a human  
def open_enter_bank_txns():    
    #click CM
    pyautogui.click(509, 188)
    #mouseover Transactions
    pyautogui.moveTo(527, 213, duration=1)
    #mouseover Enter Bank Transactions
    pyautogui.moveTo(658, 261, duration=1)
    pyautogui.click(658, 261)
    time.sleep(5) # wait for slow dialog to open

def enter_txn(record):
    if record.txn_type == 'Deposit':
        select_deposit()
    elif record.txn_type == 'Charge':
        select_charge()
    enter_cash_acct(record.cash_acct)
    enter_date(record.date)
    enter_amount(record.amount)
    enter_desc(record.desc)
    enter_acct(record.acct)
    post()
    ok_post_prior_month()
    
def select_deposit():
    pyautogui.moveTo(867, 392)
    pyautogui.click(867, 392)
    pyautogui.moveTo(815, 405)
    pyautogui.click(815, 405)
    
def select_charge():
    pyautogui.moveTo(867, 392)
    pyautogui.click(867, 392)
    pyautogui.moveTo(820, 418)
    pyautogui.click(820, 418)
    
def enter_cash_acct(cash_acct):
    pyautogui.moveTo(820, 418, duration=1)
    pyautogui.click(820, 418)
    pyautogui.typewrite(cash_acct)
    
def enter_date(date):
    pyautogui.moveTo(1117, 472)
    pyautogui.doubleClick(1117, 472)
    pyautogui.typewrite(date)
    
def enter_amount(amount):
    pyautogui.moveTo(836, 471)
    pyautogui.click(836, 471)
    pyautogui.typewrite(amount)
    
def enter_desc(desc):
    pyautogui.moveTo(848, 502)
    pyautogui.click(848, 502)
    pyautogui.typewrite(desc)
    
def enter_acct(acct):
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
    
def post():
    pyautogui.moveTo(1043, 701)
    pyautogui.click(1043, 701)
    time.sleep(3)
    
def ok_post_prior_month():
    pyautogui.moveTo(889, 592)
    pyautogui.click(889, 592)

def close_bank_txns_window():
    pyautogui.moveTo(1230, 347)
    pyautogui.click(1230, 347)

def exit_bw_gold():
    # click x in corner of window
    pyautogui.moveTo(983, 125)
    pyautogui.click(983, 125)
    # click "Skip Backup"
    pyautogui.moveTo(734, 245)
    pyautogui.click(734, 245)
    
    
if __name__ == '__main__':
    filename = sys.argv[1]
    pyautogui_setup()
    initial_warning()
    
    # import company name and transactions from csv
    company, txns = import_txns(filename)
    print(txns)
    
    # read username/password if --open flag given
    try:
        flag = sys.argv[2]
        if flag == '--open':
            username, password = sys.argv[3:5]
            open_bw_gold(username, password)
    except IndexError:
        pass
    
    select_company(company)
    open_enter_bank_txns()
    for txn in txns:
        enter_txn(txn)
    close_bank_txns_window()
    exit_bw_gold()


