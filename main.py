# ** See comment in parse_mail_from_file: 87 **
import mailbox
import os
import csv
import email
import pathlib
import re
from chardet import detect
from email.message import Message
from email.policy import *
list_name = '6lo'
resource_dir = "FTP" # store extracted data

# get the body in the email file
def get_message_body(message: Message):
    content = ""
    # walk_though_staff = [ part for part in message.walk()]

    for part in message.walk(): # walk through all the submessages in parent message
        if part.get_content_type() in ["text/plain", "text/html"]:
            # payload = part.get_payload()          # the raw text(str)
            payload = part.get_payload(decode=True) # the raw text(bytes)
            encoding = detect(payload)["encoding"] # check the encoding type
            # print("payload coding", detect(payload)["encoding"])
            content = payload.decode(encoding if encoding else "utf-8", errors="ignore")

    return content.encode().decode()

# get the infomation from each message in single mbox file
def parse_message(message: Message):
    text_content = get_message_body(message)
    m = {k.lower(): message.get(k, "N/A") for k in message.keys()}

    mail_info = {
        "date": m.get("date"),
        "subject": m.get("subject"),
        "from": m.get("from"),
        "to" : m.get("to", "[No Receiver]"),
        "reply": m.get("in-reply-to", "[No parent message]"),
        "content": text_content,

    }

    return mail_info


# still in process 
# preprocessing downloaded email data through url
def export(out_dir: str = '.', _format: str = "csv"):
    
    with open(f"{out_dir}/{list_name}.{_format.lower()}", "w+", newline='') as csv_file:    
        writer = csv.DictWriter(csv_file, ["date", "subject", "from", "to", "reply", "content"])
        writer.writeheader()
        
        for name in os.listdir(f"{resource_dir}/{list_name}"):

            message = email.message_from_file(open(f"{resource_dir}/{list_name}/{name}"), policy=default)
            message_info = parse_message(message)
            writer.writerow(message_info)


# process the `.mail` file and get the basic information.
def parse_mail_from_file(mail_dirname):

    # 列出目的目錄下的所有.mbox檔案
    # list all the mbox files in the target dir
    try:
        csvfile = open(f"{resource_dir}/{list_name}.csv", "w+", encoding="utf-8", newline='')
        writer = csv.DictWriter(csvfile, ["date", "subject", "from", "to", "reply", "content", "other"])
        writer.writeheader()

        # trying to use mbox to parse the message in `.mail` files
        for mbox_file in [f"{filename}" for filename in pathlib.Path(mail_dirname).iterdir()]:
            for message in mailbox.mbox(mbox_file):
                message_info = parse_message(message)
                writer.writerow(message_info)

    except Exception as e:
        print(str(e))
    
    finally:
        csvfile.close()



if __name__ == "__main__":
    parse_mail_from_file(f"{resource_dir}/{list_name}")