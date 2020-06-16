Automated Transaction Entry For Legacy Accounting System
=======================================================
This Program uses PyAutoGUI to automate entry of bank transaction data into a legacy accounting system, Sage BusinessWorks Gold, AKA BW Gold.

The data is downloaded from a bank (this particular bank does not provide an API to access transactions).
The data is then formatted correctly (per test.csv), and the program manually enters it by importing the csv and 

The program logs into the accounting program with the username/password provided at the command line.
Then it leverages PyAutoGUI's automated mouse movement, clicking, and typewriting functions to enter the data.

I initially banged this out in roughly two hours, knowing nothing of PyAutoGUI beforehand. When I was a bookkeeper, the tasks this program completes automatically took me an entire day each month.

Dependencies

Python 3 (only has been tested on 3.8)
PyAutoGUI 0.9.50+
dateutil 2.8.1+ (pip package name "python-dateutil")
