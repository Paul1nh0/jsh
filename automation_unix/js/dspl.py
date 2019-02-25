dup = set()

with open('crash.txt','r') as cr4:
    cont = cr4.read()
    t12 = str(cont)
    if 'set([' in t12:
        dup = eval(t12)

with open('log.crash.txt', 'w') as lg:
    for i in dup:
        lg.write(i)
