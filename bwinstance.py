from automateddialog import *
from subprocess import Popen
import sys
class BWInstance(AutomatedDialog):
    def __init__(self, username, password):
        self.ref_image = 'bwinstance.png'
        self.username = username
        self.password = password
        super().__init__()
        
    def run(self):
        self.open()
        self.set_ref_location()
        self.enter_username()
        self.enter_password()
        self.login_click_ok()
        
    def open(self):
        Popen(['Z:\Sage\BWProg\\BWLauncher.exe'])
        time.sleep(7)
    
    def enter_username(self):
        rel_x = 9
        rel_y = 53
        self.move(rel_x, rel_y)
        self.doubleClick(rel_x, rel_y)
        pyautogui.typewrite(self.username)
    
    def enter_password(self):
        rel_x = 42
        rel_y = 81
        self.move(rel_x, rel_y)
        self.click(rel_x, rel_y)
        pyautogui.typewrite(self.password)
        
    def login_click_ok(self):
        rel_x = 235
        rel_y = -12
        self.move(rel_x, rel_y)
        self.click(rel_x, rel_y)

    def close(self):
        self.click_x_button()
        self.click_skip_backup()

    def click_x_button(self):
        rel_x = 372
        rel_y = -19
        self.move(rel_x, rel_y)
        self.click(rel_x, rel_y)
        
    def click_skip_backup(self):
        rel_x = 123
        rel_y = 101
        self.move(rel_x, rel_y)
        self.click(rel_x, rel_y)
        
if __name__ == '__main__':
    username, password = sys.argv[1:3]
    bw = BWInstance(username, password)
    bw.close()
    
