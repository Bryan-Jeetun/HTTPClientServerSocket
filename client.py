import socket

import requests
from bs4 import BeautifulSoup

HOST = 'www.tinyos.net'  # Server hostname
PORT = 80  # Port


def getResponse():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    request_header = b'GET / HTTP/1.0\r\nHost: www.tinyos.net\r\n\r\n'
    client_socket.sendall(request_header)

    response = ''
    while True:
        recv = client_socket.recv(1024)
        if not recv:
            break
        response += str(recv.decode() + "\n")
    client_socket.close()
    return response


def saveBodyToHtml():
    with open("index.html", 'wb') as fd:
        for line in getBody():
            fd.write(bytes(line.encode()))


def saveImagesLocally():
    soup = BeautifulSoup(getResponse(), "lxml")

    images = soup.find_all('img')

    for img in images:
        if img.has_attr('src'):
            r = requests.get("http://" + HOST + "/" + img['src'], allow_redirects=True)
            open(img['src'], 'wb').write(r.content)


def getBody():
    return getResponse()


if __name__ == '__main__':
    saveBodyToHtml()
    saveImagesLocally()
