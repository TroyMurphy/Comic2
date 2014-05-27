from ComicTk import *
import PearlsBeforeSwine
import datetime, allGlobals

ComicDict = {
            "Pearls Before Swine" : PearlsBeforeSwine.PearlsBeforeSwineInstance() 
            }

def main():
    root = tk.Tk()
    root = tk_GiveWindowMainMenu(root, ComicDict)
    root = tk_initializeCanvas(root)
    root = tk_GiveWindowNavigation(root)

    root.mainloop()

if __name__ == "__main__":
    allGlobals.theDate = datetime.datetime.today()
    print("The Date: "+ datetime.datetime.strftime(allGlobals.theDate, "%Y/%m/%d"))
    main()
    
    