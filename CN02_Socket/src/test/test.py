import socket
import sys
from threading import *

try:
    listen_port = 8888
except KeyboardInterrupt:
    print("User interrupted")
    print("[*] Exiting...")
    sys.exit()

max_conn = 10
buffer_size = 8192


def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', listen_port))
        s.listen(max_conn)
        print("[*] Socket initializing")
        print("[*] Successful")
    except Exception as e:
        print("Error initializing")
        sys.exit(2)

    while 1:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            Thread(target=conn_string, args=(conn, data, addr)).start()
        except KeyboardInterrupt:
            s.close()
            print("[x] Shutting down server")
            sys.exit(1)

    s.close()


def conn_string(conn, data, addr):
    try:
        # first = (data.split('\n')[0])
        # url = first.split(' ')[1]

        lines = data.splitlines()
        while lines[len(lines) - 1] == "":
            lines.remove('')
        first = lines[0].split()
        url = str(first[1])

        pos = (url.find("://"))
        if (pos == -1):
            temp = url
        else:
            temp = url[(pos+3):]

        portpos = temp.find(":")
        serverpos = temp.find(":/")
        if serverpos == -1:
            serverpos = len(temp)
        server = ""
        port = -1
        if (portpos == -1 or serverpos < portpos):
            port = 80
            server = temp[:serverpos]
        else:
            port = int((temp[(portpos+1):])[:serverpos-portpos-1])
            server = temp[:portpos]

        proxy(server, port, conn, addr, data)
    except KeyboardInterrupt as e:
        pass


def proxy(server, port, conn, addr, data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(type(port))
        s.connect((server, port))
        s.sendall(data)

        while True:
            reply = s.recv(buffer_size)
            if(len(reply) > 0):
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar/1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % dar
                print(
                    "[*] Complete from %s => %s <=") % (str(addr[0]), str(dar))
            else:
                break

        s.close()
        conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)


start()
