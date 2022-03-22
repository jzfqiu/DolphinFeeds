from feed import Feed
from time import sleep
from config import SOURCES, SLEEP_TIME

if __name__ == "__main__":
    while True:
        for d in SOURCES:
            f = Feed(d["url"], d["source"], d["tags"])
            updated = f.update()
        print("[Server] Update complete, {} articles updated.".format(updated))
        sleep(SLEEP_TIME)
        