from email.iterators import _structure
import mailbox
import os
import csv
import email
from chardet import detect
from email.utils import parsedate_to_datetime
from email.message import EmailMessage, Message
from email.policy import *


list_name = '6lo'
resource_dir = "FTP" # store extracted data

def _attr_structure(msg, fp=None, level=0, include_default=False):
    """A handy debugging aid (customized by Mack)"""
    if fp is None:
        fp = None
    tab = ' ' * (level * 4)
    print(tab + msg.get_content_type() + " | Date: " + msg["date"], end='')
    if include_default:
        print(' [%s]' % msg.get_default_type())
    else:
        print()
    if msg.is_multipart():
        for subpart in msg.get_payload():
            _attr_structure(subpart, fp, level+1, include_default)

# get the body in the email message
def get_message_body(message: Message):
    content = ""
    
    for part in message.walk(): # walk through all the submessages in parent message
        if part.get_content_type() in ["text/plain", "text/html"]:

            payload = part.get_payload(decode=True) # the raw text(str)
            encoding = detect(payload)["encoding"] # check the encoding type
            
            # print("payload coding", detect(payload)["encoding"])
            content += payload.decode(encoding if encoding else "utf-8", errors="ignore")
            
    return content.encode().decode()


# get the infomation from each message in single mail file
def get_message_info(message: Message):
    mail_info = {}
    
    try:
        m = {k.lower(): message.get(k, "N/A") for k in message.keys()}
        text_content = get_message_body(message)

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

# export the processed email data downloaded through url
def export(out_dir: str = '.', _format: str = "csv") -> None:
    
    with open(f"{out_dir}/{list_name}.{_format.lower()}", "w+",encoding="utf-8", newline='') as csv_file:    
        writer = csv.DictWriter(csv_file, ["date", "subject", "from", "to", "reply", "content"])
        writer.writeheader()
        
        for fname in os.listdir(f"{resource_dir}/{list_name}"): # list all .mail files

            # read email files in resource directory
            for message in mailbox.mbox(f"{resource_dir}/{list_name}/{fname}", 
                                        factory=lambda f: email.message_from_binary_file(f, policy=default)):
                
                # get the basic information(ex: subject, to, from...) from an email
                message_info = get_message_info(message)
                
                writer.writerow(message_info)

def main() -> None:

    export()

if __name__ == "__main__":
    main()
