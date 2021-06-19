import sys
import os
import requests

from bs4 import BeautifulSoup

def path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def last_version():
    r = requests.get("https://github.com/INIRU/LOL_PW/releases")
    soup = BeautifulSoup(r.content, "html.parser")
    return soup.find_all(attrs={'class': 'css-truncate-target'}, style="max-width: 125px")[0].text