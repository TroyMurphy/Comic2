import Tkinter as tk
import base64, io, imghdr
from PIL import Image, ImageTk
import datetime, allGlobals

def tk_GiveWindowMainMenu(window, ComicDict):    
    #Required because of limited scope to the command element of menu option
    def loadCommand(comicName):
        #print("loading Comic: "+ comicName)
        tk_switchComic(window, ComicDict[comicName])

    def exportSelection():
        ypos = 0
        for instance in ComicDict.values():
            try:
                photo = instance.getTkImage()
                tk_setImageInCanvas(window, photo, (0,ypos))
                ypos += 20 + photo._PhotoImage__size[1]
            except:
                print("Skipped "+instance.getName())
                pass
            
    def editSelection():
        pass
    
    def resetComicToNone():
        allGlobals.theComic = None
        
    menubar = tk.Menu(window)
    ComicSelectionMenu = tk.Menu(menubar, tearoff=0, name="mainMenu")
    ComicSelectionMenu.add_command(label="All", command= resetComicToNone)
    for comic in ComicDict.values():
        #note comic=comic snapshots the for loop and gives lambda a default value
        #without it only the last comic will show for all lambda functions
        ComicSelectionMenu.add_command(label=comic.getName(), command=lambda comic=comic: loadCommand(comic.getName()))
        print("Comic Added: "+ comic.getName())
        
    ExportMenu = tk.Menu(menubar, tearoff=0)
    ExportMenu.add_command(label="View Selection", command=exportSelection)
    ExportMenu.add_command(label="Edit Selection", command=editSelection)
    
    menubar.add_cascade(label="Comics", menu=ComicSelectionMenu)
    menubar.add_cascade(label="Select", menu=ExportMenu)
    
    window.config(menu=menubar)
    return window

def tk_switchComic(window, ComicDictInstance):
    allGlobals.theComic = ComicDictInstance
    print(allGlobals.theComic.getName())
    if type(allGlobals.theComic) != type(None):
        titleLabel = tk.Label(master = window, text=allGlobals.theComic.getName(), font=("Arial", 16), name="titleLabel")
        titleLabel.pack(side="top")
    else:
        titleLabel = tk.Label(master = window, text="All Comics", font=("Arial", 16), name="titleLabel")
        titleLabel.pack(side="top")
    #get the Base 64 Image and format it as a GIF
    theComicImage = allGlobals.theComic.getTkImage()
    if theComicImage != None:
    #draw it to the canvas
        try:
            tk_setImageInCanvas(window, theComicImage)
        except:
            print("Image Failed To Load In Canvas")
    
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

def tk_setImageInCanvas(window, thePhoto, postuple=(0,0)):
    theCanvas = window.children["comicFrame"].children["comicCanvas"]
    print("Found canvas")
    theCanvas.create_image(postuple[0],postuple[1], image=thePhoto, anchor=tk.NW)
    try:
        theCanvas.refs
    except AttributeError:
        theCanvas.refs = []
        
    theCanvas.refs.append(thePhoto)
    print("Connected Image")

def tk_GiveWindowNavigation(window, ComicDict):
    
    def exportAll():
        ypos = 0
        for instance in ComicDict.values():
            try:
                photo = instance.getTkImage()
                tk_setImageInCanvas(window, photo, (0,ypos))
                ypos += 20 + photo._PhotoImage__size[1]
            except:
                print("Skipped "+instance.getName())
                pass
            
    def writeRefresh():
        try:
            window.children["comicFrame"].children["comicCanvas"].delete(tk.ALL)
        except Exception, e:
            print("Could not clear canvas. %s" % e)
            pass
        print(allGlobals.theDate)
        dateEntry.delete(0, tk.END)
        dateEntry.insert(0, str(allGlobals.theDate.date()).replace("-","/"))
        if type(allGlobals.theComic) != type(None):
            tk_switchComic(window, allGlobals.theComic)
        else:
            exportAll()
        
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

    