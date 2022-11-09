# AES-DFA
This tool automates and facilitates an  Differential fault analysis attack on AES 128 with a fault injected between the 2 last MixColumns


This tools is based on [this paper](https://blog.quarkslab.com/differential-fault-analysis-on-white-box-aes-implementations.html) from Philippe Teuwen and Charles Hubain

According to the previous article, we need to provide ``the ciphertext`` and 4 pairs of ``erroneous ciphertexts`` (4 different positions)

# Usage :
```python
from DFA_Attack import *

cipher_text = b'827070B8E53C40F79C51B57EB082367D'

faulted_texts = [
	b'1D7070B8E53C40339C51427EB005367D',
	b'A47070B8E53C40DA9C51817EB0AD367D',
	b'829970B8EE3C40F79C51B52BB082437D',
	b'820570B8D33C40F79C51B5EAB0823F7D',
	b'8270C2B8E57E40F7F551B57EB08236B0',
	b'8270DAB8E52140F7DB51B57EB08236F2',
	b'82707000E53C6DF79CABB57EA782367D',
	b'827070C5E53C73F79C21B57E4982367D'
]


key = DFA_attack(
		cipher=cipher_text,
		faults=faulted_texts,
		rounds=11
	).Crack_key()

print(key)
```

*This tools was inspired by phoenixAES code from (Philippe Teuwen)*
