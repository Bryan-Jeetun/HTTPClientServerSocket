from utils import folderUtil
import socket
from bs4 import BeautifulSoup
import sys

HOST = 'www.example.com'  # Server hostname
PORT = 80  # Port

########################################

# Create the client socket and connect it to host + port
print('# Creating socket')
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

client_socket.connect((HOST, PORT))

# Send a header to the host
request_header = 'GET http://' + HOST + '/ HTTP/1.0\r\n\r\n'
client_socket.sendall(request_header.encode())

#####################################


response = ''
while True:  # While client is still receiving bytes, keep reading and decoding
    recv = client_socket.recv(512)
    if len(recv) < 1:
        break
    try:
        response += str(recv.decode() + "\n")
    except UnicodeDecodeError as e:
        response += str(recv.decode("ISO-8859-1") + "\n")


def saveBodyToHtml():
    with open("index.html", 'wb') as fd:
        for line in response:
            fd.write(bytes(line.encode()))


def saveImagesLocally():
    soup = BeautifulSoup(response, "lxml")
    images = soup.find_all('img')

    for img in images:
        #################################################
        # Create the client socket and connect it to host + port
        print('# Creating socket')
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        print('# Connecting to server, ' + HOST)
        client_socket.connect((HOST, PORT))

        #######################################
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

            print(image)

            try:
                f = open(img['src'], 'wb')
                f.write(image)
                f.close()
            except FileNotFoundError as err:
                print(err)
                dirName = 'C:/Users/bryan/PycharmProjects/CN-HTTPSocket/' + img['src']
                folderUtil.makedirs(dirName)
                print("Directory ", dirName, " Created ")

                f = open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket/' + img['src'], 'wb')
                f.write(image)
                f.close()


if __name__ == '__main__':
    saveBodyToHtml()
    saveImagesLocally()
