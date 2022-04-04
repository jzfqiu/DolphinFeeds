import zoneinfo
from feed import Feed
from time import sleep
from config import SOURCES, SLEEP_TIME
from datetime import datetime
from zoneinfo import ZoneInfo
import traceback

if __name__ == "__main__":
    while True:
        for d in SOURCES:
            f = Feed(d["url"], d["source"], d["tags"])
            try:
                updated = f.update()
            except:
                traceback.print_exc()
        now = datetime.now()
        now.replace(tzinfo=ZoneInfo("America/New_York"))
        print("[{}] Update complete, {} articles updated.".format(now.strftime("%H:%M:%S"), updated))
        sleep(SLEEP_TIME)
        