import hashlib

def merkle(hashList):
    if len(hashList)==1:
        return hashList[0]
    newHashList = []

    for i in  range(0,len(hashList)-1,2):
        newHashList.append(calc_hash(hashList[i],hashList[i+1]))
    if len(hashList) % 2 == 1:
        newHashList.append(calc_hash(hashList[-1],hashList[-1]))
    return merkle(newHashList)

# 해시의 기본 원리는 모든 문자스트림을 리틀 엔디언 순으로 읽어들여 나눈다.
# 따라서 해시와 해시를 더할 때에는 역순으로 더 할 수 있도록 해야한다.
def calc_hash(a_list,b_list):
    a = a_list[::-1]
    b = b_list[::-1]
    result_hash = hashlib.sha256(hashlib.sha256(a+b).digest()).digest()
    return result_hash[::-1]

txHashes = [
"8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87",
"fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4",
"6359f0868171b1d194cbee1af2f16ea598ae8fad666d9b012c8ed2b79a236ec4",
"e9a66845e05d5abc0ad04ec80f774a7e585c6e8db975962d069a522137b80c1d",
]

print(merkle(txHashes))