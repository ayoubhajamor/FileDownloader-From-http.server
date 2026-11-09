import os
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def createFile(data, a):
    if "text" in data.headers['Content-type']:
        with open(a['href'], 'w') as f:
            f.write(data.text)
    else:
        with open(a['href'], 'wb') as f:
            f.write(data.content)
    print(f"{a['href']} created.")

p = Path(os.getcwd())
DownloadP = p / "Downloaded"
# Make the directory that files will be downloaded into
os.makedirs(DownloadP, exist_ok=True)
# cd 
os.chdir(DownloadP)

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
soup = BeautifulSoup(html_doc, 'html.parser')

for a in soup.find_all('a'):
    data = requests.get(f"{url}/{a['href']}")
    createFile(data, a)
