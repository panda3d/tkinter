import sys
from _tkinter_ext import _tkinter
sys.modules['_tkinter'] = _tkinter
del _tkinter
del sys
