# coding: cp1252

import sys
from cx_Freeze import setup, Executable
base = None



build_exe_options = {
    "packages": ["psycopg2", "threading", "time", "datetime", "json", "os", "logging", "dotenv", "codecs", "serial", "icmplib"],
    "include_files": [
        "logs/",
        ".env"
        ]
    }
if sys.platform == 'win32':
    base = "Win32GUI"



setup(
    name="Hindalco Data Driver",
    version="0.1",
    description="Hindalco Data Driver app",
    options={"build_exe":build_exe_options},
    executables=[Executable("main.py")]
    )