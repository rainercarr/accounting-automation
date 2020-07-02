import accutil
from automateddialog import *
from collections import namedtuple
import csv
import pyautogui
from selectcompany import *
import time


class EnterChecks(AutomatedDialog):

    def __init__(self, check_csv):
        self.ref_image = 'enterbanktransactions.png'
        self.check_csv = check_csv
        super().__init__()

    def run(self):
        self.import_checks()
        self.set_ref_location()
        # SelectCompany(self.company)
        self.open()
        self.enter_checks()
        self.close()

    def import_checks(self):
        data = list(csv.reader(open(self.check_csv)))
        # company name needs to be on line index 0
        self.company = data[0][0]
        # all other transaction data on line index 1 and below
        self.Check = namedtuple('Check', ['txn_type', 'cash_acct', 'check_no', 'recipient_type', 'date', 'id', 'recipient', 'amount', 'acct'])
        check_data = accutil.remove_blank_lines(data[1:])
        print(check_data)
        self.checks = []
        for record in check_data:
            if record[0] in ['Check', 'Manual Check']:
                self.checks.append(self.Check._make(record))
        print(self.checks)        

    def open(self):
        self.click(0, 0)
        self.move(25, 33)
        self.click(159, 46)
        time.sleep(5)

    def enter_checks(self):
        if len(self.checks) > 0:
            self.curr_cash_acct = self.checks[0].cash_acct
            self.initial_check_setup(self.checks[0])
            for check in self.checks:
                if check.cash_acct == self.curr_cash_acct:
                    self.enter_check(check)
                else:
                    self.close()
                    self.open()
                    self.curr_cash_acct = check.cash_acct
                    self.initial_check_setup(check)
                    self.enter_check(check)
            

    def initial_check_setup(self, check):
        #cash account
        pyautogui.click(956, 528)
        pyautogui.typewrite(check.cash_acct)
        #check number
        pyautogui.click(946, 556)
        pyautogui.typewrite(check.check_no)
        #print check register
        pyautogui.click(926, 579)
        #handwritten checks only
        pyautogui.click(926, 597)
        #click ok
        pyautogui.click(1029, 637)
        #check number higher than previous message
        pyautogui.click(987, 520)
        #check number lower than previous (must click both)
        pyautogui.click(890, 619)
        time.sleep(1)

    def enter_check(self, check):
        pyautogui.click(830, 339)
        if check.recipient_type == 'Vendor':
            pyautogui.click(830, 339)
            pyautogui.click(819, 371)
            # "normally you should use A/P" message
            pyautogui.click(951, 581)
            pyautogui.typewrite(check.id)
        elif check.recipient_type in ['Customer', 'Employee']:
            if check.recipient_type == 'Customer':
                pyautogui.click(830, 374)
            elif check.recipient_type == 'Employee':
                pyautogui.click(830, 387)
            pyautogui.click(819, 371)
            pyautogui.typewrite(check.id)
        else:
            # raise an error if there is no check id or recipient
            if check.recipient == '':
                raise Exception("No check recipient listed")
        # enter recipient name
        pyautogui.typewrite('\t')
        if check.recipient != '':
            pyautogui.typewrite(check.recipient)
        # check number 
        pyautogui.click(1120, 358)
        pyautogui.typewrite(check.check_no)
        # amount
        pyautogui.click(1123, 386)
        pyautogui.typewrite(check.amount)
        # date
        pyautogui.doubleClick(1122, 414)
        pyautogui.typewrite(check.date)
        # account
        pyautogui.click(776, 614)
        pyautogui.typewrite(check.acct)
        pyautogui.click(1055, 612)
        # click accept
        pyautogui.click(1149, 590)
        # click post
        pyautogui.click(1013, 741)
        # no post to job cost module
        pyautogui.click(1026, 611)

    def close(self):
        pyautogui.click(1199, 305)

if __name__ == '__main__':
    EnterChecks('./data/testcheck.csv')