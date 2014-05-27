import Tkinter as tk
import base64, io, imghdr
from PIL import Image
import datetime, config

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
    config.theComic = ComicDictInstance
    print("New Comic: "+ config.theComic.getName())
    #get the Base 64 Image and format it as a GIF
    theComicImage = PIL_format64AsGIF(config.theComic.getPILImage())

    #draw it to the canvas
    
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
    frame.pack()    
    return window

def tk_setImageInCanvas(window, thePhoto):
    theCanvas = window.children["comicFrame"].children["comicCanvas"]
    theCanvas.create_image(0,100, anchor=tk.NE, image=thePhoto)
    
def PIL_format64AsGIF(thePILImage):
    imghdr.what(thePILImage)