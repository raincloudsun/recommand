#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, json
import requests #from urllib.request import urlopen
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

reload(sys)
sys.setdefaultencoding('utf-8')
twitter = Twitter()
store = {}

'''
Cosine Similarity
'''
def vector_inner_product(a, b):
    s = 0
    for i in range(len(a)):
        s += (a[i]*b[i])
    return s

def vector_size(v):
    s = 0
    for i in range(len(v)):
        s += v[i]**2
    return s**0.5

def cosine_similarity(a, b):
    numerator = vector_inner_product(a,b)
    denominator = vector_size(a) * vector_size(b)
    print( "> numerator   : %.10f" % numerator )
    print( "> denominator : %.10f" % denominator )
    return numerator/denominator

'''
Crawling & Word Frequency
'''
def crawling(source):
    html = requests.get(source['url']).content
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    return soup.find_all(name=source['name'], attrs=source['attr'])

def setVector(docs):
    dic = {}
    for docs_index in range(len(docs)):
        doc = docs[docs_index].get_text()
        print json.dumps(doc,ensure_ascii=False)

        words=twitter.nouns(doc)

        for i in range(len(words)):
            value = dic.get(words[i])
            if value == None:
                dic[words[i]] = 1 
            else:
                dic[words[i]] = value + 1

    return dic

def documentsSimilarity(srcList, p):
    for i in range(len(srcList)):
        docs = crawling(srcList[i])
        store[i] = setVector(docs)

    r = 0
    score = {}
    score[p] = store[p].values()

    print "\n*** Score Calculation ***"

    for i in range(len(store)):
        score[i] = []
        dic = store[i]
        for k in store[p]:
            v = dic.get(k)
            if v == None:
                score[i].append(0)
            else:
                score[i].append(v)

        r = cosine_similarity(score[p], score[i])

        #print score[i]
        #print "\n"
        print "%d : %d = sim(%.10f)" % (p,i,r)

if __name__ == "__main__":
    documents = [
        {'url' : "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=008&aid=0004159617",
         'name': "div",
         'attr': {"id":"articleBodyContents"}},
        {'url' : "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=119&aid=0002305457",
         'name': "div",
         'attr': {"id":"articleBodyContents"}},
        {'url' : "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=138&aid=0002069244",
         'name':"div",
         'attr': {"id":"articleBodyContents"}},
        {'url' : "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=366&aid=0000424453",
         'name':"div",
         'attr': {"id":"articleBodyContents"}},
        {'url' : "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=014&aid=0004159362",
         'name':"div",
         'attr': {"id":"articleBodyContents"}}
    ]

    documentsSimilarity(documents, 0)

# End of File
