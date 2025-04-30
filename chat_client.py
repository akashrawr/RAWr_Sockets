# chat_client.py

import ctypes
import ctypes.wintypes

ws2_32 = ctypes.WinDLL('Ws2_32.dll')

AF_INET = 2
SOCK_STREAM = 1
IPPROTO_TCP = 6
INVALID_SOCKET = -1
PORT = 12345

class WSADATA(ctypes.Structure):
    _fields_ = [("wVersion", ctypes.wintypes.WORD),
                ("wHighVersion", ctypes.wintypes.WORD),
                ("szDescription", ctypes.c_char * 257),
                ("szSystemStatus", ctypes.c_char * 129),
                ("iMaxSockets", ctypes.wintypes.USHORT),
                ("iMaxUdpDg", ctypes.wintypes.USHORT),
                ("lpVendorInfo", ctypes.c_char_p)]

class sockaddr_in(ctypes.Structure):
    _fields_ = [("sin_family", ctypes.c_ushort),
                ("sin_port", ctypes.c_ushort),
                ("sin_addr", ctypes.c_uint32),
                ("sin_zero", ctypes.c_char * 8)]

def inet_addr(ip):
    return ctypes.windll.ws2_32.inet_addr(ip.encode())

def htons(x):
    return ctypes.windll.ws2_32.htons(x)

# Initialize Winsock
wsadata = WSADATA()
ws2_32.WSAStartup(0x0202, ctypes.byref(wsadata))

# Create socket
sock = ws2_32.socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

addr = sockaddr_in()
addr.sin_family = AF_INET
addr.sin_port = htons(PORT)
addr.sin_addr = inet_addr("127.0.0.1")
addr.sin_zero = b'\x00' * 8

# Connect to server
result = ws2_32.connect(sock, ctypes.byref(addr), ctypes.sizeof(addr))
if result != 0:
    print("Connection failed.")
    exit(1)

print("[CLIENT] Connected to server.")

buf = ctypes.create_string_buffer(1024)

try:
    while True:
        msg = input("You: ")
        ws2_32.send(sock, msg.encode(), len(msg), 0)
        n = ws2_32.recv(sock, buf, 1024, 0)
        if n <= 0:
            break
        reply = buf.raw[:n].decode()
        print("Server:", reply)
finally:
    ws2_32.closesocket(sock)
    ws2_32.WSACleanup()
    print("[CLIENT] Closed.")
