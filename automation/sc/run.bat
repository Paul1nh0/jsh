FIXME!!
@Echo OFF
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\cdb.exe" -g C:\\Users\\akayn\\Desktop\\jssh\\chakra\\cc_windows_1_7_5\\x64_release\\ch.exe C:\Users\akayn\desktop\automation\SC\curpus\11\fuzz-0.js
timeout /T 60
taskkill /im cdb.exe /f
