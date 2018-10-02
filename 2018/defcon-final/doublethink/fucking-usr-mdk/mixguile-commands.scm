;; -*-scheme-*- -------------- mixguile-commands.scm :
;  mixvm commands implementation using the mixvm-cmd primitive
;  ------------------------------------------------------------------
;  Copyright (C) 2001, 2006, 2007 Free Software Foundation, Inc.
;
;  This program is free software; you can redistribute it and/or modify
;  it under the terms of the GNU General Public License as published by
;  the Free Software Foundation; either version 3 of the License, or
;  (at your option) any later version.
;
;  This program is distributed in the hope that it will be useful,
;  but WITHOUT ANY WARRANTY; without even the implied warranty of
;  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;  GNU General Public License for more details.
;
;  You should have received a copy of the GNU General Public License
;  along with this program; if not, write to the Free Software
;  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
;
;;

;; auxiliar functions for argument conversion
(define argsym->string
  (lambda (arg)
    (cond ((symbol? arg) (symbol->string arg))
	  ((string? arg) arg)
	  (else (error "Wrong argument type" arg)))))

(define argnsym->string
  (lambda (arg)
    (cond ((null? arg) "")
	  ((pair? arg) (argsym->string (car arg)))
	  (else (argsym->string arg)))))

(define argnum->string
  (lambda (arg)
    (cond ((number? arg) (number->string arg))
	  ((string? arg) arg)
	  (else (error "Wrong argument type" arg)))))

(define argnnum->string
  (lambda (arg)
    (cond ((null? arg) "")
	  ((pair? arg) (argnum->string (car arg)))
	  (else (argnum->string arg)))))

;;; mixvm commands

; preg
(define mix-preg
  (lambda (. reg)
    (mixvm-cmd "preg" (argnsym->string reg))))

; sreg
(define mix-sreg
  (lambda (reg val) (mixvm-cmd "sreg" (string-append (argsym->string reg)
						     " "
						     (argnum->string val)))))

; pmem
(define mix-pmem
  (lambda (from . to)
    (cond ((null? to) (mixvm-cmd "pmem" (argnum->string from)))
	  (else (mixvm-cmd "pmem"
			   (string-append (argnum->string from)
					  "-"
					  (argnnum->string to)))))))

; smem
(define mix-smem
  (lambda (cell val) (mixvm-cmd "smem" (string-append (argnum->string cell)
						      " "
						      (argnum->string val)))))

; pall
(define mix-pall (lambda () (mixvm-cmd "pall" "")))

; pc
(define mix-pc (lambda () (mixvm-cmd "pc" "")))

; pflags
(define mix-pflags (lambda () (mixvm-cmd "pflags" "")))

; sover
(define mix-sover
  (lambda (val)
    (mixvm-cmd "sover" (if val "T" "F"))))

; psym
(define mix-psym
  (lambda (. sym)
    (mixvm-cmd "psym" (argnsym->string sym))))

; ssym
(define mix-ssym
  (lambda (sym value)
    (mixvm-cmd "ssym"
	       (string-append
		(argsym->string sym) " " (argnum->string value)))))

; run
(define mix-run
  (lambda (. file)
    (mixvm-cmd "run" (argnsym->string file))))

; next
(define mix-next
  (lambda (. no)
    (mixvm-cmd "next" (argnnum->string no))))

; load
(define mix-load
  (lambda (file)
    (mixvm-cmd "load" (argsym->string file))))

; pstat
(define mix-pstat (lambda () (mixvm-cmd "pstat" "")))

; compile
(define mix-compile
  (lambda (. file)
    (mixvm-cmd "compile" (argnsym->string file))))

; devdir
(define mix-sddir
  (lambda (dir)
    (mixvm-cmd "sddir" dir)))

(define mix-pddir (lambda () (mixvm-cmd "pddir" "")))

; edit
(define mix-edit
  (lambda (. file)
    (mixvm-cmd "edit" (argnsym->string file))))

; help
(define mix-help
  (lambda (. cmd)
    (mixvm-cmd "help" (argnsym->string cmd))))

; pasm
(define mix-pasm (lambda () (mixvm-cmd "pasm" "")))

; sasm
(define mix-sasm
  (lambda (path)
    (mixvm-cmd "sasm" (argsym->string path))))

; pedit
(define mix-pedit (lambda () (mixvm-cmd "pedit" "")))

; sedit
(define mix-sedit
  (lambda (path)
    (mixvm-cmd "sedit" (argsym->string path))))

; sbp
(define mix-sbp
  (lambda (line)
    (mixvm-cmd "sbp" (argnum->string line))))

; sbp
(define mix-pline
  (lambda (. no)
    (mixvm-cmd "pline" (argnnum->string no))))

; cbp
(define mix-cbp
  (lambda (line)
    (mixvm-cmd "cbp" (argnum->string line))))

; sbpa
(define mix-sbpa
  (lambda (addr)
    (mixvm-cmd "sbpa" (argnum->string addr))))

; cbpa
(define mix-cbpa
  (lambda (addr)
    (mixvm-cmd "cbpa" (argnum->string addr))))


; sbpc
(define mix-sbpc (lambda () (mixvm-cmd "sbpc" "")))

; cbpc
(define mix-cbpc (lambda () (mixvm-cmd "cbpc" "")))

; sbpo
(define mix-sbpo (lambda () (mixvm-cmd "sbpo" "")))

; cbpo
(define mix-cbpo (lambda () (mixvm-cmd "cbpo" "")))

; sbpm
(define mix-sbpm
  (lambda (cell)
    (mixvm-cmd "sbpm" (argnum->string cell))))

; cbpm
(define mix-cbpm
  (lambda (cell)
    (mixvm-cmd "cbpm" (argnum->string cell))))

; sbpr
(define mix-sbpr
  (lambda (reg)
    (mixvm-cmd "sbpr" (argsym->string reg))))

; cbpr
(define mix-cbpr
  (lambda (reg)
    (mixvm-cmd "cbpr" (argsym->string reg))))

; pbt
(define mix-pbt
  (lambda (. num)
    (mixvm-cmd "pbt" (argnnum->string num))))

; timing
(define mix-stime
  (lambda (on)
    (mixvm-cmd "stime" (if on "on" "off"))))

(define mix-ptime (lambda () (mixvm-cmd "ptime" "")))

; timing
(define mix-strace
  (lambda (on)
    (mixvm-cmd "strace" (if on "on" "off"))))

; logging
(define mix-slog
  (lambda (on)
    (mixvm-cmd "slog" (if on "on" "off"))))

; w2d
(define mix-w2d
  (lambda (w)
    (mixvm-cmd "w2d" w)));

; weval
(define mix-weval
  (lambda (exp)
    (mixvm-cmd "weval" (argsym->string exp))))

; pprog
(define mix-pprog (lambda () (mixvm-cmd "pprog" "")))

; sprog
(define mix-psrc (lambda () (mixvm-cmd "psrc" "")))

