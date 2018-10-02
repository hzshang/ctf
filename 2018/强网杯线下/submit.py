#192.168.210.60~192.168.210.64
import requests
import json
import sys
import socket
import threading
import time

URL = 'http://1.1.1.1/Common/submitAnswer'
TOKEN = "13efdb729f62f24d749f852294a19994"
MAXLEN = 50

def submit_flag(flag):
    s = requests.post(url=URL, data={"answer": flag, "token": TOKEN})
    s.encoding = 'utf-8-sig'
    print s.json()['msg']

def handle_client(client_socket):
# print out what the client send
    req = client_socket.recv(1024)
    print "[*] Received: %s" % req
    # send back a packet
    if len(req.strip()) >= MAXLEN :
            client_socket.close()
    submit_flag(req.strip())
    client_socket.close()

def flag_server():
    bind_ip = "0.0.0.0"
    bind_port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))
    server.listen(1000)
    print "[*] Listening on %s:%d" % (bind_ip,bind_port)
    while True:
        client,addr = server.accept()
        print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
        # spin up our client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()

if __name__ == '__main__':
    flag_server()
