import urllib2 as urllib
import cStringIO
import datetime, allGlobals, io
from PIL import Image, ImageTk

#have to go two layers deep

class BabyBluesInstance(object):
    def __init__(self):
        self.url = "http://babyblues.com/archive/index.php?formname=getstrip&GoToDay="
        
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        
    def fetchImageURL(self):
        def findImageURLKey(htmlpage):
            def stripJava(javaPageUrl):
                javareq = urllib.Request(javaPageUrl)
                javareq.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox')
                javaresponse = urllib.urlopen(javareq)
                javapage = javaresponse.readlines()
                for javaLine in javapage:
                    if "src='http://safr.kingfeatures.com/" in javaLine:
                        imgLine = javaLine.split("<img src='")[1].split("' alt=")[0]
                        print("imgLine = "+ imgLine)
                        return imgLine
            for htmlLine in htmlpage:
#                print(htmlLine)
                if 'src="http://safr.kingfeatures.com/idn/babyblues/' in htmlLine:
                    print("html line: ", htmlLine)
                    retline = htmlLine.split('type="text/javascript" src="')[1].split('">Please use a')[0]
                    retline = retline.strip()
                    
                    print("retline: ", retline)
                    #get source from javascript which has the image
                    return stripJava(retline)
                    
            print("OH NO! EMPTY")
            return "empty"
        
        formattedDate = allGlobals.theDate.strftime("%m/%d/%Y")
        page = self.url+formattedDate
        print(page)         
        req = urllib.Request(page, headers=self.hdr)
        response = urllib.urlopen(req)
        html = response.readlines()
        #print(html)
        key = findImageURLKey(html)
        print(key)
        return key
    
    def getTkImage(self):
        #get Url
        url = self.fetchImageURL()
        #open url
        image_bytes = urllib.urlopen(url).read()
        #internal data file
        data_stream = io.BytesIO(image_bytes)
        #open as PIL Image object
        pil_image = Image.open(data_stream)
        #get size of image
        tk_image = ImageTk.PhotoImage(pil_image)
        
        return tk_image
    
    def getName(self):
        return "Baby Blues"