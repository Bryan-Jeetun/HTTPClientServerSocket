import os
import re
import time
import datetime
import socket
import threading
import random

# ================================
HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6060
ADDR = (HOST, PORT)


# ===============================


def open_static(filename, mode='rb'):
    try:
        with open(filename, mode) as f:
            data = f.read()
            ts = os.stat(filename).st_mtime
            last_modified = datetime.datetime \
                .utcfromtimestamp(ts) \
                .strftime('%a, %d %b %Y %H:%M:%S GMT')
            return data, last_modified
    except FileNotFoundError:
        return b'', 0


def build_header(status, file_type, last_modified):
    last_modified = f'Last-Modified: {last_modified}'.encode()
    content_type = ""
    if file_type == "html":
        content_type = "Content-Type: text/html; charset=utf-8"
    elif file_type == "jpg":
        content_type = "Content-Type: image/jpg"
    elif file_type == "png":
        content_type = "Content-Type: image/png"
    elif file_type == "css":
        content_type = "Content-Type: text/css"
    elif file_type == "js":
        content_type = "Content-Type: text/javascript"
    elif file_type == "ico":
        content_type = "Content-Type: image/x-icon"

    http_status = ""
    if status == "200":
        http_status = "HTTP/1.1 200 OK"
    elif status == "400":
        http_status = "HTTP/1.1 400 Bad Request"
    elif status == "404":
        http_status = "HTTP/1.1 404 Not Found"
    elif status == "500":
        http_status = "HTTP/1.1 500 Server Error"
    elif status == "304":
        http_status = "HTTP/1.1 304 Not Modified"

    return http_status.encode() + "\r\n".encode() \
           + content_type.encode() + "\r\n".encode() \
           + last_modified + "\r\n".encode() + "\r\n".encode()


def prepare_response(path, file_type):
    path = '.' + path
    body, last_modified = open_static(path, 'rb')
    if body:
        header = build_header('200', file_type, last_modified)
    else:
        header = build_header('404', file_type, last_modified)

    return header + body


def parse_request(request):
    headers = request.decode().split('\r\n')
    try:
        method, request, protocol = headers[0].split(' ')
    except ValueError:
        split = headers[0].split(' ')
        method = split[0]
        request = split[1]
        protocol = split[2]
    if request == '/': request = '/index.html'

    path = re.findall('[/a-z.]+', request)[0]

    try:
        file_type = path.split('.')[1]
    except IndexError:
        path = "/index.html"
        file_type = "html"

    if method == 'POST':
        body = headers[0]
        createFileOrWritePOST(path, body)
        print(f'Form data: {body}')

    if method == 'PUT':
        body = headers[0]
        createFileOrWritePUT(path, body)
        print(f'Form data: {body}')

    return method, path, file_type


def createFileOrWritePOST(fileName, postBody):
    f = open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + fileName, 'a+')
    split = postBody.split(" ")
    split = split[1]
    split = split.split("?")
    split = split[1]
    if "&" in split:
        parms = split.split("&")
        for par in parms:
            word = par.split("=")
            key = word[0]
            value = word[1]
            f.write("{" + key + " : " + value + "}" + "\n")
    else:
        split = split.split("=")
        key = split[0]
        value = split[1]
        f.write("{" + key + " : " + value + "}" + "\n")


def createFileOrWritePUT(fileName, postBody):
    fileName = fileName.split(".")[0]
    fileName = fileName + str(random.randint(0, 99999)) + '.txt'
    f = open('C:/Users/bryan/PycharmProjects/CN-HTTPSocket' + fileName, 'a+')
    split = postBody.split(" ")
    split = split[1]
    split = split.split("?")
    split = split[1]
    if "&" in split:
        parms = split.split("&")
        for par in parms:
            word = par.split("=")
            key = word[0]
            value = word[1]
            f.write("PUT Generated on " + time.ctime() + " {" + key + " : " + value + "}" + "\n")
    else:
        split = split.split("=")
        key = split[0]
        value = split[1]
        f.write("PUT Generated on " + time.ctime() + " {" + key + " : " + value + "}" + "\n")


def process_request(msg, client):
    method, path, file_type = parse_request(msg)
    response = prepare_response(path, file_type)
    client.send(response)
    client.close()
    print(f'({time.ctime()}) - {method} - {path}')


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}")

    while True:
        conn, addr = server.accept()
        message = conn.recv(4096)
        if message:
            threading.Thread(target=process_request, args=(message, conn)).start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()
