;; -*-scheme-*- -------------- mixguile-vm-stat.scm :
;  mixvm status functions
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

;; possible status index
(define mix-status-values (vector 'MIX_ERROR
				  'MIX_BREAK
				  'MIX_COND_BREAK
				  'MIX_HALTED
				  'MIX_RUNNING
				  'MIX_LOADED
				  'MIX_EMPTY))
;; return status as a simbol
(define mix-vm-status (lambda () (vector-ref mix-status-values (mixvm-status))))

;; check for a given status
(define mix-vm-status?
  (lambda (status) (eq? status (mix-vm-status))))

;; predicates for each possible status
(define mix-vm-error? (lambda () (mix-vm-status? 'MIX_ERROR)))
(define mix-vm-break? (lambda () (mix-vm-status? 'MIX_BREAK)))
(define mix-vm-cond-break? (lambda () (mix-vm-status? 'MIX_COND_BREAK)))
(define mix-vm-halted? (lambda () (mix-vm-status? 'MIX_HALTED)))
(define mix-vm-running? (lambda () (mix-vm-status? 'MIX_RUNNING)))
(define mix-vm-loaded? (lambda () (mix-vm-status? 'MIX_LOADED)))
(define mix-vm-empty? (lambda () (mix-vm-status? 'MIX_EMPTY)))


;; define hooks on break conditions

(define mix-make-conditional-hook
  (lambda (test hook)
    (lambda (arglist)
      (if (test) (hook (mix-src-line-no) (mix-loc))))))

(define mix-add-run-next-hook
  (lambda (hook)
    (mix-add-post-hook 'run hook)
    (mix-add-post-hook 'next hook)))


(define mix-add-break-hook
  (lambda (hook)
    (mix-add-run-next-hook (mix-make-conditional-hook mix-vm-break? hook))))

(define mix-add-cond-break-hook
  (lambda (hook)
    (mix-add-run-next-hook (mix-make-conditional-hook
			    mix-vm-cond-break? hook))))


