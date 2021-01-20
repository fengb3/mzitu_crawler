import os

from bs4 import BeautifulSoup
import requests
import csv
import progressbar
import time
import random

def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

url_list = []
nav_page_nums = 0;

def get_page_number():
    page_url = 'https://www.mzitu.com/'
    html_text = requests.get(page_url, headers = get_headers()).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for x in soup.body.find_all('a', attrs = {'class' : 'page-numbers'}):
        if(is_number(x.text) and int(x.text)>=200):
            return int(x.text)

# check numeric string
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

# get urls for each nav page
def get_subpage_url(page_url):
    html_text = requests.get(page_url, headers = get_headers()).text
    soup = BeautifulSoup(html_text,'html.parser')
    for x in soup.body.find_all('ul', attrs = {"id" : "pins"}):
        for y in x.find_all('li'):
            curr_duct = {}
            curr_duct['text'] = str(y.span.text)
            curr_duct['url'] = str(y.a.get('href'))
            url_list.append(curr_duct)

# write to csv
def write_csv(url_list):
    with open("urls.csv", 'w', newline="\n") as csvfile:
        fieldnames = ['text', 'url']
        spamwrite = csv.DictWriter(csvfile, fieldnames=fieldnames)
        spamwrite.writeheader()
        for x in url_list:
            # print(x)
            spamwrite.writerow(x)

bar = progressbar.ProgressBar(
    widgets = [
        progressbar.Percentage(),
        ' (', progressbar.SimpleProgress(), ') ',
        progressbar.Bar(), ' ',
        progressbar.ETA()
    ]
)

nav_page_nums = get_page_number()

print("getting "+str(nav_page_nums)+" detail pages")

for i in bar(range(1, nav_page_nums)):
    get_subpage_url("https://www.mzitu.com/page/"+str(i)+"/")
    time.sleep(random.randint(0,3)) 

write_csv(url_list)