arr=[3,-1,-1,-1,5,1]
even = 0
odd = 0

for i in arr:
    value = i
    if (i < 0):
        value = i * -1
    if (value % 2 == 0):
        even += i;
    else:
        odd += i;

if(even==0):
    gzero=0
    lzero=0
    for i in arr:
        if(i<0):
            lzero+=i;
        else:
            gzero+=i;
    print((gzero-lzero)*(gzero-lzero))
elif(odd==0):
    gzero = 0
    lzero = 0
    for i in arr:
        if (i < 0):
            lzero += i;
        else:
            gzero += i;
    print((gzero - lzero) * (gzero - lzero))
else:
    print((even-odd)*(even-odd))
