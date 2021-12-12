import socket

s = socket.socket()
print("Socket successfully created")

port = 8888

s.bind(('', port))
print("Socket binded to %s" % (port))

s.listen(5)

print("Socket is listening")

while True:
    c, addr = s.accept()
    print("Connected by ", addr)
    c.send('Thank you for connecting')
    c.close()
