@echo off
IF NOT EXIST %~dp0\venv\Scripts\python.exe (
  python %~dp0\src\cli\init.py
)

%~dp0\venv\Scripts\python.exe %~dp0\src\cli\tsu.py %*
