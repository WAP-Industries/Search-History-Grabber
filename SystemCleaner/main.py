import sys
sys.dont_write_bytecode = True

from dotenv import load_dotenv
from fetcher import *

def main():
    load_dotenv()
    
    dirs = {} 
    for i in os.listdir(Fetcher.TargetDir):
        d = Fetcher.TargetDir+i+"\\History"
        if (os.path.exists(d)): dirs[i] = d

    if not os.path.exists(Fetcher.Out): 
        os.mkdir(Fetcher.Out)

    for i in dirs:
        shutil.copy(dirs[i], f"{Fetcher.Out}{i}")
    Fetcher.Run()

if __name__=="__main__":
    main()