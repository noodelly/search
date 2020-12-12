from html.parser import HTMLParser
import requests
import os
import sys

uncrawled = ['https://wikipedia.org', 'https://google.com']
crawled = []

class HTMLParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            print("Start tag: ", tag)
            print("Attributes: ", attrs)
            crawl(attrs)
    def handle_data(self, data):
        print("Found data: ", data)

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
    elif target[:8] == "https://":
        print("HTTPS FOUND")
    elif target[:8] == "HTTPS://":
        print("HTTPS FOUND")
    elif target[:8] == "HTTP://":
        print("HTTP FOUND")
    elif target[:8] == "http://":
        print("HTTP FOUND")
    elif target[:1] == "/":
        print("SUBDIR FOUND")

    elif target[:1] == "#":
        print("IGNORE: IS A IN-PAGE LINK")
        pass
        
def request(seed): 
    print(seed)
    try:
        response = requests.get(seed)
        print("GET w/ status code: ", response.status_code)
        parser = HTMLParse()
        parser.feed(str(response.content))
        print("RETURNED SIZE: ", len(response.content) / 1000, "KB")
    except:
        crawled.append(seed)
        print("GET FAIL: HOST COULD NOT BE REACHED")
        print("TRYING NEXT SEED")

def checkRobots():
    pass
        
request(sys.argv[1])
    
    
