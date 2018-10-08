@echo off
IF NOT EXIST %~dp0\venv\Scripts\python.exe (
  %~dp0\venv\Scripts\python.exe %~dp0\src\cli\tsu.py init
)

%~dp0\venv\Scripts\python.exe %~dp0\src\cli\tsu.py %*
