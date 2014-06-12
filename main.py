from ComicTk import *
from GoComicStrips import *
from CyanideAndHappinessStrip import *
from DilbertStrip import *
from BabyBluesStrip import *
import datetime, allGlobals
from collections import OrderedDict

ComicDict = {
             # Need to decrypt javascript before safrking images can be used
             #"Baby Blues" : BabyBluesInstance(),
            "Calvin And Hobbes" : CalvinAndHobbesInstance(),
            "Cyanide And Happiness": CyanideAndHappinessInstance(),
            "Dilbert": DilbertInstance(),
            "Garfield": GarfieldInstance(),
            "Get Fuzzy": GetFuzzyInstance(),
            "Herman": HermanInstance(),
            "Luann": LuannInstance(),
            "Pearls Before Swine" : PearlsBeforeSwineInstance(),
            "Pickles": PicklesInstance()
            }

ComicDict = OrderedDict(sorted(ComicDict.items(), key=lambda t: t[0]))

def main():
    root = tk.Tk()
    root = tk_GiveWindowMainMenu(root, ComicDict)
    root = tk_initializeCanvas(root)
    root = tk_GiveWindowNavigation(root, ComicDict)

    root.mainloop()

if __name__ == "__main__":
    allGlobals.theDate = datetime.datetime.today()
    print("The Date: "+ datetime.datetime.strftime(allGlobals.theDate, "%Y/%m/%d"))
    main()
    
    