from collections.abc import Callable
import os
import re
import tarfile
import mailbox
import pathlib
from email.message import Message, EmailMessage
from email.parser import BytesParser, Parser
from email.policy import default, compat32
from email.generator import Generator
from email.iterators import _structure
#########################################################

# TODO get all the content in the .mbox files.
# TODO convert .mbox to .eml
# TODO split mbox to .eml files in bulk

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
    
# split single .mbox file to multiple .eml files
def split_mbox(mbox_file, out_dir="."):
    message_files = []

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    # export the mbox messages to each .eml file
    mbox_pattern = re.compile(r"\d\d\d\d-\d\d")


    with open(f"{out_dir}", "w") as file:
        gen = Generator(file)
        gen.flatten(mbox_file)



def main():
    tar_file = 'mbox0122_ast_b.tar.gz'
    data_dir = tar_file[:-7] + "/" + list_name
    mbox_name = f"{data_dir}/2013-05.mbox"

    # extract the tarfile
    if not pathlib.Path(data_dir).exists():
        extract_tarfile(tar_file)

    
    
    # mbox_files = []
    # count = 0
    # for file in pathlib.Path(data_dir).iterdir(): # iterate all .mbox files and 
    #     if count > 5:
    #         break

    # mbox_files = []
    # count = 0
    # for file in pathlib.Path(data_dir).iterdir(): # iterate all .mbox files and 
    #     if count > 5:
    #         break

    #     count += 1
    
    #     count += 1


if __name__ == "__main__":
    main()