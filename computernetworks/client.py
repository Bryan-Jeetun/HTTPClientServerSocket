import time

from utils import folderUtil
import socket
from bs4 import BeautifulSoup
import sys

# ================================
HOST = 'www.google.com' #socket.gethostbyname(socket.gethostname())
PORT = 80 #6060
ADDR = (HOST, PORT)
PROJECT_FOLDER = 'C:/Users/bryan/PycharmProjects/CN-HTTPSocket/'


# Replace this with the main project folder... Didn't have enough time to make it configurable :(
# ================================

def debug(message):
    print("[CLIENT] " + message)


def askForUserInput():
    print("=========================================")
    put = input(
        "1. Save server homepage to local\n2. Save server images to local\n3. Send a post request to server\n4. Send a put request to the server\n5. Send a head request to the server\n6. Shut down the client\n\nNumber: ")

    if put == "1":
        saveBodyToHtml()
    elif put == "2":
        saveImagesLocally()
    elif put == "3":
        sendPostRequest()
    elif put == "4":
        sendPutRequest()
    elif put == "5":
        sendHeadRequest()
    elif put == "6":
        debug("Shutting down client...")
        sys.exit()


debug("Started connecting")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

request_header = f'GET http://{HOST}/ HTTP/1.0\r\nHost: ' + HOST + '\r\n\r\n'
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((HOST, PORT))
    request_header = f'GET http://{HOST}/ HTTP/1.0\r\n\r\n'
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
    askForUserInput()


def saveImagesLocally():
    debug("Started Saving all images")
    soup = BeautifulSoup(response, "lxml")
    images = soup.find_all('img')

    for img in images:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((HOST, PORT))

        if img.has_attr('src'):

            req = 'GET ' "/" + img['src'] + ' HTTP/1.0\r\nHost: ' + HOST + '\r\n\r\n'

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
                dirName = PROJECT_FOLDER + img['src']
                folderUtil.makedirs(dirName)
                print("Directory ", dirName, " Created ")

                f = open(PROJECT_FOLDER + img['src'], 'wb')
                f.write(image)
                f.close()
        client_socket.close()
    debug("Finished Saving all images")
    askForUserInput()


def sendPostRequest():
    debug("Started sending post request")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    FILE = input("Write to what file, don't forget the extension!\nEnter:")
    DATA = input("What data should we send? (Use this format: key1=test&key2=blah)\nEnter:")

    header = f"POST /{FILE}?{DATA} HTTP/1.1 Host: {HOST}"

    s.send(header.encode())
    s.close()
    debug("Finished sending post request")
    askForUserInput()


def sendPutRequest():
    debug("Started sending put request")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    FILE = input("What should the name of the file be?\nEnter:")
    DATA = input("What data should we send? (Use this format: key1=value1&key2=value2)\nEnter:")

    header = f"PUT /{FILE}.txt?{DATA} HTTP/1.1 Host: {HOST}"

    request = header
    s.send(request.encode())
    s.close()
    debug("Finished sending put request")
    askForUserInput()


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

    askForUserInput()


debug(f"Connected to: {HOST}:{PORT} with main project folder set to {PROJECT_FOLDER}")
debug("Welcome to the HTTP Client Console")
askForUserInput()
