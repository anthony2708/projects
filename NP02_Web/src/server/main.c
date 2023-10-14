#include "Header.h"

int main()
{
    // Header for response
    char GET_header[] = "HTTP/1.1 200 OK\r\n"
                        "Connection: keep-alive \r\n"
                        "Content-Type: ";
    char POST_header[] = "HTTP/1.1 301 Moved Permanently\r\n"
                         "Location: ";
    char header[BUFFER_SIZE] = {};
    char buffer[BUFFER_SIZE];
    int option = 1;
    char *content;
    int fsize = 0;
    int authorize = 0;
    // Create a socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1)
    {
        perror("Web Server (socket)");
        return 1;
    }
    printf("Socket created successfully\n");

    // Create the address to bind the socket to
    struct sockaddr_in server_addr;
    int server_addrlen = sizeof(server_addr);

    // Bind port and all address of local machine to server_addr
    memset(&server_addr, '\0', server_addrlen);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Display all address that is able to connect to server and the port to access

    showIP();

    // Create client address
    struct sockaddr_in client_addr;
    int client_addrlen = sizeof(client_addr);

    // Allow the socket to bind using already used socket
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));
    // Bind the socket to the address
    bind(sockfd, (struct sockaddr *)&server_addr, server_addrlen);
    printf("Socket successfully bound to address\n");

    // Listen for incoming connections
    if (listen(sockfd, SOMAXCONN) != 0)
    {
        perror("Web Server (listen)");
        return 1;
    }
    printf("Server listening for connections\n");

    for (;;)
    {
        // Accept incoming connections
        int newSockfd = accept(sockfd, (struct sockaddr *)&server_addr,
                               (socklen_t *)&server_addrlen);
        if (newSockfd < 0)
        {
            perror("Web Server (accept)");
            continue;
        }
        printf("Connection accepted\n");

        // Get client address
        int sockN = getsockname(newSockfd, (struct sockaddr *)&client_addr,
                                (socklen_t *)&client_addrlen);
        if (sockN < 0)
        {
            perror("Web Server (getsockname)");
            continue;
        }

        // Read from the socket
        char buffer[BUFFER_SIZE] = {0};
        int valRead = read(newSockfd, buffer, BUFFER_SIZE);
        if (valRead < 0)
        {
            perror("Web Server (read)");
            continue;
        }

        // Read the request get most important part which are method, uri
        char method[BUFFER_SIZE], uri[BUFFER_SIZE], version[BUFFER_SIZE];
        sscanf(buffer, "%s %s %s", method, uri, version);
        printf("[%s:%u] %s %s %s\n", inet_ntoa(client_addr.sin_addr),
               ntohs(client_addr.sin_port), method, version, uri);

        // printf("%s\n",buffer);
        // Handle GET request
        if (strcmp(method, "GET") == 0)
        {
            strcpy(header, GET_header);
            // Direct to index to handle if access website
            if (strcmp(uri, "/") == 0)
            {
                completeGETfile("index.html", content, header, fsize, newSockfd);
            }
            // Direct to index to handle if try to get into /images.html without login
            else if (strcmp(uri, "/images.html") == 0 && authorize == 0)
            {
                completeGETfile("index.html", content, header, fsize, newSockfd);
            }
            // Handle other request like css, jpg, png
            else
            {
                char *directory = uri + 1;
                completeGETfile(directory, content, header, fsize, newSockfd);
            }
        }
        // Handle POST request
        else if (strcmp(method, "POST") == 0)
        {
            strcpy(header, POST_header);
            if (checkLogin(buffer, &authorize))
            {
                completePOSTFile(uri, header, newSockfd);
            }
            else
            {
                completePOSTFile("/", header, newSockfd);
            }
        }
    }
    return 0;
}
