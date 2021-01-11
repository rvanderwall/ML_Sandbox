from lxml import html
import requests
import re
import urllib.request
import shutil


def scrape_guten(out_text):
    url = 'https://www.gutenberg.org/ebooks/1727'
    mainWebsite = "https://www.gutenberg.org/"

    page = requests.get(url)
    tree = html.fromstring(page.content)
    links = re.findall('a href="(.*.txt)"', page.text)

    for l in links:
        fileurl = mainWebsite + l
        print(fileurl)
        with urllib.request.urlopen(fileurl) as response, open(out_text, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            break


