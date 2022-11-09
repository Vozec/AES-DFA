from binascii import unhexlify,hexlify

from utils.AES import crack
from utils.AES_utils import *

class DFA_attack:
	def __init__(self,cipher,faults,rounds=11):
		self.cipher = cipher
		self.faults = faults
		self.rounds = rounds

	def Crack_key(self):
		self.key_recovered,recovered = crack(
			[unhexlify(x) for x in self.faults],
			unhexlify(self.cipher)
		 )
		if recovered:
			return self.get_init_key(self.key_recovered,self.rounds)
		return self.key_recovered

	def get_init_key(self,last_round_key,rounds):
		unhex = unhexlify(bytes(last_round_key,'utf-8'))
		expended = [
			unhex[_ : _ + len(unhex) // 4]
			for _ in range(0, len(unhex), 4)
		]
		return hexlify(
			b"".join(reverse_key_expension(expended, rounds)[:4])
		).decode()