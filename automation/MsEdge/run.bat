@Echo OFF
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\cdb.exe" -p 8540 -c "!exploitable;" -c "!load winext\msec.dll;" -c "g;"
timeout /T 60
taskkill /im cdb.exe /f
