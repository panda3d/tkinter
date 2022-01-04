Python interface to Tcl/Tk
==========================

This is the Python built-in tkinter module, except supplied separately.

It is useful when using a build of Python that does not have tkinter included,
such as in a virtual environment on an Ubuntu installation without python3-tk.

Documentation: https://docs.python.org/3/library/tkinter.html

Building
--------

To build the wheel, just type:

```
python setup.py bdist_wheel
```

On Windows and macOS, the dependencies are copied automatically.
On Linux, you need to use auditwheel to do this, but see the included
`build_manylinux.sh` script.

License
-------

The `tkinter` directory is lifted from the Python source, so its license is
that of the Python source (Python Software Foundation license).
