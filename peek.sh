#! /usr/bin/bash

FILE="view-csv.py"

if [ ! $FILE ]; then
    echo $"You have to input a file name\n"
    exit
fi

if [ -f $FILE ]; then
    python3 $FILE

else
    echo $"The file does not exist\n"
fi

