/*
Yong Lee
leey2@onid.oregonstate.edu
cs344-400
Homework 6
Some codes taken from http://ilab.cs.byu.edu/python/socket/echoserver.html

FLOP calculated by using:
	for (unsigned long int i=a; i > 0; i--){
		b = a/i;
	}
	
FLOP estimated to be 1,500,000,000, the whole program takes little longer than 15s, I'm guessing due to fork and stuff
*/
#define _BSD_SOURCE
#define _POSIX_SOURCE
#define _GNU_SOURCE

#include <sys/types.h> // basic system data types
#include <sys/socket.h> // basic socket definitions
#include <sys/time.h> // timeval struct for select
#include <netinet/in.h> // sockaddr_in and other internet defs
#include <arpa/inet.h> // inet(3) functions
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <strings.h> // for bzero
#include <sys/stat.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <sys/select.h>
#include <time.h>

#define LISTENQ 1

#define MAXLINE 4096
#define MAXSOCKADDR 128
#define BUFFSIZE 8192

#define SERV_PORT 9879
#define SERV_PORT_STR "9879"


void intr_sig1(int signal);
void intr_sig2(int signal);
void intr_sig3(int signal);

void intr_sig1(int sig){
    printf ("Process Interrupted.\n");
	exit(EXIT_SUCCESS);
}

void intr_sig2(int sig){
    printf ("Connection Hung up.\n");
	exit(EXIT_SUCCESS);
}

void intr_sig3(int sig){
    printf ("Process Quit.\n");
    exit(EXIT_SUCCESS);
}


int main (int argc, char **argv)
{
	unsigned long int ulimit=0;
	unsigned long int llimit=0;
	
	int count = 0;
	int count1 = 0;
	int n=0;
	
	int status;
	pid_t pid;
	int num = 1;
	
	int pnum[100];
	
	char temp[MAXLINE];
	char temp1[MAXLINE];
	char temp2[MAXLINE];
	char hostname[MAXLINE];
	char procid[MAXLINE];
	
	int sockfd;
	
	struct sockaddr_in servaddr;
	char sendline[MAXLINE] = "<flop>1500000000</flop>" ;
	char recvline[MAXLINE];
	char recvline1[MAXLINE];
	
	if (signal(SIGINT, intr_sig1) == SIG_ERR){
        printf("Error");
    }

    if (signal(SIGHUP, intr_sig2) == SIG_ERR){
        printf("Error");
    }

    if (signal(SIGQUIT, intr_sig3) == SIG_ERR){
        printf("Error");
    }
	
	
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(SERV_PORT);
	inet_pton(AF_INET, argv[1], &servaddr.sin_addr);
	
	connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
	
	pid = fork();
		if (pid < 0){
			//error
			fprintf (stderr, "Fork failed.\n");
		}
		else if (pid == 0){
			write(sockfd, sendline, strlen(sendline));
			
			bzero(recvline, MAXLINE);
			bzero(temp, MAXLINE);
			bzero(temp1, MAXLINE);
			
			if (read(sockfd, recvline, MAXLINE) == 0){
				perror("server terminated prematurely");
				exit(EXIT_FAILURE);
			}
			
			//Get lower limit
			while (recvline[count] != '>'){
				if (recvline[count] != '<'){
					temp[count1] = recvline[count];
					count1++;
				}
				count++;
			}
			
			if (strcmp(temp, "llimit") == 0){
				count++;
				count1 = 0;
				while (recvline[count] != '<'){
					temp1[count1] = recvline[count];
					count++;
					count1++;
				}
			}
			else
				printf("Error lower limit.\n");
			
			llimit = atoi(temp1);
			
			//Get upper limit
			while (recvline[count] != '>'){
				count ++;
			}
			
			count ++;
			
			while (recvline[count] != '>'){
				count ++;
			}
			
			count++;
			count1 = 0;
			while (recvline[count] != '<'){
				temp2[count1] = recvline[count];
				count++;
				count1++;
			}
			
			ulimit = atoi(temp2);
			
			
			//Check for perfect number
			count1 = 0;
			
			for (unsigned long int i=llimit; i <=ulimit; i++){
				n = 0;
				for(unsigned long int j=1; j<i; j++){
					if ((i % j) == 0){
						n = n + j;
					}
				}
				if (n == i){
					pnum[count1] = i;
					count1++;
				}
			}
			
			count = 0;
			
			bzero(sendline, MAXLINE);
			bzero(temp, MAXLINE);
			
			//Send data to server in xml format
			gethostname(hostname, MAXLINE);
			sprintf(procid, "%d", getpid());
			
			strcat(sendline, "<host>");
			strcat(sendline, hostname);
			strcat(sendline, "</host>");
			
			strcat(sendline, "<processid>");
			strcat(sendline, procid);
			strcat(sendline, "</processid>");
			
			strcat(sendline, "<llimit>");
			strcat(sendline, temp1);
			strcat(sendline, "</llimit>");
			
			strcat(sendline, "<ulimit>");
			strcat(sendline, temp2);
			strcat(sendline, "</ulimit>");
			
			count = 0;
			while (count < count1){
				strcat(sendline, "<pnum>");
				sprintf(temp, "%d", pnum[count]);
				strcat(sendline, temp);
				strcat(sendline, "</pnum>");
				//printf("%s\n", temp);
				count++;
			}
			
			strcat(sendline, "<end>");
			
			write(sockfd, sendline, strlen(sendline));
		}
		else{
			sleep(2); 
			bzero(recvline1, MAXLINE);
			if (read(sockfd, recvline1, MAXLINE) == 0){
				perror("server terminated prematurely");
				exit(EXIT_FAILURE);
			}
			
			if (strcmp(recvline1, "kill") == 0){
				kill (getpid(), SIGHUP);
			}
		
		}
		
	
		/* Wait for children to exit. */
		while (num > 0) {
		  pid = wait(&status);
		  --num;  
		}

	return 0;
}

