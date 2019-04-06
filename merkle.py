import hashlib

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
    a1 = a.encode('utf-8')[::-1]
    b1 = b.encode('utf-8')[::-1]
    #a1 = decode(a[::-1],'hex')    
    #b1 = decode(b[::-1],'hex')
    result = hashlib.sha256(a1+b1).hexdigest()
    #result = hashlib.sha256(a1+b1).digest()
    #print(result)
    #print(encode(result,'hex')[::-1])
    #print(encode(result2,'hex')[::-1])
    return result[::-1]
    # return encode(result,'hex')[::-1]
