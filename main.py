from ComicTk import *
from GoComicStrips import *
import datetime, allGlobals

ComicDict = {
            "Calvin And Hobbes" : CalvinAndHobbesInstance(),
            "Garfield": GarfieldInstance(),
            "Get Fuzzy": GetFuzzyInstance(),
            "Herman": HermanInstance(),
            "Luann": LuannInstance(),
            "Pearls Before Swine" : PearlsBeforeSwineInstance(),
            "Pickles": PicklesInstance()
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
    
    