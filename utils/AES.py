from utils.AES_utils import xor,add_key,get_candidate,int2bytes,bytes2int
from utils.constants import sbox,sbox_inv,mult,fault_map
from binascii import hexlify

def check_diff(output,ref):
    diffmap = [x!=0 for x in xor(output,ref)]
    if sum(diffmap)==4 and output != ref:
        return fault_map[1].index(diffmap)
    return None

def crack(faults, ref):
    candidates = [[], [], [], []]
    recovered  = [False, False, False, False]
    key        = [None]*16
    for f in faults:
        idx = check_diff(f,ref)
        if idx is not None:
            if recovered[idx]:
                continue
            absorb(idx, f, candidates, ref)
            if False not in [len(_) == 1 for _ in (
                    candidates[idx],
                    candidates[idx][0][0],
                    candidates[idx][0][1],
                    candidates[idx][0][2],
                    candidates[idx][0][3])]:
                recovered[idx]=True
                K = [k for k, y in zip (range(16), fault_map [1][idx]) if y]
                G = [g for g, y in zip (ref, fault_map [1][idx]) if y]
                for j in range(4):
                    key[K[j]]=list(candidates[idx][0][j])[0] ^ G[j]

            if False not in recovered:
                return hexlify(bytes(key)).decode(),True

    return ''.join([
            "%02X" % x if x is not None else ".." 
                for x in key
        ]).lower(),False

def absorb(idx, o, candidates, goldenrefbytes):
    diff=[x^g for x, g, y in zip (o, goldenrefbytes, fault_map [1][idx]) if y]
    cands  = get_candidate(diff, [[14, 9,  13, 11], [2, 3, 1, 1]][True])
    cands += get_candidate(diff, [[11, 14, 9,  13], [3, 1, 1, 2]][True])
    cands += get_candidate(diff, [[13, 11, 14, 9] , [1, 1, 2, 3]][True])
    cands += get_candidate(diff, [[9,  13, 11, 14], [1, 2, 3, 1]][True])
    if not candidates[idx]:
        candidates[idx] = cands
        return
    new_c=[]
    for lc0,lc1,lc2,lc3 in cands:
        for loc0,loc1,loc2,loc3 in candidates[idx]:
            if (lc0 & loc0) and (lc1 & loc1) and (lc2 & loc2) and (lc3 & loc3):
                new_c.append((
                    (lc0 & loc0),
                    (lc1 & loc1),
                    (lc2 & loc2),
                    (lc3 & loc3)
                ))
    if new_c != []:
        candidates[idx]=new_c
    else:
        candidates[idx] += cands
