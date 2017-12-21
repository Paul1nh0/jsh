import os, time, sys

while 1:
    time.sleep(120)
    os.system('taskkill /im '+sys.argv[-1]+' /f')
