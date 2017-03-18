	.data
ww_:	.space 12
vvv_:	.space 4
vv_:	.space 4
v_:	.space 4
	.text
	.globl pp
	.ent pp
pp:	
	sw $fp, -16($sp)
	sw $ra, -20($sp)
	sub $fp, $sp, 12
	sub $sp, $fp, 8
	lw $t8, 8($fp)
	addi $t3, $0, 1
	sw $t3, 0($t8)
	add $sp, $fp, 12
	lw $ra, -8($fp)
	lw $fp, -4($fp)
	jr $ra
	.text
	.globl main
	.ent main
main:	
	lw $t7, v_
	beq $t7, $0, C0
C1:	
	lw $t6, ww_+8
	beq $t6, $0, C2
C3:	
	addi $t1, $0, 1
	sw $t1, v_
	b, I0
C2:	
	sw $0, v_
I0:	
C0:	
	addi $t2, $0, 3
	addi $t4, $0, 4
	ble $t2, $t4, C4
C5:	
L0:	
	beq $0, $0, C6
C7:	
	addi $t5, $0, 1
	addi $t0, $0, 1
	bne $t5, $t0, C8
C9:	
	li $v0, 11
	li $a0, '\n'
	syscall
	b, I1
C8:	
	addi $a0, $0, 7
	li $v0, 1
	syscall
I1:	
	b, L0
C6:	
C4:	
	li $v0, 10
	syscall
	.end main