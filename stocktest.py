import urllib2
from datetime import datetime, timedelta
import numpy
import mailjet
import requests
from requests.auth import HTTPBasicAuth
import os
import NLP

mailjet_api = mailjet.Api(api_key='bbbb2a82e844e6e6a8e68819b34bfa55', secret_key='a351a09703c3cce4c51308d301254f02')
payload = {"from":"nrsheth2@illinois.edu", "to":"niharrsheth@gmail.com", "subject":"Current Stock Information"}

today = datetime.now()
degree = 4
stockList = ["YHOO", "CAT", "GOOG", "BABA", "STJ", "INTC", "BAC", "ATI", "LUV", "GRPN", "WAIR", "OTIV", "AMDA", "ICLDW", "FB"]

rangevar = 5

successes = {}

d = str(today.month - 1).zfill(2)
e = str(today.day - 2).zfill(2)
f = str(today.year)

pastDate = today - timedelta(days=7)
a = str(pastDate.month - 1).zfill(2)
b = str(pastDate.day - 2).zfill(2)
c = str(pastDate.year)
positives = ""
for m in stockList:
    data = urllib2.urlopen("http://ichart.finance.yahoo.com/table.csv?s="+m+"&a="+a+"&b="+b+"&c="+c+"&d="+d+"&e="+e+"&f="+f+"&g=d&ignore=.csv")
        
    data.readline()
    data.readline()
    info = []
    yvalues = []
    for j,i in enumerate(data.readlines()):
        #print i
        info = i.split(",")
        yvalues.append(float(info[4])-float(info[1]))
    
    coeff = numpy.polyfit(range(rangevar)[::-1], yvalues, degree)
    print coeff
    NLPVal = NLP.calc([m])
    print NLPVal
    blah = coeff[0]*rangevar**4 + coeff[1]*rangevar**3 + coeff[2]*rangevar**2 + coeff[3]*rangevar + coeff[4]
    if blah>0:
        positives += m+" "
        successes[m] = blah/float(info[4])*100*(1+NLPVal)
        print "val:", successes[m]
    #print blah
    print m, blah/float(info[4])*100
t = sorted(successes, key=successes.get, reverse=True)
print t
positives = ""
for i in xrange(3): positives += t[i] + " "
requests.get("https://api.mailjet.com/v3/send", auth=HTTPBasicAuth('bbbb2a82e844e6e6a8e68819b34bfa55', 'a351a09703c3cce4c51308d301254f02'), params=payload)
#os.system('curl --user "bbbb2a82e844e6e6a8e68819b34bfa55:a351a09703c3cce4c51308d301254f02" https://api.mailjet.com/v3/send -F from="nrsheth2@illinois.edu" -F to="niharrsheth@gmail.com" -F subject="Hai" -F text="'+positives+'"')