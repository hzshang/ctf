for i in range(0,0x44a8,8):
	p=i+0x6001BC
	d=Qword(p)
	PatchQword(p,d^0x1122334455667788)
