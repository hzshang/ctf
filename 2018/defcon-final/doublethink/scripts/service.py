#!/usr/bin/env python

import subprocess
import hashlib
import random
import base64
import string
import json
import sys
import os
import signal

available = {
	'past': { 'lgp-30', 'pdp-1', 'pdp-8', 'pdp-10', 'mix', 'ibm-1401', 'nova' },
	'present': { 'amd64', 'arm64', 'mipsel' },
	'future': { 'risc-v', 'hexagon', 'mmix', 'clemency' }
}
all_available = set.union(*available.values())
max_control = len(available['past']) + len(available['future']) + 1

descriptions = {
	'lgp-30': "Built in 1956, the Lionhearted Grand Party 30, or the LGP-30 was an early general purpose computer. Heroic Party members would toil with this desk sized computer late into the light, rewriting the past in the Party's image.",
	'pdp-1': "The first Party Data Platform design, the PDP-1 revolutionized the Party's ability to adjust the narrative of events.",
	'pdp-8': "The Party Data Platform 8 design brought Big Brother to the masses.",
	'pdp-10': "The Party Data Platform 10 was a valiant attempt at solidifying party control.",
	'mix': "Donald Knuth, a faithful servant of the party, created the Managerial Interactive X.",
	'amd86': "The Advanced Management Design allowed the Party to controll undesirables."
}

shellcode = ""

def choose_arch(controlled):
	print "[**]"
	print "[**]"

	num_past = len(available['past'] & set(controlled))
	num_present = len(available['present'] & set(controlled))
	#num_future = len(available['future'] & set(controlled))
	new_past = available['past'] - set(controlled)
	new_present = available['present'] - set(controlled)
	new_future = available['future'] - set(controlled)

	can_choose = set()
	# can_choose = {"amd64"}

	if num_present == 0:
		print "[**] You cannot control the past without controlling the present, and your influence on the future depends on your influence on the past."
		print "[**] The party controls all."
		print "[**] Choose your actions wisely."
		print "[**] You may attempt to exert control over the following present architectures:", ' '.join(sorted(new_present))
		can_choose |= new_present
	elif new_past:
		print "[**] Since you control the blissful present, you may exert control over doubleplusgood architectures of our past:", ' '.join(sorted(new_past))
		can_choose |= new_past

	if num_present > 0 and num_past > 0 and new_future:
		print "[**] As you control the gloried past, you may attempt to exert control over the architectures of our bright future:", ' '.join(sorted(new_future))
		can_choose |= new_future

	print "[**] What will you control next? "
	choice = raw_input("> ").strip()

	assert choice in can_choose
	return choice

def fire(arch, flag, arch_shellcode):
	cmd = [
		os.path.join(os.path.dirname(__file__), 'run_emu.sh'),
		arch,
	]
	env = {
		'FLAG': flag,
		'SHELLCODE': ''.join(base64.encodestring(arch_shellcode).split())
	}
	success = subprocess.Popen(cmd, env=env).wait() == 0
	print "[**] Checking for control..."
	return success

def input_shellcode(r=0x1000):
	global shellcode

	#print "Shellcode length:"
	#r = int(raw_input('> ').strip())
	shellcode = ""
	print "[**] Shellcode:"
	while len(shellcode) < r:
            d = sys.stdin.read(r-len(shellcode))
            if len(d) == 0:
                # it seems that healthcheck connect and disconnect
                # quickly without sending any data. we have to avoid
                # infinite read loop
                sys.exit(0)
            shellcode += d

def main(scorefile):
	print "[**] Who controls the past controls the future."
	print "[**] Who controls the present controls the past."
	print "[**]"
	print "[**] Take control."
	print "[**]"
	input_shellcode()

	print "[**] Press enter when ready."
	raw_input('> ')
	flag = "OOO" + ''.join(random.choice(string.digits) for _ in range(10))

	try:
		# controlled = ["amd64","ibm-1401","clemency","hexagon"]
		controlled = []
		while len(controlled) < max_control:
			choice = choose_arch(controlled)
			if choice and fire(choice, flag, shellcode):
				print "[**] You have obtained control over %s." % choice
				controlled.append(choice)
				print "[**] You control:", ' '.join(controlled)
			else:
				print "[**] You have reached the limits of your control."
				break
		else:
			print "[**] There is nothing else to control!"
	except Exception:
		print "[**] Something went wrong. Big Brother is watching you."

	print "[**] You achieved control over %d architectures." % len(controlled)
	if len(controlled) == 0:
		print "[**] If you want to keep a secret, you must also hide it from yourself."
	elif len(controlled) == 1:
		print "[**] A lunatic is just a minority of one."
	elif len(controlled) == 2:
		print "[**] Doublethink means the power of holding two contradictory beliefs in one's mind simultaneously, and accepting both of them."
	else:
		print "[**] The Revolution will be complete when the language is perfect."

	open(scorefile, 'w').write(str(len(controlled)) + '\n' + "Control attained: " + ' '.join(controlled) + '\n')

def timeout_handler(signum, frame):
    print "timeout!"
    os.kill(os.getpid(), signal.SIGKILL)

if __name__ == '__main__':
    signal.alarm(240)
    signal.signal(signal.SIGALRM, timeout_handler)
    main(scorefile=(sys.argv[1] if len(sys.argv) > 1 else '/score'))
