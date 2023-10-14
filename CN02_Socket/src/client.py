import socket
import sys

try:
    host = input("Enter host proxy: ")
    port = int(input("Enter port proxy: "))
    while True:
        s = socket.socket()
        s.connect((host, port))
        domain = bytes(input("\n\n\nEnter domain: "), "utf-8")
        s.sendall(b'Host: ' + domain)
        print(s.recv(1024))
        s.close()
except KeyboardInterrupt:
    sys.exit(1)
