import cx_Freeze
import sys
import os

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r"C:\Users\MadGeek\AppData\Local\Programs\Python\Python38-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\MadGeek\AppData\Local\Programs\Python\Python38-32\tcl\tk8.6"

executables = [cx_Freeze.Executable('notepad.py', base=base, icon='icon.ico')]

cx_Freeze.setup(
    name='Notepad',
    options={'build_exe': {'packages': ['tkinter', 'os'], 'include_files': ['assets', 'icon.ico', 'tcl86t.dll', 'tk86t.dll']}},
    version='1.0',
    author='Md. Hasibul Hasan Shovo',
    author_email='it.hhs19@gmail.com',
    description='Notepad is a free source code editor that runs in the Microsoft Windows environment.',
    keywords=['notepad', 'editor', 'notepad_editor'],
    executables=executables
)
