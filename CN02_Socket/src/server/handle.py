import socket
import sys

BLACKLIST = "./blacklist.conf"
PATH403 = "./403.html"


def get403(f):
    try:
        return ''.join(open(f, 'r', encoding='utf-8').readlines())
    except Exception as e:
        print(e)


def printInfo(type, req, addr):
    print("\t", addr[0], "\t", type, req, "\t")


def checkBlocked(list):
    f = open(list, "r")
    res = []
    for line in f:
        res.append(line.strip())
    f.close()
    return res


def handle(conn, cli_addr):
    try:
        req = conn.recv(999999)
        # print(req)
    except Exception:
        pass
    req = str(req, encoding="utf-8")
    first_line = req.split("\n")[0]
    try:
        url = first_line.split(" ")[1]
        # print("___URL___: ", url)
    except Exception:
        url = ""

    BLOCKED = checkBlocked(BLACKLIST)

    for i in range(0, len(BLOCKED)):
        if (BLOCKED[i] in url):
            print("BLOCKED: ", url)
            conn.send(b"HTTP/1.1 403 Forbidden\n")
            conn.send(b"Content-Type: text/html\n")
            conn.send(b"\n\n")
            f = open(PATH403, 'r', encoding='utf-8')
            for line in f:
                conn.send(bytes(line.strip(), encoding="utf-8"))
            conn.close()
            sys.exit(1)

    printInfo("Request:", first_line, cli_addr)

    http_pos = url.find("://")
    if http_pos == -1:
        temp = url
    else:
        temp = url[(http_pos + 3):]

    port_pos = temp.find(":")
    server_pos = temp.find("/")
    if server_pos == -1:
        server_pos = len(temp)

    server, port = "", -1
    if port_pos == -1 or server_pos < port_pos:
        port = 80
        server = temp[:server_pos]
    else:
        port = int((temp[(port_pos + 1):])[: server_pos - port_pos - 1])
        server = temp[:port_pos]

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server, port))
        client.send(bytes(req, encoding="utf-8"))
        while 1:
            data = client.recv(999999)
            if data:
                conn.send(data)
            else:
                break
        client.close()
        conn.close()
    except Exception:
        if client:
            client.close()
        if conn:
            conn.close()
        printInfo("Reset:", first_line, cli_addr)
        sys.exit(1)
