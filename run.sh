#! /usr/bin/bash

if [ ! -d "/FTP" ]; then
    python3 download-from-url.py
    sleep 2s
    echo Download successfully\n
fi
python3 main.py