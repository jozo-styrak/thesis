#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
import sys, re

DATE_PATTERN = re.compile("<p class=[\'\"]meta[\'\"]>([\s\S]*?)</p>")
AUTHOR_PATTERN = re.compile("<p class=[\'\"]podpis[\'\"]>([\s\S]*?)<a href")
HEADLINE_PATTERN = re.compile("<h1>(.*)</h1>")
PEREX_PATTERN = re.compile("<p class=[\'\"]perex[\'\"]>([\s\S]*?)</p>")
TEXT_PATTERN = re.compile("<p><p>([\s\S]*)<p class=[\'\"]podpis[\'\"]>")

def getPatternMatch(pattern, text):
    try:
        result = pattern.search(text)
        return result.group(1)
    except:
        return ""
        
def processText(text):
    text_htmlStripped = re.sub("<[^<]+?>", " ", text.replace("</p>", ".")) # if there is one sentence per paragraph and which is not delimited by '.'
    return re.sub("[ ]+", " ", text_htmlStripped.replace("\r\n", " ").replace("\n", " ").replace(". .", ". ").replace('..', '.').strip().decode('windows-1250', errors='replace').encode('utf-8', errors='replace'))
    
def readArticle(pageContent, link):
    item = {'link' : link}
    item.update({'date' : processText(getPatternMatch(DATE_PATTERN, pageContent))})
    item.update({'headline' : processText(getPatternMatch(HEADLINE_PATTERN, pageContent))})
    item.update({'perex' : processText(getPatternMatch(PEREX_PATTERN, pageContent))})
    item.update({'content' : processText(getPatternMatch(TEXT_PATTERN, pageContent))})
    item.update({'author' : processText(getPatternMatch(AUTHOR_PATTERN, pageContent))})
    if item['content'].find('Zdroj:') > -1:
        item.update({'source' : item['content'][item['content'].find('Zdroj:')+7:]})
        item['content'] = item['content'][:item['content'].find('Zdroj:')].strip()
    else:
        item.update({'source' : ''})  
    return item	

def getXmlPage(parsedPage, out):
    out.write("<?xml version=\"1.0\"?>\n")
    out.write("<article address=\""+parsedPage['link']+"\">\n")
    out.write("<headline>"+parsedPage['headline']+".</headline>\n")
    if parsedPage['date'] != '':
        out.write("<date>"+parsedPage['date']+"</date>\n") 
    if parsedPage['perex'] != '':
        out.write("<perex>"+parsedPage['perex']+"</perex>\n")
    if parsedPage['content'] != '':
        out.write("<content>"+parsedPage['content']+"</content>\n") 
    if parsedPage['author'] != '':
        out.write("<author>"+parsedPage['author']+"</author>\n")
    if parsedPage['source'] != '':
        out.write("<source>"+parsedPage['source']+"</source>\n")
    out.write("</article>\n")

def getTextPage(parsedPage, out):
    out.write(parsedPage['headline'].replace("&amp;", "&").replace("&quot;", "\"").replace("„", "\"")+".\n")
    if parsedPage['perex'] != '':
        out.write(parsedPage['perex'].replace("&amp;", "&").replace("&quot;", "\"").replace("„", "\"")+"\n")
    if parsedPage['content'] != '':
        out.write(parsedPage['content'].replace("&amp;", "&").replace("&quot;", "\"").replace("„", "\"")+"\n")

xmlOutput = True
if (len(sys.argv) == 3) and (sys.argv[2] == "text"):
    xmlOutput = False

if xmlOutput:
    getXmlPage(readArticle(urlopen(sys.argv[1]).read(), sys.argv[1]), sys.stdout)
else:
    getTextPage(readArticle(urlopen(sys.argv[1]).read(), sys.argv[1]), sys.stdout)