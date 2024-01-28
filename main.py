import os
import re
import tarfile

import mailbox
from email.utils import parsedate_to_datetime

# TODO: make a same tool in command line with `csplit` command

project_dir = os.path.dirname(__file__)

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


# converting one mbox file to emls files to target dir
def main():
    list_name = '6lo'
    resource_dir = "resource" # store extracted data
    mailbox_dir = "emails" # store .eml files dsorted by mbox
    tar_file = 'mbox0122_ast_b.tar.gz'
    tar_path = f"{resource_dir}/{tar_file}"
    
    test_mbox_file_path = f"{resource_dir}/{tar_file[:-7]}/{list_name}/2013-05.mbox"

    extract_tarfile(tar_path, resource_dir)
    
    mbox_to_eml(test_mbox_file_path, out_dir=f"{mailbox_dir}/{list_name}")


def read_tar_main():
    list_name = "6lo"
    resource_dir = "resource" # store extracted data
    tar_file = 'mbox0122_ast_b.tar.gz'
    tar_path = f"{resource_dir}/{tar_file}"

    
    with tarfile.open(tar_path, "r:gz") as tar:
        # tar.list(verbose=False) # ${tarFilename}/${emailListName}/YYYY-mm.mbox
        
        # get the filename without extension
        outfile_path = re.search("\d\d\d\d-\d\d", member.name).group()
        
        #handle the file extension
        if not outfile_path.endswith(".mbox"):
            outfile_path = outfile_path + ".eml"
        
        # write 
        for member in tar.getmembers():
            mbox_file = open(f"emails/{outfile_path}", "wb")
            mbox_file.write(tar.extractfile(member).read())
            mbox_file.close()
        

if __name__ == "__main__":
    main()