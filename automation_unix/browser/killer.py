import os, time, sys

while 1:
    
    os.system('killall '+sys.argv[-1])
    time.sleep(120)
