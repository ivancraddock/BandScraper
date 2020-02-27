import pyperclip
import requests
from bs4 import BeautifulSoup
import os
import urllib.request


url_string = pyperclip.paste()

if "http" not in url_string:
    exit()

res = requests.get(url_string)

src = res.content

soup = BeautifulSoup(src,'html.parser')

folder = soup.title.string
pwd = dir_path = os.path.dirname(os.path.realpath(__file__))

if os.path.isdir(folder):
    print(f"ALBUM ALREADY IN DESTINATION DIRECTORY: {pwd}/{folder}")
    exit()

os.mkdir(folder)

links = soup.find_all("script")

for i in links:
    if "trackinfo: [{" in str(i):
        for j in str(i).split("\n"):
            if "trackinfo: [{" in j:
                json_object = j
                break
        break

json_array = json_object[2:-2].split(",")

url_dict = {}
address,title = None,None
for i in json_array:
    
    if i[:6] == '"file"':
        address = i.split('"mp3-128":')[1][1:-2]
    if i[:7] == '"title"':
        title = i.split(":",1)[1][1:-1]
    if address != None and title != None:
        url_dict[title] = str(address)
        address,title = None,None
    

for i in url_dict.keys():
    print(f"downloading {i}")
    urllib.request.urlretrieve(url_dict[i], f'{folder}/{i}')


