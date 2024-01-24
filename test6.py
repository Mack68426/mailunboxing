import os
import re
import tarfile
import mailbox
import pathlib
from email.message import Message, 
from email.parser import BytesParser
from email import policy

listname = '6lo'

def extract_mboxes(file_path):
    tar = tarfile.open(file_path, "r:gz")
    dir = "emails"

    if not os.path.isdir(dir):
        os.mkdir(dir)
    tar.extractall(dir)

def parse_maildir(dir_path):
    mdir_folders = ['tmp', 'new', 'cur'] # 
    mdir = mailbox.Maildir(dir_path, factory=None)
    
    # create dir if it is not existed
    for folder in mdir_folders:
        pathlib.Path(f"{dir_path}/{folder}").mkdir(exist_ok=True)
        
    print(mdir.list_folders())
        

def parse_message(message):

    if not isinstance(message, Message):
        raise TypeError("argument `message` is not a instance of `email.Message`\n")
    
    pass

def main():
    file_path = 'maildir0122_wM_wo.tar.gz'
    extract_mboxes(file_path)

    parse_maildir(f"emails/{file_path[:-7]}/{listname}")
    
    # count = 0
    # for m in mails:
    #     if count > 3:
    #         break
    #     print(m)

    #     count+=1

if __name__ == "__main__":
    main()