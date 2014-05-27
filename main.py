from ComicTk import *
import PearlsBeforeSwine
import datetime, config

ComicDict = {
            "Pearls Before Swine" : PearlsBeforeSwine.PearlsBeforeSwineInstance() 
            }

def main():
    root = tk.Tk()
    root = tk_GiveWindowMainMenu(root, ComicDict)
    root = tk_initializeCanvas(root)
    root.mainloop()

if __name__ == "__main__":
    config.theDate = datetime.datetime.today()
    print("The Date: "+ datetime.datetime.strftime(config.theDate, "%Y/%m/%d"))
    main()
    
    