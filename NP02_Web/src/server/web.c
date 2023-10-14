#include "Header.h"

// Show all IP of local machine except for loopback IP
int showIP()
{
    struct ifaddrs *addresses;
    if (getifaddrs(&addresses) == -1)
    {
        perror("Error:");
        return -1;
    }

    struct ifaddrs *address = addresses;
    while (address)
    {
        // Check all the address if they are IPv4
        int family = address->ifa_addr->sa_family;
        if (family == AF_INET)
        {
            // Remove loopback address as it is not needed
            // to display for other machine to connect
            if (strcmp(address->ifa_name, "lo") != 0)
            {
                // Display the IP and port of the Server
                printf("%s", "Access server at: ");
                char ap[100];
                const int family_size = sizeof(struct sockaddr_in);
                getnameinfo(address->ifa_addr, family_size, ap, sizeof(ap), 0, 0, 1);
                printf("%s:%d\n", ap, PORT);
            }
        }
        address = address->ifa_next;
    }
    freeifaddrs(addresses);
    return 0;
}

// Check input from user for POST
// username: admin password: admin for images.html. Otherwise, return to index.html
int checkLogin(char *buffer, int *authorize)
{
    char *dup_buffer = strdup(buffer);
    char *authen = strstr(dup_buffer, "uname");
    if (strcmp(authen, "uname=admin&psw=admin&remember=on") == 0 || strcmp(authen, "uname=admin&psw=admin") == 0)
    {
        *authorize = 1;
        return 1;
    }
    return 0;
}

// Find mime type for Content-Type of header
char *mime(char *fileName)
{
    char *mimeType;
    if (strcmp(fileName, "") == 0)
    {
        mimeType = "text/html\r\n";
    }
    else
    {
        char *fileNameDup = strdup(fileName);
        char *name = strtok(fileNameDup, ".");
        char *extensions = strtok(NULL, ".");

        if (strcmp(extensions, "png") == 0)
        {
            mimeType = "images/png\r\n";
        }
        else if (strcmp(extensions, "jpg") == 0)
        {
            mimeType = "images/jpg\r\n";
        }
        else if (strcmp(extensions, "css") == 0)
        {
            mimeType = "text/css\r\n";
        }
        else
        {
            mimeType = "text/html\r\n";
        }
    }
    return mimeType;
}

void serverSendGET(char *header, char *content, int fsize, int newSockfd)
{
    int valWrite = write(newSockfd, header, strlen(header));
    char *data = (char *)content;
    while (fsize > 0)
    {
        if (fsize < BUFFER_SIZE)
        {
            int len = write(newSockfd, data, fsize);
            break;
        }
        else
        {
            int len = write(newSockfd, data, BUFFER_SIZE);
            if (len <= 0)
                break;
            data += len;
            fsize -= len;
        }
    }
    free(content);
    fflush(stdin);
    fflush(stdout);
    close(newSockfd);
}

void completeGETfile(char *filename, char *content, char *header, int fsize, int socket)
{
    // char public[BUFFER_SIZE] = "app/web/" ;
    // The above line is for testing purpose on Docker, the below is for running on local machine.
    char public[BUFFER_SIZE] = "../src/public";
    strcat(public, filename);
    // Open and read file into content as data to send
    FILE *fp = fopen(public, "rb");
    if (fp == NULL)
    {
        perror("Error:");
        return;
    }
    fseek(fp, 0, SEEK_END);
    fsize = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    content = malloc(fsize + 1);
    fread(content, fsize, 1, fp);
    fclose(fp);

    // Use the size of the file to prepare for the field Content-Length
    char conLen[] = "Content-Length: ";
    int length = snprintf(NULL, 0, "%d", fsize);
    char *len = malloc(length + 1);
    snprintf(len, length + 1, "%d", fsize);
    strcat(conLen, len);
    free(len);

    // Use the filename to determine mimeType for Content-Type
    // Attach fields of Content-Type and Content-Length into the header
    strcat(header, mime(filename));
    strcat(header, conLen);
    // Finally attach "\r\n\r\n" defined as DELIMETER before calling function to send
    strcat(header, DELIMETER);
    serverSendGET(header, content, fsize, socket);
}

void serverSendPOST(char *header, int newSockfd)
{
    // Because there is no data just need to send header to move to the right folder to GET
    int valWrite = write(newSockfd, header, strlen(header));
    if (valWrite < 0)
        perror("Web Server (write)");
    fflush(stdin);
    fflush(stdout);
    close(newSockfd);
}

void completePOSTFile(char *uri, char *header, int newSockfd)
{
    // Compared to GET, POST doesn't need to open file only need to know the location
    //  to attach to the Moved Permanently field
    char *directory = uri + 1;
    // strcat(public,directory);
    strcat(header, uri);
    strcat(header, "\r\n");

    // Find the Mime type for Content-Type field before attach to header
    strcat(header, "Content-Type: ");
    strcat(header, mime(directory));

    // Finally attach "\r\n\r\n" defined as DELIMETER before calling function to send
    strcat(header, DELIMETER);
    serverSendPOST(header, newSockfd);
}