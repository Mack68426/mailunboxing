#! /usr/bin/bash

if [ ! -d "FTP" ]; then
    python3 download.py
    sleep 2s
    echo "Download successfully"
    echo

fi

python3 main.py
echo Done
echo
 
