import sys
sys.path.append('C:\\Users\\akayn\\Documents\\runner\\psutil')
sys.path.append('C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x64')
import os

with open("run.bat", mode='w') as bat:
      bat.write("@Echo OFF\n")
      bat.write('"C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x64\\cdb.exe" -g '+sys.argv[-2]+' '+sys.argv[-1]+'\n') 
      bat.write("timeout /T 60\n")
      bat.write("taskkill /im cdb.exe /f\n")

os.system('run.bat')

