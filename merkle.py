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
    print("result : ", result)
    return encode(result,'hex')[::-1]

txHashes = [
"8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87",
"fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4",
"6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4",
"e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d"
]

print(merkle(txHashes))