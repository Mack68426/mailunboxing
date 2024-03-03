@echo off
set DATA_DIR=".\FTP"

if not exist %DATA_DIR% (
    python download.py
    timeout /t 2
    echo downloaded successfilly!
    echo:
)

python main.py
echo Done.
echo:
