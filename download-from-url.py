# download email files from `ietf.org/ietf-ftp/ietf-mail-archive/` through HTTP
import re
import os
import requests
from bs4 import BeautifulSoup

baseurl = "https://www.ietf.org/ietf-ftp/ietf-mail-archive/6lo/"
headers = {"User-Agent" : "Mozilla/5.0"}
dir = "FTP/6lo/"


def download_from_url():
    os.makedirs(dir, exist_ok=True)
    
    page = requests.get(f"{baseurl}", headers=headers)
    
    for file_date in re.findall(r"\d\d\d\d-\d\d", page.text):
        response = requests.get(f"{baseurl}{file_date}.mail", headers=headers, stream=True)

        with open(f"{dir}/{file_date}.eml", "w+") as file:
            file.write(response.text)

if __name__ == "__main__":
    download_from_url()