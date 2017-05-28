from cx_Freeze import setup, Executable

import os

os.environ['TCL_LIBRARY'] = "d:\\Anaconda\\Library\\lib\\tcl8"
os.environ['TK_LIBRARY'] = "d:\\Anaconda\\Library\\lib\\tk8.5"

setup(
    name = "FormFillScript",
    version = "0.1",
    description = "Script for filling web form",
    executables = [Executable("app.pyw")]
)
