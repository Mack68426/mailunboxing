# -*- coding: utf-8 -*-

# OBJECTIVE:
#   read mbox members from tar.gz and
#   access each the message content in the members

# TODO: convert the .mbox files to .eml files without untarring 
# TODO: make a same tool in command line with `csplit` command

import os
import pathlib
import re
import csv
import tarfile
import mailbox
from chardet import detect
from email.message import Message

list_name = '6lo'
resource_dir = "resource" # store extracted data
mailbox_dir = "FTP" # store .eml files dsorted by mbox
tar_file = 'mbox0122_ast_b.tar.gz'
_test_mbox_file_path = f"{resource_dir}/{tar_file[:-7]}/{list_name}/2013-05.mbox"


# 解壓縮資料檔
# unpack the compressed data file
def extract_tarfile(file_path, out_dir="."):
    # check if the output dir exists
    # if yes, then skip
    # if not, then build a new folder
    os.makedirs(out_dir, exist_ok=True)
    
    # open the tar file and extract it
    tar = tarfile.open(file_path, "r:*")

    # item_files = [item.name for item in tar]
    tar.extractall(out_dir)
    

    tar.close()

# the main converter converting `.mbox` file to `.eml` files
def mbox_to_eml(mboxfile_path, out_dir='.') -> None:

    # new folder built by mbox filename
    folder_name = re.search(r"\d\d\d\d-\d\d", mboxfile_path).group()

    # create folders to store email files by mbox
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(f"{out_dir}/{folder_name}", exist_ok=True)

    # read the .mbox file and split it
    for index, message in enumerate(mailbox.mbox(mboxfile_path), 1):
        eml_filename = f"{out_dir}/{folder_name}/{folder_name}-{index}.eml"
        
        # create email files one by one 
        with open(eml_filename, "w+", encoding="UTF-8") as file:
            file.write(message.as_string())


def get_message_content(message: Message):
    content = ""
    
    for part in message.walk(): # walk through all the submessages in parent message
        if part.get_content_type() in ["text/plain", "text/html"]:
            # payload = part.get_payload()          # the raw text(str)
            payload = part.get_payload(decode=True) # the raw text(bytes)
            encoding = detect(payload)["encoding"] # check the encoding type
            # print("payload coding", detect(payload)["encoding"])
            content += payload.decode(encoding if encoding else "utf-8", errors="ignore")

    return content.encode().decode()

# get the infomation from each message in single mbox file
def parse_message(message: Message):
    text_content = get_message_content(message)
    m = {k.lower(): message.get(k, "N/A") for k in message.keys()}

    mail_info = {
        "date": m.pop("date"),
        "subject": m.pop("subject"),
        "from": m.pop("from"),
        "to" : m.pop("to", "[No Receiver]"),
        "reply": m.pop("in-reply-to", "[No parent message]"),
        "content": text_content,
        "other": ";".join([*m])
    }

    return mail_info

def main():

    tar_path = f"{resource_dir}/{tar_file}" # 壓縮檔路徑

    # 將壓縮資料檔案解壓縮到目地資料夾
    # extract the mbox files in tar.gz to target directory
    extract_tarfile(tar_path, resource_dir)
    
    # 列出目的目錄下的所有.mbox檔案
    # list all the mbox files in the target dir
    mboxfiles = [f"{filename}" for filename in pathlib.Path(f"{resource_dir}/{tar_file[:-7]}/{list_name}/").iterdir()]
    

    csvfile = open(f"{resource_dir}/{list_name}.csv", "w+", encoding="utf-8", newline='')
    writer = csv.DictWriter(csvfile, ["date", "subject", "from", "to", "reply", "content", "other"])
    writer.writeheader()
    
    for mbox_file in mboxfiles:
        
        # split mbox to multiple eml files
        # mbox_to_eml(mbox_file, f"{mailbox_dir}/{list_name}")

        for message in mailbox.mbox(mbox_file):
            message_info = parse_message(message)
            writer.writerow(message_info)
    
    csvfile.close()


if __name__ == "__main__":
    main()