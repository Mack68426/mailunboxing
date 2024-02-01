# -*- coding: utf-8 -*-

# OBJECTIVE:
#   read mbox members from tar.gz and
#   access each the message content in the members

# TODO: convert the .mbox files to .eml files without untarring 
# TODO: make a same tool in command line with `csplit` command
import os
import pathlib
import re
import tarfile
import mailbox
from chardet import detect
from email.message import Message


list_name = '6lo'
resource_dir = "resource" # store extracted data
mailbox_dir = "emails" # store .eml files dsorted by mbox
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
        with open(eml_filename, "wb+") as file:
            file.write(message.as_bytes())



# TODO: 直接從壓縮檔中的項目擷取email內容
def _direct_read_tar():
    pass

def get_message_content(message: Message):
    content = ""
    
    for part in message.walk(): # walk through all the submessages in parent message
        if part.get_content_type() in ["text/plain", "text/html"]:
            # payload = part.get_payload()          # the raw text(str)
            payload = part.get_payload(decode=True) # the raw text(bytes)
            encoding = detect(payload)["encoding"] # check the encoding type
            # print("payload coding", detect(payload)["encoding"])
            content += payload.decode(encoding if encoding else "utf-8", errors="ignore")

    return content.encode()


# parse each message in single mbox file
def parse_message(message: Message):
    text_content = get_message_content(message)
    m = dict(map(lambda k: (k.lower(), message.get(k, "N/A")), message.keys()))

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

def _peek_thread():
    for index, msg in enumerate(mailbox.mbox(_test_mbox_file_path)):
        # watching the email thread and header
        print("No.", index)
        print("Subject:"); print(msg["Subject"], end="\n\n")
        print("From:"); print(msg["from"], end="\n\n")
        print("To:"); print(msg["to"], end="\n\n")
        print("Reply To:"); print(msg["reply-to"], end="\n\n")
        
        # We only need to see the address in "In-Reply-To" field
        # for checking the "parent message" in email thread 
        print("In Reply To:"); print(msg["in-reply-to"], end="\n\n") 
        print("\n")

def main():
    tar_path = f"{resource_dir}/{tar_file}"

    # 將壓縮資料檔案解壓縮到目地資料夾
    # extract the mbox files in tar.gz to target directory
    extract_tarfile(tar_path, resource_dir)
    
    # 列出目的目錄下的所有.mbox檔案
    # list all the mbox files in the target dir
    mboxfiles = [f"{filename}" for filename in pathlib.Path(f"{resource_dir}/{tar_file[:-7]}/{list_name}/").iterdir()]
    
    for mbox_file in mboxfiles:
        print("current file:", mbox_file)
        # split mbox to multiple eml files
        mbox_to_eml(mbox_file, f"{mailbox_dir}/{list_name}")

        for message in mailbox.mbox(mbox_file):
            message_info = parse_message(message)

            print(message_info)


if __name__ == "__main__":
    main()