;   ### ### ### ### ###
;   ### ### ### ### ###
;   ### ### ### ### ###
;   ### ### ### ### ###
;   ### ### ### ### ###

PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4

MOV ESP, EBP
POP EBP

MOV EAX, 1
XOR EBX, EBX
INT 0x80