#! /usr/bin/bash

FILE="view-csv.py"

if [ -f $FILE ]; then

    python3 $FILE

else
    echo "The file does not exist"
    echo
fi

