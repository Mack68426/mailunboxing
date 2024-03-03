@echo off

set FILE="6lo.csv"

if exist %FILE% ( 
    python view-csv.py
) else (
    echo "The CSV file does not exist."
    echo:
)