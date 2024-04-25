MANIFEST:
========
This scipt generates first level bucket report for all devices attached to a iDrive user account.
For each of the devices generates a csv output where directories are sorted by their size.

SETUP:
=====
- update system python3 to 3.12.3   
https://www.python.org/downloads/release/python-3123/

- for debugging with VS Code:
set VS default Interpreter to system Python:
    - Ex: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3  

RUN:
===
- login to iDrive account from web interface
- get the token from the API call
- enter the token in the constant.py file
- run:> python3 idrive-web-scrape.py 