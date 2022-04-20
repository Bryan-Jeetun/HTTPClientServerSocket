from utils import dir
import socket
from bs4 import BeautifulSoup

HOST = 'www.google.com'  # Server hostname
PORT = 80  # Port

# Create the client socket and connect it to host + port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
client_socket.connect(server_address)

#Send a header to the host
request_header = b'GET /index.html HTTP/1.0\r\n\r\n'
client_socket.sendall(request_header)

response = ''
while True:  # While client is still receiving bytes, keep reading and decoding
    recv = client_socket.recv(1024)
    if len(recv) < 1:
        break
    try:
        response += str(recv.decode() + "\n")
    except UnicodeDecodeError as e:
        response += str(recv.decode("ISO-8859-1") + "\n")
client_socket.close()



def saveBodyToHtml():
    with open("index.html", 'wb') as fd:
        for line in response:
            fd.write(bytes(line.encode()))


def saveImagesLocally():
    soup = BeautifulSoup(response, "lxml")
    images = soup.find_all('img')

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    for img in images:
        if img.has_attr('src'):

            #####################
            req = 'GET ' + HOST + img['src'] + ' HTTP/1.0\r\n\r\n'
            print(req)
            client_socket.send(req.encode())

            picture = b''
            while True:
                data = client_socket.recv(5120)
                if len(data) < 1:
                    break
                picture = picture + data
            client_socket.close()

            pos = picture.find(b"\r\n\r\n")
            picture = picture[pos + 4:]

            try:
                f = open(img['src'], 'wb')
                f.write(picture)
                f.close()
            except FileNotFoundError as e:
                dirName = 'C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + img['src']
                dir.makedirs(dirName)
                print("Directory ", dirName, " Created ")
                f = open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + img['src'], 'wb')
                f.write(picture)
                f.close()



if __name__ == '__main__':
    saveImagesLocally()
    saveBodyToHtml()
