from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.install import install as _install
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import os
import sys
import shutil
from subprocess import run
from glob import glob


if "." in sys.path:
    sys.path.remove(".")
if "" in sys.path:
    sys.path.remove("")
if os.getcwd() in sys.path:
    sys.path.remove(os.getcwd())

import _tkinter

tcl = _tkinter.create(None, "", "Tcl", False, False, False)
tcl_dir = tcl.eval("info library")
version = tcl.eval("info patchlevel")

internal_dir = os.path.join("build", "lib", "_tkinter_ext")
if os.path.isdir(internal_dir):
    # Make sure not to pick up libs from a previous build
    shutil.rmtree(internal_dir)
os.makedirs(internal_dir)

# Copy the tkinter extension module
shutil.copy(_tkinter.__file__, os.path.join(internal_dir, os.path.basename(_tkinter.__file__)))

# Copy the dependencies (on Linux, we use auditwheel after the fact)
if sys.platform == "win32":
    dll_ver = tcl.eval("info tclversion").replace(".", "")
    dll_dir = os.path.dirname(_tkinter.__file__)
    shutil.copy(os.path.join(dll_dir, f"tcl{dll_ver}t.dll"), internal_dir)
    shutil.copy(os.path.join(dll_dir, f"tk{dll_ver}t.dll"), internal_dir)

elif sys.platform == "darwin":
    dylib_ver = tcl.eval("info tclversion")
    dylib_dir = os.path.normpath(os.path.join(os.path.dirname(_tkinter.__file__), "..", ".."))
    tcl_dylib = f"libtcl{dylib_ver}.dylib"
    tk_dylib = f"libtk{dylib_ver}.dylib"
    shutil.copy(os.path.join(dylib_dir, tcl_dylib), internal_dir)
    shutil.copy(os.path.join(dylib_dir, tk_dylib), internal_dir)
    os.chmod(os.path.join(internal_dir, tcl_dylib), 0o755)
    os.chmod(os.path.join(internal_dir, tk_dylib), 0o755)

    # Make all the library references relative.
    run([
        "install_name_tool", "-id",
        "@loader_path/" + tcl_dylib,
        os.path.join(internal_dir, tcl_dylib),
    ], check=True)
    run([
        "install_name_tool", "-id",
        "@loader_path/" + tk_dylib,
        os.path.join(internal_dir, tk_dylib),
    ], check=True)
    run([
        "install_name_tool", "-change",
        os.path.join(dylib_dir, tcl_dylib), "@loader_path/" + tcl_dylib,
        os.path.join(internal_dir, os.path.basename(_tkinter.__file__)),
    ], check=True)
    run([
        "install_name_tool", "-change",
        os.path.join(dylib_dir, tk_dylib), "@loader_path/" + tk_dylib,
        os.path.join(internal_dir, os.path.basename(_tkinter.__file__)),
    ], check=True)

# Copy the Tcl data files
target_tcl_dir = os.path.join(internal_dir, "tcl", os.path.basename(tcl_dir))
if os.path.isdir(target_tcl_dir):
    shutil.rmtree(target_tcl_dir)
shutil.copytree(tcl_dir, target_tcl_dir)

# And the Tk data files, too
tk_dir = os.path.join(os.path.dirname(tcl_dir), os.path.basename(tcl_dir).replace("tcl", "tk"))
target_tk_dir = os.path.join(internal_dir, "tcl", os.path.basename(tk_dir))
if os.path.isdir(target_tk_dir):
    shutil.rmtree(target_tk_dir)
shutil.copytree(tk_dir, target_tk_dir)

# In my experiments, this was only necessary inside an .app on macOS
tcl8_dir = os.path.join(os.path.dirname(tcl_dir), os.path.basename(tcl_dir).split(".", 1)[0])
if os.path.isdir(tcl8_dir):
    target_tcl8_dir = os.path.join(internal_dir, "tcl", os.path.basename(tcl8_dir))
    if os.path.isdir(target_tcl8_dir):
        shutil.rmtree(target_tcl8_dir)
    shutil.copytree(tcl8_dir, target_tcl8_dir)

# Force it to be considered a platform-specific wheel
class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

# Prevent the tkinter package being put inside a purelib directory
class install(_install):
    def finalize_options(self):
        _install.finalize_options(self)
        self.install_lib = self.install_platlib

setup(
    name="tkinter",
    version=version,
    py_modules=["_tkinter"],
    packages=["tkinter", "_tkinter_ext"],
    package_dir={"tkinter": "tkinter", "_tkinter_ext": "_tkinter_ext"},
    package_data={"_tkinter_ext": ["_tkinter_ext/tcl/*", "_tkinter_ext/tcl/*/*", "_tkinter_ext/tcl/*/*/*"]},
    cmdclass={"bdist_wheel": bdist_wheel, "install": install},
)
