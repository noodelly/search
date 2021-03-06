from html.parser import HTMLParser
import requests
import os
import sys
import time
from time import perf_counter

class HTMLParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            print("Start tag: ", tag)
            print("Attributes: ", attrs)
            crawl(attrs)
    def handle_data(self, data):
        pass
        #print("Found data: ", data)

def crawl(attrs):
    i = 0
    target = ""
    if "href" not in attrs[i]:
        i = i + 1
    else:
        target = attrs[i][1]
    #Now check to see if the href points to website or subdirectory
    if target[:2] == "//":
        print("SITE FOUND")
        target = "https:" + target
        writer(0, target)
    elif target[:8] == "https://":
        print("HTTPS FOUND")
        writer(0, target)
    elif target[:8] == "HTTPS://":
        print("HTTPS FOUND")
        writer(0, target)
    elif target[:8] == "HTTP://":
        print("HTTP FOUND")
        writer(0, target)
    elif target[:8] == "http://":
        print("HTTP FOUND")
        writer(0, target)
    elif target[:1] == "/":
        print("SUBDIR FOUND")
    elif target[:1] == "#":
        print("IGNORE: IS A IN-PAGE LINK")
        pass
        
def request(seed): 
    parseFlags(seed)
    print(seed)
    perf_start = perf_counter()
    try:
        response = requests.get(seed)
        #writer(3, str(response.content))
        title = getTitle(str(response.content))
        print("GET w/ status code: ", response.status_code)
        parser = HTMLParse()
        parser.feed(str(response.content))
        print("RETURNED SIZE: ", len(response.content) / 1000, "KB")
        writeIndex(title, seed)
        perf_end = perf_counter()
        elapsed = (perf_end - perf_start) * 1000
        writer(2, "[CRAWLED] " + seed +" at " + time.asctime(time.localtime(time.time())) + " (" + str(elapsed) + "ms)")
        #read the uncrawled file
    except:
        #crawled.append(seed)
        print("GET FAIL: HOST COULD NOT BE REACHED")
        print("TRYING NEXT SEED")
        pass

def parseFlags(flags):
    if sys.argv[1] == "-f" and sys.argv[2] == "all":
        flushAllFiles()
    else:
        pass

def flushAllFiles():
    f1 = open("uncrawled.wcf", "w")
    f1.write("")
    f1.close()
    f2 = open("debug.log", "w")
    f2.write("")
    f2.close()
    exit(0)

def getTitle(response):
    title_origin = response.find("<title>")
    title_end = response.find("</title>")
    title = response[title_origin+7:title_end]
    return title

def fetchNextSeed(line):
    file = open("uncrawled.wcf", "r")
    seed = file.readlines(line)[0]
    seed = seed.replace("\n", "")
    return seed

def writer(type, data):
    if type == 0:   #uncrawled
        file = open("uncrawled.wcf", "a")
        file.writelines(data)
        file.write("\n")
        file.close()
    elif type == 1: #crawled
        file = open("crawled.xml", "a")
        file.write("\n" + data)
        file.close()
    elif type == 2: #debug
        file = open("debug.log", "a")
        file.write("\n" + data)
        file.close()
    elif type == 3: #crawlerref
        file = open("crawlerref.wcf", "w")
        file.write(data)
        file.close()

def writeIndex(title, url):
    writer(1, "<index>")
    writer(1, "\t<page>"+title+"</page>")
    writer(1, "\t<url>"+url+"</url>")
    writer(1, "</index>")


def checkRobots():
    pass

TIMEOUT_MAX = 10

current_seed_index = 0
request(sys.argv[1])
while 1: 
    current_seed_index + 1       
    request(fetchNextSeed(current_seed_index))
    
    
