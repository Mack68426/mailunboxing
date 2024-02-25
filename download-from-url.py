# OBJECTIVE:
#   download email files from `ietf.org/ietf-ftp/ietf-mail-archive/` through HTTP
import mailbox
import pathlib
import re
import os
import requests
from bs4 import BeautifulSoup

baseurl = "https://www.ietf.org/ietf-ftp/ietf-mail-archive/6lo/"
headers = {"User-Agent" : "Mozilla/5.0"}
list_name = "6lo"
out_dir = "FTP/6lo/"


# the converter converting `.mail` file to `.eml` files
def mail_to_eml(mailfile_path, out_dir='.', exist_ok = False) -> None:

    # new folder built by mbox filename
    folder_name = re.search(r"\d\d\d\d-\d\d", mailfile_path).group()

    # create folders to store email files by mbox
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(f"{out_dir}/{folder_name}", exist_ok=True)
    if not exist_ok:
        # read the .mbox file and split it
        for index, message in enumerate(mailbox.mbox(mailfile_path), 1):
            eml_filename = f"{out_dir}/{folder_name}/{folder_name}-{index}.eml"
            
            # create email files one by one 
            with open(eml_filename, "w+", encoding="UTF-8") as file:
                file.write(message.as_string())


def download_from_url(url):
    os.makedirs(out_dir, exist_ok=True)
    
    page = requests.get(f"{url}", headers=headers)
    
    for file_date in re.findall(r"\d\d\d\d-\d\d", page.text):
        response = requests.get(f"{url}{file_date}.mail", headers=headers, stream=True)

        with open(f"{out_dir}/{file_date}.mail", "w+") as file:
            file.write(response.text)

def main() -> None:

    # download email files from url under the "ietf.org" domain to disk
    download_from_url(baseurl)


if __name__ == "__main__":
    main()