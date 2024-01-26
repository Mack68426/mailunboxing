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

tar_file = 'mbox0122_ast_b.tar.gz'
data_dir = tar_file[:-7] + "/" + list_name


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

def save_message_as(message: mailbox.mboxMessage, folder_name=".", filename: str or None=None, ext_name="txt"):
    # handle type exception
    if not isinstance(message, (mailbox.mboxMessage, Message)):
        raise TypeError("The type of passing message is wrong.\n")
    
    # handle file extension
    if len(filename.split(".")) > 1:
        filename = filename.split(".")[0]
    
    # convert the datetime in email to python's datetime
    if filename is None: 
        filename = parsedate_to_datetime(message["date"])
    
    with open(f"{folder_name}/{filename}.{ext_name}", "w", encoding="UTF-8") as file:
        file.write(message.as_string())


def save_mbox_as_eml(mbox_path: str, path_to_save="."):
    # handle exception
    if not isinstance(mbox_path, str):
        raise TypeError("The passing object is not a instance of str.\n")
    
    for index, message in enumerate(mailbox.mbox(mbox_path), 1):
        folder_name = re.search(r"\d\d\d\d-\d\d", mbox_path).group()
        eml_filename = folder_name + "-%s" % index

        # create the output directories if it doesn't exist 
        while not os.path.exists(f"{path_to_save}/{folder_name}/"):
            os.makedirs(f"{path_to_save}/{folder_name}/", exist_ok=True)

        save_message_as(message, folder_name=folder_name, filename=eml_filename, ext_name="eml")


def mboxtoeml_main():
    mbox_filenames = [file.name for file in pathlib.Path(data_dir).iterdir()]
    mbox_filename = f"{data_dir}/2013-05.mbox"
    
    # extract the tarfile
    if not pathlib.Path(data_dir).exists():
        extract_tarfile(tar_file)

    # convert mbox to emls to directed dir
    save_mbox_as_eml(mbox_filename)
    



if __name__ == "__main__":
    mboxtoeml_main()