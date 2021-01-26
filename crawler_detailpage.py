import os

from bs4 import BeautifulSoup
import requests
import csv
import progressbar
import time
import random

page_dict = {}
path = '/home/bohan/Pictures/mzitu/'

def get_headers():
    '''
    随机获取一个headers
    '''
    user_agents =  ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    headers = {'User-Agent':random.choice(user_agents)}
    return headers

def get_img_headers():
    '''
    get headers with img referer
    '''
    headers = {}
    headers = get_headers()
    headers['Referer'] = 'https://www.mzitu.com/'
    return headers


# read page contents
def read_info(page_url):
    page_dict = {}
    html_text = requests.get(page_url, headers = get_headers()).text
    soup = BeautifulSoup(html_text, 'html.parser')

    for x in soup.body.find_all('div', attrs = {'class' : 'pagenavi'}):
        for a in x.find_all('a'):
            if(is_number(a.text) and int(a.text) >4):
                page_dict['max_page'] = int(a.text)

    for t in soup.body.find_all('div', attrs = {'class' : 'main-tags'}):
        tags = []
        for a in t.find_all('a'):
            tags.append(a.text)
        page_dict['tags'] = tags

    return page_dict

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

def get_imgurl(page_url):
    html_text = requests.get(page_url, headers = get_headers()).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for x in soup.body.find_all('img', attrs = {'class' : 'blur'}):
        return str(x['src'])

def get_imgcontent(img_url):
    return requests.get(img_url, headers = get_img_headers()).content

def dowload_image(url, info, title):
    print("Dowloading " + title)
    for page_num in bar(range(1, info['max_page']+1)):
        f = open(path + '/' + title + '/img' + str(page_num), 'wb')
        img_url = get_imgurl(url + '/' + str(page_num))
        f.write(get_imgcontent(img_url))
        f.close()
        time.sleep(random.randint(0,3))


with open('urls.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter = ',')
    count = 0
    for row in reader:
        bar = progressbar.ProgressBar(
            widgets = [
                progressbar.Percentage(),
                ' (', progressbar.SimpleProgress(), ') ',
                progressbar.Bar(), ' ',
                progressbar.ETA()
            ]
        )
        if count < 11 and count > 5:
            if(os.path.exists(path + row[0].replace('?', ''))):
                print('catalog exist', count)
            else:
                os.mkdir(path + row[0].replace('?', ''), 0o755)
            f = open(path + row[0].replace('?', '') + '/index', 'w')
            f.write(str(row[1]) + '\n')
            info = read_info(row[1])
            f.write(str(info['max_page']) + '\n')
            f.write(','.join(info['tags']))
            f.close()
            dowload_image(row[1], info, row[0])
        count += 1

'''
page_dict = read_info('https://www.mzitu.com/252276')
for page_num in range(1, page_dict['max_page']):  
    f = open('img' + str(page_num), 'wb')
    img_url = get_imgurl('https://www.mzitu.com/252276/' + str(page_num))
    f.write(get_imgcontent(img_url))
    f.close()
    time.sleep(random.randint(0,3))
'''


