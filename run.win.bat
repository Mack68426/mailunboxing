@echo off
set DATA_DIR=".\FTP"

if not exist %DATA_DIR% (
    python download.py
    timeout /t 2
    echo downloaded successfilly!
    echo:
)

python get_info.py
echo Done.
echo:
