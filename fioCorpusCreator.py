#!/usr/bin/env python
""" ----------------- creates simple xml file corpus from specified web address ---------------- """
""" ----------------- specially designed for fio news ------------------------------------------ """
""" ----------------- input: filename for output ----------------------------------------------- """
from urllib import urlopen
import sys, re

datePattern = "<p class=[\'\"]meta[\'\"]>([\s\S]*?)</p>"
authorPattern = "<p class=[\'\"]podpis[\'\"]>([\s\S]*?)<a href"
headlinePattern = "<h1>(.*)</h1>"
perexPattern = "<p class=[\'\"]perex[\'\"]>([\s\S]*?)</p>"
textPattern = "<p><p>([\s\S]*)<p class=[\'\"]podpis[\'\"]>"
    
def getHyperlinks(link):
    print "Getting hyperlinks from " + link
    webLinkRe = "<h6><a href=\"([\s\S]*?)\".*?>"
    siteContent = urlopen(link).read()
    return re.findall(webLinkRe, siteContent)
    
def getPatternMatch(pattern, text):
    try:
        result = re.search(pattern, text)
        return result.group(1)
    except:
        return ""
        
def processText(text):
    text_htmlStripped = re.sub("<[^<]+?>", " ", text)
    #.strip().replace("&amp;", "&").replace("&quot;", "\"")
    return re.sub("[ ]+", " ", text_htmlStripped.replace("\r\n", " ").replace("\n", " ").strip().decode('windows-1250', errors='replace').encode('utf-8', errors='replace'))
        
def readArticle(pageContent, link):
    item = {'link' : link}
    item.update({'date' : processText(getPatternMatch(datePattern, pageContent))})
    item.update({'headline' : processText(getPatternMatch(headlinePattern, pageContent))})
    item.update({'perex' : processText(getPatternMatch(perexPattern, pageContent))})
    item.update({'content' : processText(getPatternMatch(textPattern, pageContent))})
    item.update({'author' : processText(getPatternMatch(authorPattern, pageContent))})
    if item['content'].find('Zdroj:') > -1:
        item.update({'source' : item['content'][item['content'].find('Zdroj:')+7:]})
        item['content'] = item['content'][:item['content'].find('Zdroj:')].strip()
    else:
        item.update({'source' : ''})  
    return item      
    
def crawlWebPage(link, max_count):
    links = []
    i = 0
    while i < max_count:
        for l in getHyperlinks(link + "?offset=" + str(i)):
            links.append("http://www.fio.cz" + l)
        i = i + 12
    articles = []
    if links:
        for link in list(set(links)):
            print "Getting content from " + link
            try:
                page = urlopen(link)
                pageContent = page.read()
                articles.append(readArticle(pageContent, link))
            except IOError as e:
                print "I/O error {0} : {1}".format(e.errno, e.strerror)
    return articles                
    
def createXmlCorpus(link, out):
    out.write("<?xml version=\"1.0\"?>\n")
    out.write("<corpus page=\""+link+"\">\n")
    for entry in crawlWebPage(link, 50):
        out.write("<article address=\""+entry['link']+"\">\n")
        out.write("<headline>"+entry['headline']+"</headline>\n")
        if entry['date'] != '':
            out.write("<date>"+entry['date']+"</date>\n") 
        if entry['perex'] != '':             
            out.write("<perex>"+entry['perex']+"</perex>\n")
        if entry['content'] != '':        
            out.write("<content>"+entry['content']+"</content>\n") 
        if entry['author'] != '':        
            out.write("<author>"+entry['author']+"</author>\n")  
        if entry['source'] != '':        
            out.write("<source>"+entry['source']+"</source>\n")             
        out.write("</article>\n")
    out.write("</corpus>")
    
def getTexts(link, max_count, directory):
    i = 1
    for entry in crawlWebPage(link, max_count):
        f = open(directory + "/" + str(i).rjust(3, '0') + '.txt', 'w')
        f.write(entry['headline'] + '. ')
        if entry['perex'] != '':             
            f.write(entry['perex'])
        if entry['content'] != '':        
            f.write(entry['content'])
        i += 1
        f.close()
        
#f = sys.stdout
#if len(sys.argv) >= 2:
#    f = open(sys.argv[1].strip(), 'w')        
#print createXmlCorpus('http://www.fio.cz/zpravodajstvi/novinky-z-burzy-komentare', f)
#print createXmlCorpus('http://www.fio.cz/zpravodajstvi/zpravy-z-burzy', f)
#f.close()

getTexts(sys.argv[1].strip(), int(sys.argv[2]), sys.argv[3].strip())