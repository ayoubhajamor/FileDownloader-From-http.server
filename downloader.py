import os
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def createFile(path , data, name):
    if "text" in data.headers['Content-type']:
        with open(path / name, 'w') as f:
            f.write(data.text)
    else:
        with open(path / name, 'wb') as f:
            f.write(data.content)
    print(f"{path}/{name} created.")

def getFilesAndDirs(html):
    soup = BeautifulSoup(html, 'html.parser')
    files = []
    dirs = []
    for a in soup.find_all('a'):
        if a['href'].endswith('/'):
            dirs.append(a['href'])
        else:
            files.append(a['href'])
    return files, dirs

def getFile(url, name):
    return requests.get(f"{url}/{name}")

p = Path(os.getcwd())
DownloadP = p / "Downloaded"
# Make the directory that files will be downloaded into
os.makedirs(DownloadP, exist_ok=True)

if len(sys.argv) <= 2:
    print(f"Usage : {sys.argv[0]} <host> <port>")
    sys.exit()

host, port = sys.argv[1], sys.argv[2]
url = f"http://{host}:{port}"
r = requests.get(url)

if r.status_code != 200:
    print("Something went wrong !")
    print(f"Status code {r.status_code}")
    sys.exit()

html_doc = r.text

files, dirs = getFilesAndDirs(html_doc)


while True:
    while files != []:
        name = files.pop()
        data = getFile(url, name)
        createFile(DownloadP , data, name)

    # TODO: Go inside each dir and download all its files
    break


