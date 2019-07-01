import os
from time import sleep
from datetime import datetime, timedelta

def loop():
    try:
        while True:
            now = datetime.now()
            next_run = now + timedelta(1)

            print("start time:", now)

            os.system("git pull")
            os.system("python script.py")
            os.system("git add .")
            os.system("git commit -m \"New stats\"")
            os.system("git push")


            print("next run:", next_run)
            time_delta = next_run - now
            seconds_to_sleep = time_delta.seconds
            print("sleeping...")
            sleep(seconds_to_sleep)

    except Exception:
        print("ending...")

if __name__ == "__main__":
    loop()