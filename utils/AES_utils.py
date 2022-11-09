from utils.constants import sbox,table,sbox_inv,mult

def reverse_key_expension(expended, rounds):
	for r in reversed(range(1, rounds)):
		for _ in range(3):
			expended.insert(0, xor(expended[2], expended[3]))
		expended.insert(0, xor(
			xor(expended[3], lookup(r)),
			inv_sub(inv_rev(expended[2]))
			)
		)
	return expended

def get_candidate(diff,table):
	def get_cpt(diff, table):
		ibox = [sbox,sbox_inv][True]
		itab = [0]*256
		for i,mi in enumerate(mult[table]):
			itab[mi] = i
		return [
			itab[ibox[j^diff] ^ ibox_j] 
			for j,ibox_j in enumerate(ibox)
		]
	candidats = [get_cpt(a, b) for a,b in zip(diff, table)]
	intersec  = set(candidats[0]).intersection(*candidats[1:])
	return [[set([j for j,x in c if x==z]) for c in [
				[t for t in enumerate(c) if t[1] in intersec]
			for c in candidats]
		] for z in intersec]


xor	 	  = lambda A,B : bytes([i ^ j for i, j in zip(A, B)])
lookup    = lambda x : bytes([table[x], 0, 0, 0])
inv_rev   = lambda w : w[1:] + bytes([w[0]])
inv_sub   = lambda w : bytes([sbox[_] for _ in w])
add_key   = lambda st,key : xor(st, key)
int2bytes = lambda st: (state).to_bytes(16, byteorder='big', signed=False)
bytes2int = lambda st: int.from_bytes(state, byteorder='big', signed=False)