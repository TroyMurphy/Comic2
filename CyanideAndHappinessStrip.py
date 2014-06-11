import urllib2 as urllib
import cStringIO
import datetime, allGlobals, io
from PIL import Image, ImageTk

class CyanideAndHappinessInstance(object):
    def __init__(self):
        self.url = "http://www.explosm.net/comics/"
        
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
                if 'src="http://www.explosm.net/db/files/Comics/' in htmlLine:
                    #print("html line: ", htmlLine)
                    retline = htmlLine.split("http://www.explosm.net/db/files/Comics/")[1]
                    #print("retline = ", retline)
                    retline = str(retline).split('"')[0]
                    retline = retline.strip()
                    #print("retline: ", retline)
                    return retline
            print("OH NO! EMPTY")
            return "empty"
        
        formattedDate = str((allGlobals.theDate.date() - datetime.datetime.strptime("09/01/2004","%m/%d/%Y").date()).days + 15)
        page = self.url+formattedDate
        #print(page)         
        req = urllib.Request(page, headers=self.hdr)
        response = urllib.urlopen(req)
        html = response.readlines()
        #print(html)
        key = findImageURLKey(html)
        print("URL " +"http://www.explosm.net/db/files/Comics/" + key)
        return "http://www.explosm.net/db/files/Comics/" + key
    
    def getTkImage(self):
        try:
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
        except:
            print("Returned None")
            return None
        
    def getName(self):
        return "Cyanide And Happiness"