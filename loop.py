import os
from time import sleep
from datetime import datetime, timedelta
from Bot import like, get_followers

def loop():
    should_stop = False
    try:
        while not should_stop:
            now = datetime.now()
            next_run = now + timedelta(1)

            print("start time:", now)

            os.system("git pull")
            like()
            get_followers()
            os.system("git pull")
            os.system("git add .")
            os.system("git commit -m \"New stats\"")
            os.system("git push")


            print("next run:", next_run)
            time_delta =  next_run - datetime.now()
            seconds_to_sleep = time_delta.seconds if time_delta.seconds > 0 else 0
            print("sleeping...")
            sleep(seconds_to_sleep)

    except Exception:
        print("ending...")
        should_stop = True

if __name__ == "__main__":
    loop()