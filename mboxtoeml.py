import os
import re

import tarfile
import pathlib

from email.utils import parsedate_to_datetime

import mailbox
from email.message import Message, EmailMessage
from email.parser import BytesParser, Parser
from email.policy import default, compat32
from email.generator import Generator
from typing import List
#########################################################

# DONE: get all the content in the .mbox files.
# DONE: convert .mbox to .eml
# DONE: split mbox to .eml files

proj_dir = os.path.dirname(__file__)
path_to_extract = "/mails/"
list_name = '6lo'



# 解壓縮資料檔
# unpack the compressed data file
def extract_tarfile(file_name):
    tar = tarfile.open(file_name, "r:gz")
    dir_name = "."

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    tar.extractall(dir_name)

'''
# 解析 .mbox 檔的內容
# parse the content in .mbox file
def mbox_parser(mbox_name):
    mbox = mailbox.mbox(mbox_name)
    for index, message in enumerate(mbox):
        # print("No.", index)
        # print("Total amount:",len(message))
        # print("From:", message['from'])
        # print("To:", message["to"])
        print("Content-Type:", message.get_content_type())
        print(message.get_content_maintype())
        # print("all tags:", message.keys())
        print("Content:", message.get_payload(decode=True))
        # print(end='\n\n')

        mail = {
            "from": message["from"],
            "to"  : message["to"],
            "subject": message["subject"],
            "content": message.as_string(unixfrom=True)
        }

        yield mail
'''

# split single .mbox file to multiple .eml files
def split_mbox(mbox_obj: mailbox.mbox) -> List[mailbox.mboxMessage]:
    message_files = []

    # handle exception
    if not isinstance(mbox_obj, mailbox.mbox):
        raise TypeError("It's not a instance of `mbox` in module mailbox.\n")
    
    for message in mbox_obj:
        # message_files.append(message.as_string(unixfrom=True))
        message_files.append(message)
        
        print("Message to string:")
        print(message.as_string(unixfrom=True))

    return message_files

def save_message_as(message: mailbox.mboxMessage, out_dir=".", filename: str or None=None, ext_name="txt"):
    # handle exception
    if isinstance(message, (mailbox.mboxMessage, Message)):
        raise TypeError("The type of passing message is wrong.\n")
    
    # convert the datetime in email to python's datetime
    if filename is None: 
        filename = parsedate_to_datetime(message["date"])
    
    while not os.path.exists(f"{out_dir}/{filename}/"):
        os.makedirs(f"{out_dir}/{filename}/", exist_ok=True)
    
    with open("{}.{}".format(filename, ext_name), "w", encoding="UTF-8") as file:
        file.write(message.as_string())

def save_mbox_as_eml(mbox_obj: mailbox.mbox, out_dir="."):
    if isinstance(mbox_obj, mailbox.mbox):
        raise TypeError("The passing object is not a instance of mbox.\n")

    

def mboxtoeml_main():
    tar_file = 'mbox0122_ast_b.tar.gz'
    data_dir = tar_file[:-7] + "/" + list_name
    mbox_files = [file.name for file in pathlib.Path(data_dir).iterdir()]
    mbox_name = f"{data_dir}/2013-05.mbox"
    mbox = mailbox.mbox(mbox_name)
    
    # extract the tarfile
    if not pathlib.Path(data_dir).exists():
        extract_tarfile(tar_file)

    for msg in split_mbox(mbox):
        save_message_as(msg, out_dir=path_to_extract)

    # convert mbox to eml, maybe?
    # for mboxfile in mbox_files:
    #     mbox = mailbox.mbox(mboxfile)
        
    #     for msg in split_mbox(mbox):
    #         save_message_as(msg, out_dir=path_to_extract, ext_name="eml")
    



if __name__ == "__main__":
    mboxtoeml_main()