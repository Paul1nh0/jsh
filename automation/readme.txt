 
## Setup ##

-- win --

<< python >>

download and install python 2.7 -> https://www.python.org/downloads/
download get-pip.py -> https://bootstrap.pypa.io/get-pip.py
run: python get-pip.py
run: python -m pip install psutil

download and install windbg: https://developer.microsoft.com/en-us/windows/hardware/download-windbg
download and install symbols: https://developer.microsoft.com/en-us/windows/hardware/download-symbols
download and install: 
https://www.microsoft.com/en-us/download/details.aspx?id=29, 
https://www.microsoft.com/en-us/download/details.aspx?id=15336

((edge))

configure edge to be the default browser.
configure edge to delete history.

-- linux --

((firefox))

do this: http://how-to.wikia.com/wiki/How_to_disable_Firefox%27s_session_restore_crash_recovery_feature

download ONLY ASAN BUILDS!

profit

## USEFUL-LINKS ##

<< mozilla >>

SpiderMonkey: https://archive.mozilla.org/pub/firefox/releases/58.0b5/jsshell/
Nightly: https://www.mozilla.org/en-US/firefox/channel/desktop/  <-- good for fuzzing ..
Asan: https://developer.mozilla.org/en-US/docs/Mozilla/Testing/Firefox_and_Address_Sanitizer
Source: https://hg.mozilla.org/mozilla-central/

<< google >>

Asan: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html
Source: https://cs.chromium.org/chromium/src

<< Ms >>

Chakra: https://github.com/Microsoft/ChakraCore/releases
Source: https://github.com/Microsoft/ChakraCore

<< apple >>

webkit: https://webkit.org/blog/29/nightly-builds/
Source: https://github.com/WebKit/webkit
build with asan for MacOs: https://trac.webkit.org/wiki/ASanWebKit

fuzz webkit on linux:

download src from: https://webkit.org/getting-the-code/
follow this inst: https://ghostbin.com/paste/rpqyp (after installing llvm clang)
or apply this patch: https://gist.github.com/kkuehl/af5bbcd843a6239cee2c64b58be6def7 


 
