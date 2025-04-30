# chat_server.py

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

def htons(x):
    return ctypes.windll.ws2_32.htons(x)

# Initialize Winsock
wsadata = WSADATA()
ws2_32.WSAStartup(0x0202, ctypes.byref(wsadata))

# Create server socket
server_socket = ws2_32.socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)

addr = sockaddr_in()
addr.sin_family = AF_INET
addr.sin_port = htons(PORT)
addr.sin_addr = 0  # INADDR_ANY
addr.sin_zero = b'\x00' * 8

ws2_32.bind(server_socket, ctypes.byref(addr), ctypes.sizeof(addr))
ws2_32.listen(server_socket, 1)

print(f"[SERVER] Listening on port {PORT}...")

client_socket, _ = ws2_32.accept(server_socket, None, None)
print("[SERVER] Client connected.")

buf = ctypes.create_string_buffer(1024)

try:
    while True:
        n = ws2_32.recv(client_socket, buf, 1024, 0)
        if n <= 0:
            break
        msg = buf.raw[:n].decode()
        print("Client:", msg)
        reply = input("You: ")
        ws2_32.send(client_socket, reply.encode(), len(reply), 0)
finally:
    ws2_32.closesocket(client_socket)
    ws2_32.closesocket(server_socket)
    ws2_32.WSACleanup()
    print("[SERVER] Closed.")
