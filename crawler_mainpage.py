import os

from bs4 import BeautifulSoup
import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

page_url = 'https://www.mzitu.com/'

html_text = requests.get(page_url, headers = headers).text

soup = BeautifulSoup(html_text, 'html.parser')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

for x in soup.body.find_all('a', attrs = {'class' : 'page-numbers'}):
    if(is_number(x.text) and float(x.text)>=200):
        print(x.text)