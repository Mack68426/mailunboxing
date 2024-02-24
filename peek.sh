#! /usr/bin/bash

if [ ! $1 ]; then
    echo you have to input a file name\n
    exit
fi
FILE=$1

if [ -f $FILE ]; then
    python3 view-csv

else
    echo The file does not exist\n
fi

