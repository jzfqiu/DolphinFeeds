from feed import Feed
from time import sleep
from config import SOURCES, SLEEP_TIME

if __name__ == "__main__":
    while True:
        for d in SOURCES:
            f = Feed(d["url"], d["source"], d["tags"])
            f.update()
        print("Update complete")
        sleep(SLEEP_TIME)
        