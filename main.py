#!/usr/bin/python
# -*- coding: utf-8 -*-
#from urllib.request import urlopen
import sys, json
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

dic = {}
twitter = Twitter()

url = "http://www.wsobi.com/news/articleView.html?idxno=68588"
html = requests.get(url).content
soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
title = soup.find_all(name="p", attrs={"style":"text-align: justify;"})

for index in range(len(title)):
    doc = title[index].get_text()
    print json.dumps(doc,ensure_ascii=False)
    #print("%d : %s" % (index+1, doc))

    words=twitter.nouns(doc)
    #print json.dumps(words,ensure_ascii=False)

    for i in range(len(words)):
        value = dic.get(words[i])
        if value == None:
            dic[words[i]] = 1 
        else:
            dic[words[i]] = value + 1

print "\n*** Score Calculation ***"
print json.dumps(dic,ensure_ascii=False)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
