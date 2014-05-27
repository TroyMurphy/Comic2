import urllib2, base64
import datetime, config, io
from PIL import Image, ImageTk
from StringIO import StringIO


class GoComic(object):
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        
    def fetchImageURL(self):
        def findImageURLKey(htmlpage):
            for htmlLine in htmlpage:
#                print(htmlLine)
                if "http://assets.amuniversal.com/" in htmlLine:
                    #print("html line: ", htmlLine)
                    retline = htmlLine.split('=')[2].split('/')[3]
                    retline = str(retline)
                    retline = retline.strip(' ').strip('"')
                    # print("retline: ", retline)
                    return retline
            print("OH NO! EMPTY")
            return "empty"
        
        page = self.url+str(config.theDate.date()).replace("-","/")
        print(page)         
        req = urllib2.Request(page, headers=self.hdr)
        response = urllib2.urlopen(req)
        html = response.readlines()
        #print(html)
        key = findImageURLKey(html)
        print("URL " +"http://assets.amuniversal.com/" + key)
        return "http://assets.amuniversal.com/" + key
    
    def getPILImage(self):
        picReq = urllib2.Request(self.fetchImageURL(), headers=self.hdr)
        fd = urllib2.urlopen(picReq)
        image_file = fd.read()
        print(str(type(image_file)))       
        print(str(type(StringIO(image_file))))
        comicImage = Image.open(StringIO(image_file))
        return ImageTk.PhotoImage(comicImage)
        
    def getName(self):
        return self.name
    
    def setUrl(self, url):
        self.url = url