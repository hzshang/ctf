
d={0x5555555547c5:'^H\x89'
,0x555555554845:'H\xc1'
,0x555555555c1b:']A'
,0x555555555c1e:'A]'
,0x555555555744:'\x90]\xc3'
,0x555555554b67:'H\x8b\x85'
,0x555555554b71:'H\x8d'
,0x5555555558bd:'\x8b\x00'
,0x5555555559e9:'H\x8b'
,0x555555554cc8:'\x89E\xd8'
,0x555555554d25:'\x8b\x12\x01'
,0x555555554d56:'\x01\xca'
,0x555555554da8:'1\xd1H'
,0x555555554e22:'\x8bE\xc4'
,0x555555554e32:'\x8bU'
,0x555555554e3b:'H\x83\xc2'
,0x555555554e61:'\x8bU'
,0x555555554f2e:'\x01\xd0\x89'
,0x555555554feb:'\x8bE\xe0'
,0x555555555186:'\x8b\n'
,0x5555555552b6:'\x01\xd0'
,0x5555555552f6:'\x8bE\xbc'
,0x5555555553c5:'\x01\xd0'
,0x555555555482:'\x8bU\xdc'
,0x555555555540:'H\x83\xc2'
,0x555555555549:'\x01\xca\x01'
,0x5555555555f1:'\x8bM\xc8'
,0x555555555aed:'H\x8b'
,0x555555555b0f:'\xc1\xe8\x08'
,0x555555554934:'\x8bE\xf4'
,0x555555554c0f:'H\x8d\x85'}

for add,s in d.items():
	for i in range(len(s)):
		PatchByte(add+i,ord(s[i]))






