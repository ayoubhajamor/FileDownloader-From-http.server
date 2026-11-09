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
    print(f"./{path}/{name} created.")

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

def getHtml(url, name):
    return requests.get(f"{url}/{name}").text
def getResponse(url):
    return requests.get(url)

DownloadP = Path('.') / "Downloaded"
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


# Go inside each dir and find all its files
while dirs != []:
    d = dirs.pop()
    data = getHtml(url, d)
    foundFiles, foundDirs = getFilesAndDirs(data)

    # Append foundFiles to files
    for f in foundFiles:
        files.append(d + f)
    for k in foundDirs:
        dirs.append(d + k)

# TODO: Download all files with their respective architecteur
for f in files:
    lf = f.split('/')
    
    # Get filename
    name = lf.pop(-1)
    if len(lf) == 0:
        dpath = ''
    else:
        dpath = '/'.join(lf)
    target_dir = DownloadP / dpath
    # Creating dir
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # cd into target dir
    # os.chdir(target_dir)
    
    # set file url
    if dpath == '':
        file_url = url + '/' + name
    else:
        file_url = url + '/' + dpath + '/' + name

    # Download file
    data = getResponse(file_url)
    
    createFile(target_dir, data, name)
