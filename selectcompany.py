from automateddialog import *

class SelectCompany(AutomatedDialog):
    def __init__(self, company):
        self.company = company
        self.ref_image = 'enterbanktransactions.png'
        super().__init__()
        print(self.ref)
    
    def run(self):
        self.set_ref_location()
        self.open()
        if self.company == 'Mint Creek':
            self.select_mint_creek()
        elif self.company == 'About Frames':
            self.select_about_frames()
        else:
            raise Exception('Invalid company')
        self.close()
    
    def open(self):
        # click company button
        self.click(244, 39)
        
    def select_mint_creek(self):
        self.click(174, 24)
        
    def select_about_frames(self):
        self.click(151, -105)        

    def close(self):
        # click OK
        self.click(279, 112)

if __name__ == '__main__':
    SelectCompany('Mint Creek')