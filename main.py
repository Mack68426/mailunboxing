import os
import csv
import email
from chardet import detect
from email.message import Message

list_name = '6lo'
resource_dir = "FTP" # store extracted data

# preprocessing downloaded email data through url
# still in process 
def save_to_csv(file_path):
    
    with open(f"{list_name}.csv", "w+", newline='') as csv_file:    
        writer = csv.DictWriter(csv_file, ["date", "subject", "from", "to", "reply", "content", "other"])
        writer.writeheader()
        for name in os.listdir(f"{resource_dir}/{list_name}/"):
            message_info = email.message_from_file(open(f"{resource_dir}/{list_name}/{name}"))

def read_email_from_file(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file:
        try:
            content = file.read()
            print(content)
        except IOError as ioerr:
            print(str(ioerr))
        except Exception as e:
            print(str(e))



if __name__ == "__main__":
    read_email_from_file(f"{resource_dir}/{list_name}/2013-05.eml")