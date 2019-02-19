import subprocess
import sys, os

dir_ = os.getcwd()

sys.path.append(dir_+'\\psutil')
sys.path.append('C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x64')
import psutil

os.system('lEdge.exe '+dir_+'\\curpus\\'+str(sys.argv[-1])+'\\fuzz-0.html')

#cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
#proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#for line in proc.stdout:
#    if ("edge" in str(line)) or ("Edge" in str(line)):
#        print line

import time
time.sleep(2)
pn = [(proc.name(),proc.cpu_percent(interval=1),proc.pid) for proc in psutil.process_iter() if "MicrosoftEdgeCP.exe" in proc.name()]
edgeList = []
for l in pn:
      if ("MicrosoftEdgeCP.exe" in str(l[0])):
          edgeList.append(l)
      
active = ()
#for g in edgeList: print g

edgeList.sort(key=lambda x: x[1])
#print edgeList[-1]

numActive = str(edgeList[-1][2])

with open("run.bat", mode='w') as bat:
      bat.write("@Echo OFF\n")
      bat.write('"C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x64\\cdb.exe" -p '+numActive+' -c "!exploitable;" -c "!load winext\msec.dll;" -c "g;"\n') 
      bat.write("timeout /T 60\n")
      bat.write("taskkill /im cdb.exe /f\n")

os.system('run.bat')

