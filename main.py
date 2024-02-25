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
def get_message_info(message: Message):
    mail_info = {}
    
    try:
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
    
    except Exception as e:
        print(str(e))
    
    return mail_info



# preprocessing downloaded email data through url
def export(out_dir: str = '.', _format: str = "csv"):
    
    with open(f"{out_dir}/{list_name}.{_format.lower()}", "w+",encoding="utf-8", newline='') as csv_file:    
        writer = csv.DictWriter(csv_file, ["date", "subject", "from", "to", "reply", "content"])
        writer.writeheader()
        
        for fname in os.listdir(f"{resource_dir}/{list_name}"):
            # read email files in resource directory
            for message in mailbox.mbox(f"{resource_dir}/{list_name}/{fname}"):
                # get the basic information(ex: subject, to, from...) from an email
                message_info = get_message_info(message)

            writer.writerow(message_info)

def main() -> None:

    export()

if __name__ == "__main__":
    main()
