import accutil
from automateddialog import *
import csv
import pyautogui
from recordclass import recordclass
from selectcompany import *
import sys
import time


class PostToJournals(AutomatedDialog):
    def __init__(self, entry_csv):
        self.ref_image = 'posttojournals.png'
        self.entry_csv = entry_csv
        super().__init__()
    
    def run(self):
        self.import_entries()
        self.set_ref_location()
        SelectCompany(self.company)
        self.open()
        self.post_entries()
        self.close()

    def open(self):
        # click GL
        self.click(0, 0)
        # mouseover Entries
        self.move(9, 30)
        # click Post To Journals
        self.click(158, 30)
        # wait for dialog to open
        time.sleep(5)
    
    def import_entries(self):
        data = list(csv.reader(open(self.entry_csv)))
        data = accutil.remove_blank_lines(data)
        self.company = data[0][0]   
        entry_data = data[1:]    
        # date and desc are text fields; distribution is a list of distribution records
        self.Entry = recordclass('Entry', ['date', 'desc', 'distribution'])
        self.Distribution = recordclass('Distribution', ['type', 'amount', 'acct'])
        self.entries = []
        for record in entry_data:        
            if record[0] != "" and record[1] != "":
                record_list = record[0:2]
                dist_list = []
                dr = 0.0
                cr = 0.0
                for i in range(2, len(record), 3):
                    if record[i] in ['Debit', 'Credit']:
                        dist = self.Distribution._make([record[i], record[i + 1], record[i + 2]])
                        if dist.type == 'Debit':
                            dr += float(dist.amount)
                        elif dist.type == 'Credit':
                            cr += float(dist.amount)
                        dist_list.append(dist)
                if dr - cr != 0.0:
                    raise Exception(f'Debits do not equal credits for {record_list[0]}, {record_list[1]}')
                record_list.append(dist_list)
                curr_entry = self.Entry._make(record_list)
                self.entries.append(curr_entry)
        print(self.entries)


    def post_entries(self):
        for entry in self.entries:
            self.post_entry(entry)

    def post_entry(self, entry):
        self.enter_date(entry.date)
        self.enter_desc(entry.desc)
        for i in range(len(entry.distribution)):
            self.enter_dist(entry.distribution[i], i)        
        self.click_post()    

    def enter_date(self, date):
        pyautogui.doubleClick(782, 452)
        pyautogui.typewrite(date)
    
    def enter_desc(self, desc):
        pyautogui.click(1033, 431)
        pyautogui.typewrite(desc)
    
    def enter_dist(self, dist, idx):
        # if there are more than 7 lines of the entry
        # businessworks auto-scrolls. This accounts for that
        if idx <= 6:
            y_for_line = 544 + (idx * 16)
        else:
            y_for_line = 544 + (6 * 16)
        #Enter account number
        # only need to click to enter account number on first line
        if idx == 0:
            pyautogui.click(704, y_for_line)
        pyautogui.typewrite(dist.acct)
        if dist.type == 'Debit':
            pyautogui.click(1031, y_for_line)
            pyautogui.typewrite(dist.amount)
        elif dist.type == 'Credit':
            pyautogui.click(1107, y_for_line)
            pyautogui.typewrite(dist.amount)
        # Click Add button
        pyautogui.click(1214, 523)
    
    def click_post(self):
        pyautogui.click(1074, 719)
        time.sleep(1)
        pyautogui.click(1067, 609)

    def close(self):
        pyautogui.click(1257, 331)

if __name__ == '__main__':
    filename = sys.argv[1]
    PostToJournals(filename)