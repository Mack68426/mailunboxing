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

proj_dir = os.path.dirname(__file__)
path_to_extract = "/mails/"

def dir_empty(dir_name):
    if not os.path.exists(dir_name) or not len(os.listdir(dir_name)):
        return True
    else:
        return 
    

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
def parse_mbox(mbox_name):
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
    

# def get_body_from_file(message: Message, encoding = "utf-8"):
#     msg_content = None
#     all_content_type = set()
#     if message.is_multipart():
#         for part in message.walk():
#             content_type = part.get_content_type()

#             all_content_type.add(content_type)
            
#             # skip the text/plain attachment
#             if content_type in ["text/plain", "text/html"] and \
#             not part.get_content_disposition() == "attachment":
#                 msg_content = part.get_payload(decode=True)
#                 break
    
#     # not multipart
#     else:
#         msg_content = message.get_payload(decode=True)
#         all_content_type.add(message.get_content_type())
    
#     print("All the Content-Type in the mbox file", all_content_type)

#     return msg_content.decode(encoding=encoding)



def mbox_to_eml(mbox_filename, out_dir):
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    # export the mbox messages to each .eml file
    mbox_pattern = re.compile(r"\d\d\d\d-\d\d")
    gen = Generator(mbox_filename)
    

def main():
    list_name = '6lo'
    tar_file = 'mbox0122_ast_b.tar.gz'
    data_dir = tar_file[:-7] + "/" + list_name

    

    # extract the tarfile
    if not pathlib.Path(data_dir).exists():
        extract_tarfile(tar_file)

    mbox_name = f"{data_dir}/2013-05.mbox"

    # parse the content in mbox file 
    for m in parse_mbox(mbox_name):
        print("message body:")
        print(m.get("content"))
    
    # mbox_files = []
    # count = 0
    # for file in pathlib.Path(data_dir).iterdir(): # iterate all .mbox files and 
    #     if count > 5:
    #         break
        
    #     print("File name:", file.name)
    #     parse_mbox(file)

    #     count += 1


if __name__ == "__main__":
    main()