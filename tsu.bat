
IF NOT EXIST venv\bin\python.exe (
  venv\bin\python.exe src\cli\tsu.py init
)

venv\bin\python.exe %*
