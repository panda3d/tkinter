import os

this_dir = os.path.dirname(__file__)
tcl_dir = os.path.join(this_dir, 'tcl')
if not os.path.isdir(tcl_dir) and os.path.basename(this_dir) == 'MacOS':
    # We're probably inside a MacOS app
    tcl_dir = os.path.join(this_dir, '..', 'Resources', 'tcl')

if os.path.isdir(tcl_dir):
    for dir in os.listdir(tcl_dir):
        sub_dir = os.path.join(tcl_dir, dir)
        if os.path.isdir(sub_dir):
            if dir.startswith('tcl'):
                os.environ['TCL_LIBRARY'] = sub_dir
            if dir.startswith('tk'):
                os.environ['TK_LIBRARY'] = sub_dir
            if dir.startswith('tix'):
                os.environ['TIX_LIBRARY'] = sub_dir

del tcl_dir
del this_dir
del os
