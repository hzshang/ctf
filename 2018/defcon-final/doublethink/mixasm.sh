#! /bin/sh
#
# mixasm.sh
# Copyright (C) 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
#

python mixasm.py
python scripts/drive_emu.py mix ~/flag ./shellcode  | mixvm 2>/dev/null
