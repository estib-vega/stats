import os
from time import sleep
from datetime import datetime, timedelta

def loop():
    should_stop = False
    try:
        while not should_stop:
            now = datetime.now()
            next_run = now + timedelta(1)

            print("start time:", now)

            os.system("git pull")
            os.system("python script.py")
            os.system("git add .")
            os.system("git commit -m \"New stats\"")
            os.system("git push")


            print("next run:", next_run)
            time_delta = datetime.now() - next_run
            seconds_to_sleep = time_delta.seconds
            print("sleeping...")
            sleep(seconds_to_sleep)

    except Exception:
        print("ending...")
        should_stop = True

if __name__ == "__main__":
    loop()