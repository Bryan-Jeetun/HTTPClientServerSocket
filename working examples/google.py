import socket
import time

domain = 'www.google.com'
# must specify index.html for google
full_url = 'http://www.google.com/index.html'


mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect((domain, 80))
message = 'GET ' + full_url + ' HTTP/1.1\n\n'
mysock.sendall(bytes(message.encode()))

while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    print(data.decode())

mysock.close()
