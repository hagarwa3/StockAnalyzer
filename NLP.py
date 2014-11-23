import urllib2
from bs4 import BeautifulSoup
#names=["GPS", "NFLX", "CAT", "ROST", "ADSK", "STJ", "GME", "DAL", "BAC", "ATI", "LUV", "GRPN", "INTC", "AAPL", "MOLG", "WAIR", "OTIV", "AMDA", "ARUN", "ICLDW", "AAPL", "GOOG", "BABA"]

def calc(names):
    for i in names:
        url = 'http://finance.yahoo.com/q?s='+i
        data = urllib2.urlopen(url)
        soup = BeautifulSoup(data)
        
        divs = soup.find('div',attrs={'id':'yfi_headlines'})
        div = divs.find('div',attrs={'class':'bd'})
        ul = div.find('ul')
        lis = ul.findAll('li')
        print i
        m=0.0
        for li in lis:
            headlines = li.find('a').get('href')
            #print headlines
            ur='http://access.alchemyapi.com/calls/url/URLGetTextSentiment?apikey=9b61009a54069badce0cc7ed6bc3f229b07d150a&url='+headlines
            dat=urllib2.urlopen(ur)
            sou=BeautifulSoup(dat)
            if sou.find('score')!=None:
                m+=float(sou.find('score').string)
        return m