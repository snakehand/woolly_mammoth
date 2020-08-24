gdict = {}

def name(n):
    name = ""
    if n&1:
        name = name + "A"
    if n&2:
        name = name + "B"
    if n&4:
        name = name + "C"
    if n&8:
        name = name + "D"
    if n&16:
        name = name + "E"
    if n&32:
        name = name + "F"
    return name

mbits = 31

print("Building raw graph")
for n2 in range(1,mbits):
    for n1 in range(1,mbits):
        nlist = []
        for n in range(1,mbits):
            if (n&n2) == 0 and (n&n1) > 0 and (n&(~n1)) > 0:
                nlist.append(n)
        if len(nlist):
            gdict[(n2,n1)] = nlist

            
print("Pruning unreachable nodes")
while True:
    pruned = False
    my_keys = list(gdict.keys())
    for (n2,n1) in my_keys:
        n_list = gdict[(n2,n1)]
        plist = []
        for n in n_list:
            if (n1,n) in gdict:
                plist.append(n)
            else:
                pruned = True
        if len(n_list) != len(plist):
            if len(plist):
                gdict[(n2,n1)] = plist
            else:
                del gdict[(n2,n1)]
    if not pruned:
        break

reachable = {}
for (n2,n1) in gdict.keys():
    nlist = gdict[(n2,n1)]
    for n in nlist:
        reachable[(n1,n)] = True

my_keys = list(gdict.keys())
for (n2,n1) in my_keys:
    if not (n2,n1) in reachable:
        del gdict[(n2,n1)]

print("Raw graph has",len(gdict),"keys")
with open("wool.dot","w") as f:
    f.write("digraph woolly {\n")
    for (n2,n1) in gdict.keys():
        nlist = gdict[(n2,n1)]
        for n in nlist:
            start = name(n2)+"_"+name(n1)
            end = name(n1)+"_"+name(n)
            f.write("    %s -> %s;\n" % (start, end))
    f.write("}\n")

def is_cycle(start, current, max_depth):
    global gdict
    if max_depth <=0:
        return False
    (n2,n1) = current
    if current in gdict:
        n_list = gdict[current]
        for n in n_list:
            if (n1,n) == start:
                return [start]
            recurse = is_cycle(start, (n1,n), max_depth-1)
            if recurse:
                return recurse + [(n1,n)]
    return False

print("Detecting cycles")
cycles = {}
for start in gdict.keys():
    (n2,n1) = start
    if bin(n2).count("1") == 1:
        continue
    if start in cycles:
        continue
    print("c:", start)
    cl = is_cycle(start,start,10)
    if cl:
        for c in cl:
            cycles[c] = True

print("Found", len(cycles), "cyclical nodes. Pruning graph")
for g in gdict.keys():
    if not g in cycles:
        print(g)
        
with open("wool_cycles.dot","w") as f:
    f.write("digraph woolly {\n")
    for (n2,n1) in cycles.keys():
        nlist = gdict[(n2,n1)]
        for n in nlist:
            start = name(n2)+"_"+name(n1)
            end = name(n1)+"_"+name(n)
            f.write("    %s -> %s;\n" % (start, end))
    f.write("}\n")
