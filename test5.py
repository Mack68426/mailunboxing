import os
import re
import tarfile
import mailbox
import pathlib
from email.message import Message
from email.parser import BytesParser
from email.policy import default

proj_dir = os.path.dirname(__file__)

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

def parse_mbox(mbox_file):
    for message in mailbox.mbox(mbox_file):
        print(message)

def mbox_to_eml(mbox_file, out_dir):
    pass

def main():
    list_name = '6lo'
    tar_file = 'data/mbox0122_ast_b.tar.gz'
    data_dir = tar_file[:-7] + "/" + list_name

    # extract the tarfile if the directory does not exist
    if not pathlib.Path(data_dir).exists():
        extract_tarfile(tar_file)

    for file in os.listdir(data_dir):
        parse_mbox(file)
    
    # count = 0
    # for m in mails:
    #     if count > 3:
    #         break
    #     print(m)

    #     count+=1

if __name__ == "__main__":
    main()