from abc import abstractmethod
import pyautogui
import time

class AutomatedDialog:
    def __init__(self):
        self.warning = '''
        WARNING: all windows other than the terminal must be minimized. Please take the next few seconds to do that.
        '''
        self.setup()
        self.initial_warning()
        self.run()
        
    def initial_warning(self):
        print(self.warning)
        time.sleep(5)
        
    def setup(self):
        
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def open(self):
        pass
    
    def set_ref_location(self):
        self.ref = pyautogui.locateCenterOnScreen(self.ref_image)
        print(self.ref)

    @abstractmethod
    def close(self):
        pass

    def move(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.moveTo(abs_x, abs_y)
        
    def click(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.click(abs_x, abs_y)

    def doubleClick(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.doubleClick(abs_x, abs_y)
        


        
    
