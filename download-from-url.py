# download email files from `ietf.org/ietf-ftp/ietf-mail-archive/` through HTTP
import re
import os
import requests

baseurl = "https://www.ietf.org/ietf-ftp/ietf-mail-archive/6lo/"
headers = {"User-Agent" : "Mozilla/5.0"}
dir = "FTP/6lo/"

response = requests.get(f"{baseurl}", headers=headers)

os.makedirs(dir, exist_ok=True)

for date in re.findall("\d\d\d\d-\d\d", response.text):
    
    with open(f"{dir}/6lo_{date}.eml", "w+") as file:
        file.write(response.text)