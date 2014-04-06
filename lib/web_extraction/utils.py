# -*- coding: utf-8 -*-

from urllib import urlopen
import re

DATE_PATTERN = re.compile("<p class=[\'\"]meta[\'\"]>([\s\S]*?)</p>")
AUTHOR_PATTERN = re.compile("<p class=[\'\"]podpis[\'\"]>([\s\S]*?)<a href")
HEADLINE_PATTERN = re.compile("<h1>(.*)</h1>")
PEREX_PATTERN = re.compile("<p class=[\'\"]perex[\'\"]>([\s\S]*?)</p>")
TEXT_PATTERN = re.compile("<p><p>([\s\S]*)<p class=[\'\"]podpis[\'\"]>")
WEB_LINK = re.compile("<h6><a href=\"([\s\S]*?)\".*?>")

def getPatternMatch(pattern, text):
    try:
        result = pattern.search(text)
        return result.group(1)
    except:
        return ""
    
def processText(text):
    text_htmlStripped = re.sub("<[^<]+?>", " ", text.replace("</p>", ".")) # if there is one sentence per paragraph and which is not delimited by '.'
    return re.sub("[ ]+", " ", text_htmlStripped.replace("\r\n", " ").replace("&amp;", "&").replace("&quot;", "\"").replace("„","\"").replace("“", "\"").replace("�", "\"").replace("\n", " ").replace(". .", ". ").replace('..', '.').strip().decode('windows-1250', errors='replace').encode('utf-8', errors='replace'))

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

def getHyperlinks(link):
    print "Getting hyperlinks from " + link
    siteContent = urlopen(link).read()
    return WEB_LINK.findall(siteContent)

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
    # out.write('Dátum ' + parsedPage['date'] + '.\n')
    out.write(parsedPage['headline'].replace("&amp;", "&").replace("„","\"").replace("“", "\"").replace("&quot;", "\"").replace("�", "\"")+".\n")
    if parsedPage['perex'] != '':
        out.write(parsedPage['perex'].replace("&amp;", "&").replace("„","\"").replace("“", "\"").replace("&quot;", "\"").replace("�", "\"")+"\n")
    if parsedPage['content'] != '':
        out.write(parsedPage['content'].replace("&amp;", "&").replace("„","\"").replace("“", "\"").replace("&quot;", "\"").replace("�", "\"")+"\n")
        
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
    
def createTextCorpora(link, max_count, directory):
    i = 1
    for entry in crawlWebPage(link, max_count):
        f = open(directory + "/" + str(i).rjust(3, '0') + '.txt', 'w')
        f.write('Dátum ' + entry['date'] + '.\n')
        f.write(entry['headline'] + '. ')
        if entry['perex'] != '':             
            f.write(entry['perex'])
        if entry['content'] != '':        
            f.write(entry['content'])
        i += 1
        f.close()