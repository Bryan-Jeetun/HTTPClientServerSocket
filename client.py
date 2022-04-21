from utils import folderUtil
import socket
from bs4 import BeautifulSoup
import sys

# ================================
HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6060
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!disconnect'


# ================================

def debug(message):
    print("[CLIENT] " + message)


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    sys.exit()

client_socket.connect((HOST, PORT))

debug("Setting header")
request_header = 'GET http://' + HOST + '/ HTTP/1.0\r\n\r\n'
client_socket.sendall(request_header.encode())

response = ''

while True:
    recv = client_socket.recv(512)
    if len(recv) < 1:
        break
    try:
        response += str(recv.decode())
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
    with open("indexCopy.html", 'wb') as fd:

        while True:
            data = client_socket.recv(20)
            if len(data) < 1:
                break
            new_data = new_data + data
        pos = new_data.find(b'\r\n\r\n')
        fd.write(new_data[pos + 4:])
    debug("Finished Saving html body")

# def saveBodyToHtml():
#     with open("index.html", 'wb') as fd:
#         for line in response:
#             fd.write(bytes(line.encode()))

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


def sendPostRequest():
    debug("Started sending post request")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = "?key1=test&key2=blah"

    header = f"POST /cool.html{data} HTTP/1.1 Host: {HOST}"

    request = header
    s.send(request.encode())
    s.close()
    debug("Finished sending post request")


def sendPutRequest():
    debug("Started sending put request")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = "?key1=test&key2=blah"

    header = f"PUT /cool.txt{data} HTTP/1.1 Host: {HOST}"

    request = header
    s.send(request.encode())
    s.close()
    debug("Finished sending put request")


def sendHeadRequest():
    debug("Started sending head request")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    header = f"HEAD / HTTP/1.1\r\nHost: {HOST}\r\nAccept: text/html\r\n\r\n"

    request = header
    s.sendall(request.encode())
    print(s.recv(512).decode())
    s.close()
    debug("Finished sending head request")


print('Done working for today')
saveBodyToHtml()
saveImagesLocally()
sendPostRequest()
sendPutRequest()
sendHeadRequest()
