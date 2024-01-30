# OBJECTIVE:
#   read mbox members from tar.gz and
#   access each the message content in the members
import os
import pathlib
import re
import tarfile

import mailbox
from email import *
from email.message import Message
from email.utils import parsedate_to_datetime

# TODO: convert the .mbox files to .eml files without untarring 
# TODO: make a same tool in command line with `csplit` command

# project_dir = os.path.dirname(__file__)
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

    # new folder name built by mbox filename
    folder_name = re.search(r"\d\d\d\d-\d\d", mboxfile_path).group()

    # create folders to store email files by mbox
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(f"{out_dir}/{folder_name}", exist_ok=True)

    # read the .mbox file and split it
    for index, message in enumerate(mailbox.mbox(mboxfile_path), 1):

        # create email files one by one 
        with open(f"{out_dir}/{folder_name}/{folder_name}-{index}.eml", "w", encoding="utf-8") as file:
            file.write(message.as_string())



# TODO: 直接從壓縮檔中的項目擷取email內容
<<<<<<< HEAD
def _direct_read_tar():
=======
def _test_direct_read():
>>>>>>> c94e53230580c10275105947629ab87b3ab33ce1
    tar_path = f"{resource_dir}/{tar_file}"

    with tarfile.open(tar_path, "r:*") as tar:
        path_pattern = r"\d\d\d\d-\d\d.mbox"
        mbox_files = [re.search(path_pattern, name).group() 
                      if re.search(path_pattern, name) 
                      else None for name in tar.getnames()]
        
        mailboxes = [name for name in tar.getnames()]
        messages = [msg for mbox in mailboxes for msg in mailbox.mbox(mbox)]

        
        try:
            # read each the member content from tar.gz
            for member in tar.getmembers(): # walk through each member
                file = tar.extractfile(member.name)
                content = file.read() # member content in binary
                filename = re.search(path_pattern, member.name).group() #output file name

                f = open(f"{mailbox_dir}/{list_name}/{filename}.box", "wb")
                f.write(content)
                f.close()

            # split the mbox file to multiple

        except Exception as e:
            print(str(e))
    
# parse each message in single mbox file
def parse_message(message: Message):
    m = {key.lower(): message.get(key) for key in message.keys()}
    
    mail_info = {
        "date": m.pop("date"),
        "subject": m.pop("subject"),
        "from": m.pop("from"),
        "to" : m.get("to", "[No-Receiver or CC]"),
        "reply-to": m.get("reply-to") or m.get("in-reply-to") or "[No Reply]",
        # "content": m.pop("content"),
        "other": ";".join([*m])
    }

    return mail_info
        

def main():
    test_mbox_file_path = f"{resource_dir}/{tar_file[:-7]}/{list_name}/2013-05.mbox"
    tar_path = f"{resource_dir}/{tar_file}"
    mbox_pattern = r"\d\d\d\d-\d\d.mbox"

    # extract the mbox files in tar.gz to target directory
    extract_tarfile(tar_path, resource_dir)
    
    mboxfiles = [f"{filename}" for filename in pathlib.Path(f"{resource_dir}/{tar_file[:-7]}/{list_name}/").iterdir()]
    
    # store the .mbox files to mailbox.mbox objects
    mboxes = [mailbox.mbox(mbox) for mbox in mboxfiles]

    # parse the all message in each mboxfile from tar.gz 
    messages = [parse_message(msg) for mbox in mboxes for msg in mbox]
    
    for mbox in mboxfiles:
        # split mbox to multiple eml files
        mbox_to_eml(mbox, )
        

    # for index, msg in enumerate(mailbox.mbox(test_mbox_file_path)):
        # watching the email thread and header
        # print("No.", index)
        # print("Subject:"); print(msg["Subject"], end="\n\n")
        # print("From:"); print(msg["from"], end="\n\n")
        # print("To:"); print(msg["to"], end="\n\n")
        # print("Reply To:"); print(msg["reply-to"], end="\n\n")
        # print("In Reply To:"); print(msg["in-reply-to"], end="\n\n") # ***We only need to see the address in "In-Reply-To" field
        # print("\n")

if __name__ == "__main__":
    main()