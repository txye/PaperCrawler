import requests
from bs4 import BeautifulSoup
import os
import urllib

def get_url():
    conferences = ['acl', 'tacl', 'naacl', 'emnlp']
    years = ['2018', '2017', '2016', '2015']
    url_list = []
    root = "https://aclanthology.coli.uni-saarland.de"
    for conf in conferences:
        for year in years:
            url = os.path.join(root, 'events/' + conf + '-' + year)
            url_list.append(url)
    return url_list

def satisfy_condition(title, keywords):
    for kw in keywords:
        if kw.lower() in title.lower():
            return True
    return False

def download_store(url, path):
    data = urllib.urlopen(url).read()
    with open(path, 'wb') as fw:
        fw.write(data)

def get_paper(url_list, keywords):
    for url in url_list:
        r = requests.get(url)
        if r.ok:
            html = r.content
            soup = BeautifulSoup(html,'html.parser')
            paper_div = soup.find('div', attrs={'class': 'span12'})
            p_s = paper_div.find_all('p')
            for p in p_s:
                a_s = p.find_all('a')
                pdf_a = a_s[0]
                title = p.find('strong').find('a').get_text()
                paper_url = pdf_a.get('href')
                print(title)
                if satisfy_condition(title, keywords):
                    store_path = os.path.join('.', url.split('/')[-1])
                    if not os.path.exists(store_path):
                        os.mkdir(store_path)
                    store_path = os.path.join(store_path, title + '.pdf')
                    download_store(paper_url, store_path)

if __name__ == "__main__":
    url_list = get_url()
    get_paper(url_list, ['classification', 'text representation'])

