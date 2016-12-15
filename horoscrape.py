#modified to work without memory issues from travisriddle.com/Scraping-Horoscopes
#This scrapes a ton of horoscopes from the NY Post site.
#
#Alexander Dodson
#2016-12-12
import urllib2
import datetime
import pandas as pd
import requests
import numpy as np
import os
import gc
from bs4 import BeautifulSoup

url = 'http://nypost.com/horoscope/'
signs =['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces']

start = pd.datetime(2013,12,01)
end = datetime.datetime.today()
date_range = pd.date_range(start,end)

def parse_horos(sign):
  text = []
  pub_date = []
  z_sign = []
  for day in date_range:
    print day
    link = url+sign+'-'+day.strftime('%m-%d-%Y')+'/'
    page = requests.get(link)
    if not page.ok:
      continue
    content = urllib2.urlopen(link).read()
    soup = BeautifulSoup(content,'lxml')
    s = soup.find('div','entry-content')
    if s.find('p'):
      x = s.find('p').string
      text.append(x)
      z_sign.append(sign)  
      pub_date.append(day.strftime('%m-%d-%Y'))
    soup.decompose()
    page.close()  
  df = pd.DataFrame({'horoscope' : text, 'zodiac' : z_sign, 'pub_date' : pub_date})
  df.to_csv('horoscopes.csv',mode='a',header=False,sep='|',encoding='utf-8')
  gc.collect()
  
for sign in signs:
  print sign
  parse_horos(sign)
