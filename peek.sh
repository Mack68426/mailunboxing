#! /usr/bin/bash

LIST_NAME="6lo"
FILE="$LIST_NAME.csv"

if [ -f $FILE ]; then

    python3 $FILE

else
    echo "The file does not exist"
    echo
fi

