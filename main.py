import os
import re
import mailbox
import tarfile
import pathlib
from email.utils import parsedate_to_datetime


proj_dir = os.path.dirname(__file__)
list_name = '6lo'

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
    


    # close the file
    tar.close()

# the main converter converting `.mbox` file to `.eml` files
def mbox_to_eml(mboxfile_path, out_dir='.') -> None:

    # new folder name built by mbox
    folder_name = re.search(r"\d\d\d\d-\d\d", mboxfile_path).group()

    # read the .mbox file and split it
    for index, message in enumerate(mailbox.mbox(mboxfile_path), 1):

        # create folders to store email files by mbox
        if not os.path.exists(folder_name):
            os.makedirs(f"{out_dir}", exist_ok=True)
        
        # create email files one by one 
        with open(f"{out_dir}/{folder_name}-{index:0d}.eml", "w", encoding="utf-8") as file:
            file.write(message.as_string())


def main():
    data_dirname = "data"
    tar_file = 'mbox0122_ast_b.tar.gz'
    mbox_file_path = f"{data_dirname}/{list_name}/{tar_file[:-7]}/2013-05.mbox" # data\6lo\2013-05.mbox
    mbox_dir = re.search(r"")

    extract_tarfile(tar_file, data_dirname + "/" + list_name + "")

    mbox_to_eml(mbox_file_path, out_dir=f"{data_dirname}/{list_name}/{mbox_file_path}")

main()