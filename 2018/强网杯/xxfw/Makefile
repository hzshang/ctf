#
# Makefile
# Copyright (C) 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
PROG=shellcode

all:main.c
	@echo "Makefile needs your attention"
	gcc $^ -o $(PROG) -z execstack -g
clean:
	rm -f $(PROG)
