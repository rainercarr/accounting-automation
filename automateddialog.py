from abc import abstractmethod
import pyautogui
import time
'''
this is the parent class for each class where a certain task is implemented.
since each class requires certain points in a dialog box to be located, and a sequence of mouse movements, clicks, and text entries to be completed, basic actions can be commonly implemented here
'''

class AutomatedDialog:
    def __init__(self):
        # print a warning message to close open windows so pyautogui can detect open programs on screen
        self.warning = '''
        WARNING: all windows other than the terminal must be minimized. Please take the next few seconds to do that.
        '''
        # set the log path for all automated action logs
        self.log_folder = './logs/'
        self.setup()
        self.initial_warning()
        self.run()
        
    def initial_warning(self):
        print(self.warning)
        time.sleep(5)

    # set general pyautogui settings
    # if overriden in child classes, need to call superclass method as well.
    def setup(self):
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True

    '''
    this method should contain method calls for all gui actions to be performed
    pre-importing/processing of data should occur here as well
    must be second method of child class, after __init__()
    '''
    @abstractmethod
    def run(self):
        pass

    # open dialog where data entry will occur
    @abstractmethod
    def open(self):
        pass

    # locate given reference point shown in self.ref_image on screen
    def set_ref_location(self):
        self.ref = pyautogui.locateCenterOnScreen(self.ref_image)
        assert(self.ref is not None), "Reference location not found"
        print(self.ref)

    # close window after data entry complete
    @abstractmethod
    def close(self):
        pass

    # move mouse pointer to location relative to reference point
    def move(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.moveTo(abs_x, abs_y)

    # single left click in location relative to reference point
    def click(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.click(abs_x, abs_y)

    # double left click in location relative to reference point
    def doubleClick(self, rel_x, rel_y):
        abs_x = self.ref.x + rel_x
        abs_y = self.ref.y + rel_y
        pyautogui.doubleClick(abs_x, abs_y)
        


        
    
