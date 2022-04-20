import os
import socket

import requests
from bs4 import BeautifulSoup

HOST = 'www.google.com'  # Server hostname
PORT = 80  # Port


def getResponse():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    request_header = b'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
    client_socket.sendall(request_header)

    r = requests.get('http://www.google.com')

    response = ''
    while True:
        if r.encoding is None:
            recv = client_socket.recv(1024)
            if not recv:
                break
            response += str(recv.decode() + "\n")
        else:
            recv = client_socket.recv(1024)
            if not recv:
                break
            response += str(recv.decode(r.encoding) + "\n")
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
            print("http://" + HOST + "/" + img['src'])
            try:
                open(img['src'], 'wb').write(r.content)
            except FileNotFoundError as e:
                dirName = 'C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + img['src']
                makedirs(dirName)
                print("Directory ", dirName, " Created ")
                open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + img['src'], 'wb').write(r.content)
                continue
            # open(img['src'], 'wb').write(r.content)


def getBody():
    return getResponse()


def makedirs(name, mode=0o777, exist_ok=False):
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        try:
            makedirs(head, exist_ok=exist_ok)
        except FileExistsError:
            pass
        cdir = os.curdir
        if isinstance(tail, bytes):
            cdir = bytes(os.curdir, 'ASCII')
        if tail == cdir:
            return
    try:
        print(name)
        if '.' in name:
            print("Skipping cuz it's a file")
            pass
        else:
            os.mkdir(name, mode)
    except OSError:
        if not exist_ok or not os.path.isdir(name):
            raise


if __name__ == '__main__':
    saveBodyToHtml()
    saveImagesLocally()
