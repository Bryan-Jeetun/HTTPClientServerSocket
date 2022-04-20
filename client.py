from utils import folderUtil
import socket
from bs4 import BeautifulSoup
import sys

HOST = 'www.tinyos.net'  # Server hostname
PORT = 80  # Port

def debug(message):
    print("#DEBUG")
    print("-> " + message)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    sys.exit()

client_socket.connect((HOST, PORT))

request_header = 'GET http://' + HOST + '/ HTTP/1.0\r\n\r\n'
client_socket.sendall(request_header.encode())

response = ''

while True:
    recv = client_socket.recv(512)
    if len(recv) < 1:
        break
    try:
        response += str(recv.decode() + "\n")
    except UnicodeDecodeError as e:
        response += str(recv.decode("ISO-8859-1") + "\n")
client_socket.close()


def saveBodyToHtml():
    debug("Started Saving html body")
    new_data = b''

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.exit()

    client_socket.connect((HOST, PORT))
    request_header = 'GET http://' + HOST + '/ HTTP/1.0\r\n\r\n'
    client_socket.sendall(request_header.encode())
    with open("index.html", 'wb') as fd:

        while True:
            data = client_socket.recv(20)
            if len(data) < 1:
                break
            new_data = new_data + data
        pos = new_data.find(b'\r\n\r\n')
        fd.write(new_data[pos + 4:])
    debug("Finished Saving html body")


def saveImagesLocally():
    debug("Started Saving all images")
    soup = BeautifulSoup(response, "lxml")
    images = soup.find_all('img')

    for img in images:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            sys.exit()

        client_socket.connect((HOST, PORT))

        if img.has_attr('src'):

            req = 'GET ' "/" + img['src'] + ' HTTP/1.0\r\nHost: ' + HOST + '\r\n\r\n'
            # (!) Hier ipv / domain/ aangepast

            client_socket.sendall(req.encode())
            reply = b''

            while True:
                data = client_socket.recv(1024)
                if not data: break
                reply += data

            headers = reply.split(b'\r\n\r\n')[0]
            image = reply[len(headers) + 4:]

            try:
                f = open(img['src'], 'wb')
                f.write(image)
                f.close()
            except FileNotFoundError:
                dirName = 'C:/Users/bryan/PycharmProjects/CN-HTTPSocket/' + img['src']
                folderUtil.makedirs(dirName)
                print("Directory ", dirName, " Created ")

                f = open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket/' + img['src'], 'wb')
                f.write(image)
                f.close()
        client_socket.close()
    debug("Finished Saving all images")


if __name__ == '__main__':
    saveBodyToHtml()
    saveImagesLocally()

