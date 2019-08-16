
from bs4 import BeautifulSoup
import re
import requests
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from uploadscript import upload_json_to_elastic,text_to_json


def is_alive(url):
    try:
        urlopen(url).read()
    except:
        print("Error with HTTP" + url)
        return False
    return True


# checks if url is a file like PDF
def is_downloadable(url, test_if_alive=True):
    if test_if_alive:
        if not is_alive(url):
            return False
    """
    Does the url contain a downloadable resource
    """

    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


# checks if url is a not a file
def is_webpage(url):
    if is_alive(url):
        return not is_downloadable(url, False)
    else:
        return False


def clean_html(raw_html):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, '', raw_html)
    return clean_text


def url_to_text(url):
    text_list = []
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, "html.parser")
    for node in soup.findAll('p'):
        text = clean_html(str(node))
        text_list.append(text)
    return text_list


def urls_in_page(url):
    text_list = []
    if is_webpage(url):
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc, "html.parser")
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            text_list.extend(link.get('href'))
    return text_list


def upload_url_to_elastic(url, title="html"):
    json_list = []
    if is_webpage(url):
        list = url_to_text(url)
        for p in list:
            json_list.append(text_to_json(p, url, title, False))
        upload_json_to_elastic(json_list)
    #print(json_list)


if __name__ == '__main__':
    urls = ['https://edu.gov.il/minhalpedagogy/olim/Pages/hp.aspx',
            'https://edu.gov.il/minhalpedagogy/olim/Hebrew/Pages/heb-sec-lng.aspx',
            'http://www.yedidut.org.il/absorption',
            'http://www.merage.co.il/?categoryId=106923&itemId=232602',
            'https://www.reutheshel.org.il/%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA-%D7%A2%D7%95%D7%9C%D7%99%D7%9D-%D7%97%D7%93%D7%A9%D7%99%D7%9D-%D7%91%D7%92%D7%99%D7%9C-%D7%96%D7%A7%D7%A0%D7%94/',
            'https://www.calcalist.co.il/money/articles/0,7340,L-3388803,00.html',
            'https://www.rishonlezion.muni.il/Residents/CommunitySports/NewImmigrants/Pages/default.aspx',
            'https://mashkantaguru.co.il/assistance-in-purchasing-an-apartment-for-families-of-immigrants/'
            'https://www.btl.gov.il/ZcuyotAsdience/oleChdash/Pages/default.aspx',
            'https://www.kolzchut.org.il/he/%D7%A1%D7%98%D7%95%D7%93%D7%A0%D7%98%D7%99%D7%9D_%D7%A2%D7%95%D7%9C%D7%99%D7%9D',
            'https://www.kolzchut.org.il/he/%D7%9E%D7%99%D7%9E%D7%95%D7%9F_%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%94%D7%A9%D7%A4%D7%94_%D7%94%D7%A2%D7%91%D7%A8%D7%99%D7%AA_%D7%91%D7%90%D7%95%D7%9C%D7%A4%D7%9F_%D7%9C%D7%A2%D7%95%D7%9C%D7%99%D7%9D_%D7%97%D7%93%D7%A9%D7%99%D7%9D',
            'https://www.kolzchut.org.il/he/%D7%9E%D7%A2%D7%A0%D7%A7_%D7%9B%D7%A1%D7%A4%D7%99_%D7%97%D7%93_%D7%A4%D7%A2%D7%9E%D7%99_%D7%9C%D7%A2%D7%95%D7%9C%D7%99%D7%9D_%D7%95%D7%AA%D7%95%D7%A9%D7%91%D7%99%D7%9D_%D7%97%D7%95%D7%96%D7%A8%D7%99%D7%9D_%D7%94%D7%A0%D7%9E%D7%A6%D7%90%D7%99%D7%9D_%D7%91%D7%9E%D7%A6%D7%91_%D7%A7%D7%A9%D7%94_%D7%90%D7%95_%D7%91%D7%9E%D7%A9%D7%91%D7%A8_(%D7%A2%D7%95%D7%9C%D7%99%D7%9D_%D7%A0%D7%96%D7%A7%D7%A7%D7%99%D7%9D)']

    for url in urls:
        upload_url_to_elastic(url)