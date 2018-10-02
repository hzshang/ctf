#!/usr/bin/env python

import argparse
#import gmpy2
#import math
#import sys

def chunk_str(s, chunksize):
	return [ s[i:i+chunksize] for i in range(0, len(s), chunksize) ]

def hex2int(s):
	return int(s, 16)
def bin2int(s):
	return int(s, 2)
def bytes2int(s):
	return int(s.encode('hex'), 16)
def bin2hex(s):
	return hex(int(s,2))[2:].strip('L')
def bin2oct(s):
	return oct(int(s,2))[1:].strip('L')

class Emu(object):
	def __init__(self, flag, shellcode):
		self.flag_file = flag
		self.flag = open(self.flag_file).read().strip()
		self.flag_bits = bin(int(self.flag.encode('hex'), 16))[2:].rjust(len(self.flag)*8, '0')
		self.shellcode_file = shellcode
		self.shellcode = open(self.shellcode_file).read()
		self.shellcode_bits = bin(int(self.shellcode.encode('hex'), 16))[2:].rjust(len(self.shellcode)*8, '0')

	def _emit(self, *s): #pylint:disable=no-self-use
		print ' '.join(str(e) for e in s)

	def emit_flag(self):
		raise NotImplementedError()

	def emit_shellcode(self):
		raise NotImplementedError()

	def start(self):
		raise NotImplementedError()

	def quit(self):
		raise NotImplementedError()

class EmuSimh(Emu): #pylint:disable=abstract-method
	def start(self):
		self._emit('run 100')

	def quit(self):
		self._emit('exit')

class PlatformMIX(Emu):
	LETTERS = dict(
		[ (c,n) for n,c in enumerate(' ABCDEFGHI', start=0) ] +
		[ (c,n) for n,c in enumerate('JKLMNOPQR', start=11) ] +
		[ (c,n) for n,c in enumerate('STUVWXYZ', start=22) ] +
		[ (c,n) for n,c in enumerate('0123456789', start=30) ] +
		[ (c,n) for n,c in enumerate('.,()+-*/=$', start=40) ] +
		[ (c,n) for n,c in enumerate("<>@;:'", start=50) ]
	)

	@staticmethod
	def _mixtoint(a):
		return sum(n*64**e for e,n in enumerate(reversed(a)))

	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 5), start=3137):
			val = self._mixtoint([ PlatformMIX.LETTERS[c] for c in fw.ljust(5, ' ') ])
			self._emit('smem %d %d' % (i, val))

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 30), start=100):
			ow = bin2int(sw)
			self._emit('smem %d %d' % (i, ow))

	def start(self):
		self._emit('run')

	def quit(self):
		self._emit('quit')

class PlatformMMIX(Emu):
	def emit_flag(self):
		pass

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 64)):
			ow = bin2int(sw)
			self._emit('M%x=%d' % (0x200+8*i, ow))

	def start(self):
		self._emit('@200')
		self._emit('c')

	def quit(self):
		self._emit('quit')

#pylint:disable=abstract-method
class PlatformPDP1(EmuSimh):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 3)):
			self._emit('d', oct(i), '''"%s"''' % fw.ljust(3))

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 18)):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(6, '0')
			self._emit('d', oct(64+i), ow)

class PlatformPDP8(EmuSimh):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 1), start=01337):
			self._emit('d', oct(i), """'%s""" % fw)

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 12), start=64):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(4, '0')
			self._emit('d', oct(i), ow)

class PlatformPDP10(EmuSimh):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 1), start=01337):
			self._emit('d', oct(i), """'%s""" % fw)

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 36), start=64):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(4, '0')
			self._emit('d', oct(i), ow)

class PlatformIBM1401(EmuSimh):
	def start(self):
		self._emit('att lpt /dev/stdout')
		self._emit('run 1')

	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 1), start=900):
			self._emit('d', i, """'%s""" % fw)

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 7), start=0):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(3, '0')
			self._emit('d', i, ow)

class PlatformNova(EmuSimh):
	def emit_flag(self):
		for i, fw in enumerate(chunk_str(self.flag, 2), start=01337):
			self._emit('d', oct(i), oct(int(fw.ljust(2).encode('hex'),16)))

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 16), start=0100):
			ow = oct(int(sw,2))[1:].replace('L','').rjust(6, '0')
			self._emit('d', oct(i), ow)

class PlatformLGP30(EmuSimh):
	@staticmethod
	def _make_addr(i):
		return "%02d%02d" % (i/64, i%64)

	LETTER_BITS = {
    	'0': '000010', '1': '000110', '2': '001010', '3': '001110', '4': '010010', '5': '010110', '6': '011010', '7': '011110', '8': '100010', '9': '100110',
    	'A': '111001', 'B': '000101', 'C': '110101', 'D': '010101', 'E': '100101',
    	'F': '101010', 'G': '101110', 'H': '110001', 'I': '010001', 'J': '110010',
    	'K': '110110', 'M': '011101', 'N': '011001', 'O': '100011', 'P': '100001', # L is fucking uppercase 1...
    	'Q': '111010', 'R': '001101', 'S': '111101', 'T': '101101', 'U': '101001',
    	'V': '011111', 'W': '111110', 'X': '100111', 'Y': '001001', 'Z': '000001',
	}
	LETTERS = { letter:bin2hex(bits).zfill(2)+'00' for letter,bits in LETTER_BITS.items() }

	def emit_flag(self):
		for i, c in enumerate(chunk_str(self.flag, 1), start=13*64+37):
			self._emit('d', self._make_addr(i), PlatformLGP30.LETTERS[c])

	def emit_shellcode(self):
		for i, sw in enumerate(chunk_str(self.shellcode_bits, 31), start=0100):
			if len(sw) < 31:
				continue
			self._emit('d', self._make_addr(i), bin2hex(sw+'0').zfill(8))

platforms = {
	'pdp-1': PlatformPDP1,
	'pdp-8': PlatformPDP8,
	'pdp-10': PlatformPDP10,
	'ibm-1401': PlatformIBM1401,
	'nova': PlatformNova,
	'lgp-30': PlatformLGP30,
	'mix': PlatformMIX,
	'mmix': PlatformMMIX,
}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Format converter.')
	parser.add_argument('machine', help="the machine type")
	parser.add_argument('flag', help="the flag file")
	parser.add_argument('shellcode', help="the shellcode file")
	args = parser.parse_args()

	e = platforms[args.machine](args.flag, args.shellcode)
	e.emit_shellcode()
	e.emit_flag()
	e.start()
	e.quit()
