import urllib2
from bs4 import BeautifulSoup
url = 'http://en.wikipedia.org/w/index.php?title=Category:B-Class_articles&from=A'

conn = urllib2.urlopen(url)
html = conn.read()

soup = BeautifulSoup(html)
links = soup.find_all('a')

for tag in links:
    link = tag.get('href',None)
    if link != None:
        print link