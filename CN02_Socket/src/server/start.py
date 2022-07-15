
import _thread
from handle import *


def main():
    host = input("Enter host proxy: ")
    port = int(input("Enter port proxy: "))
    print("Proxy server started on port:", port)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.bind((host, port))
        client.listen(30)
    except Exception as e:
        print(e)
        if client:
            client.close()
        print("Socket error! Connection closed!")
        sys.exit(1)
    while 1:
        try:
            conn, cli_addr = client.accept()
            _thread.start_new_thread(handle, (conn, cli_addr))
        except KeyboardInterrupt:
            client.close()
            conn.close()
            print("Shutting down")
            sys.exit(1)


if __name__ == "__main__":
    main()
