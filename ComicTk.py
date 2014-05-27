import Tkinter as tk
import base64, io, imghdr
from PIL import Image, ImageTk
import datetime, allGlobals

def tk_GiveWindowMainMenu(window, ComicDict):
    menubar = tk.Menu(window)
    ComicSelectionMenu = tk.Menu(menubar, tearoff=0)
    
    #Required because of limited scope to the command element of menu option
    def loadCommand(comicName):
        tk_switchComic(window, ComicDict[comicName])

    for comic in ComicDict.values():  
        ComicSelectionMenu.add_command(label=comic.getName(), command=lambda: loadCommand(comic.getName()))
    menubar.add_cascade(label="Comics", menu=ComicSelectionMenu)
    
    window.config(menu=menubar)
    return window

def tk_switchComic(window, ComicDictInstance):
    allGlobals.theComic = ComicDictInstance
    print(allGlobals.theComic.getName())
    if type(allGlobals.theComic) != type(None):
        titleLabel = tk.Label(master = window, text=allGlobals.theComic.getName(), font=("Arial", 16), name="titleLabel")
        titleLabel.pack(side="top")
    else:
        window.children['titleLabel'].config(text=allGlobals.theComic.getName())
    #get the Base 64 Image and format it as a GIF
    theComicImage = PIL_format64AsGIF(allGlobals.theComic.getBase64Image())
    #draw it to the canvas
    try:
        tk_setImageInCanvas(window, theComicImage)
    except:
        print("You suck")
    
def tk_initializeCanvas(window):
    #create frame for scrollbars and canvas
    frame = tk.Frame(master=window, bd=2, relief=tk.SUNKEN, name="comicFrame")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    #add in x scrollbar
    xscrollbar = tk.Scrollbar(master=frame, name="comicXScrollbar", orient=tk.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
    #add in y scrollbar
    yscrollbar = tk.Scrollbar(master=frame, name="comicYScrollbar", orient=tk.VERTICAL)
    yscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
    #create and pack canvas into frame
    canvas = tk.Canvas(master=frame, height=500, width=800, bd=0,
                       xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, name="comicCanvas")
    canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    #allow all images on the canvas to be scrolled
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    #sync scrollbars to canvas
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)
    #put frame into the window
    frame.pack(side="bottom")    
    return window

def tk_setImageInCanvas(window, thePhoto):
    theCanvas = window.children["comicFrame"].children["comicCanvas"]
    print("Found canvas")
    theCanvas.create_image(0,0, image=thePhoto,anchor=tk.NW, )
    theCanvas.image = thePhoto
    print("Connected Image")
    #window.children["comicFrame"].pack()
    print("switchedComic")
    
def PIL_format64AsGIF(inImage):
    if allGlobals.theDate.isoweekday() != 7:
        ("print if")
        returnpic = tk.PhotoImage(data=inImage)
    else:
        print("else")
        jpg_str = base64.b64decode(inImage)
        jpg_data = io.BytesIO(jpg_str)
        
        pil_image = Image.open(jpg_data)
        returnpic = ImageTk.PhotoImage(pil_image)
    return returnpic

def tk_GiveWindowNavigation(window):
        
    def writeRefresh():
        print(allGlobals.theDate)
        dateEntry.delete(0, tk.END)
        dateEntry.insert(0, str(allGlobals.theDate.date()).replace("-","/"))
        if type(allGlobals.theComic) != type(None):
            tk_switchComic(window, allGlobals.theComic)
        else:
            print("No Comic Selected")
        
    def fetchYesterday():
        allGlobals.theDate = allGlobals.theDate - datetime.timedelta(days=1)
        writeRefresh()
                
    def fetchTomorrow():
        if (allGlobals.theDate + datetime.timedelta(days=1)).date() <= datetime.datetime.today().date():
            allGlobals.theDate = allGlobals.theDate + datetime.timedelta(days=1)
        writeRefresh()

    def fetchCustom():        
        customDate = datetime.datetime.strptime(dateEntry.get(), "%Y/%m/%d" )
        
        if customDate.date() <= datetime.datetime.today().date():
            allGlobals.theDate = customDate
            writeRefresh()
        else:
            print("Invalid Date given")
        
    def fetchToday():
        allGlobals.theDate = datetime.datetime.today()
        writeRefresh()
        
    navigationFrame = tk.Frame(master=window, name="navigationFrame")
    dateFrame = tk.Frame(master=window, name='dateFrame')
    
    dateEntry = tk.Entry(master=dateFrame, width=9, name='dateEntry')
    dateEntry.insert(0, str(allGlobals.theDate.date()).replace("-","/"))

    leftButton = tk.Button(master=navigationFrame, text="<<", width=10, command=fetchYesterday, name="leftButton")
    rightButton = tk.Button(master=navigationFrame, text=">>", width=10, command=fetchTomorrow, name="rightButton")
    dateEntryButton = tk.Button(master=dateFrame, text="SUBMIT", width=5, command=fetchCustom, name="dateEntryButton")
    todayButton = tk.Button(master=navigationFrame, text="GO TO TODAY'S STRIP", width=18, command=fetchToday, name="todayButton")
    
    leftButton.pack(side="left")
    todayButton.pack(side="left")
    rightButton.pack(side="left")
    
    dateEntry.pack(side="left")
    dateEntryButton.pack(side="left")
    
    navigationFrame.pack(side="top")
    dateFrame.pack(side="top")
    
    return window