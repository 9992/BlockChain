import hashlib
from codecs import encode, decode

def merkle(hList):
    if len(hList) == 1:
        return hList[0]
    newHList = []
    for i in range(0, len(hList)-1, 2):
        newHList.append(merklehhash(hList[i],hList[i+1]))
    if len(hList) % 2 == 1: 
        newHList.append(merklehhash(hList[-1],hList[-1]))
    return merkle(newHList)

def merklehhash(a, b):
    a1 = decode(a[::-1],'hex')    
    b1 = decode(b[::-1],'hex')
    result = hashlib.sha256(a1+b1).digest()
    return encode(result,'hex')[::-1]
