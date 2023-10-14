#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <ifaddrs.h>

#include <sys/socket.h>

#include <pthread.h>

#define PORT 8080
#define BUFFER_SIZE 1024
#define DELIMETER "\r\n\r\n"

int showIP();
int checkLogin(char *buffer, int *authorize);
char *mime(char *fileName);
void serverSendGET(char *header, char *content, int fsize, int newSockfd);
void completeGETfile(char *filename, char *content, char *header, int fsize, int socket);
void serverSendPOST(char *header, int newSockfd);
void completePOSTFile(char *uri, char *header, int newSockfd);
