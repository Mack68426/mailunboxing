import email
from email.parser import Parser

file_path = '/home/yuhong/www.ietf.org/ietf-ftp/ietf-mail-archive/ipv6/2003-09.mail'
try:
    with open(file_path, 'r', encoding="utf-8") as file:
        # 讀取檔案內容
        file_content = file.read()
        print(f"File Content:\n{file_content}")
except FileNotFoundError:
    print(f"File not found at path: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")