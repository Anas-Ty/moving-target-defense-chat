import socket
import threading

# Logic based on [cite: 33, 35]
def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"\nclient: {msg}")
            else:
                break
        except:
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to Port 9999 as requested [cite: 33]
    server.bind(('0.0.0.0', 9999)) 
    server.listen(1)
    print("Server listening on port 9999...")

    client_socket, addr = server.accept()
    print(f"Connection from {addr}")

    # Start a thread to listen for incoming messages
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    # Main loop to send messages
    while True:
        msg = input()
        client_socket.send(msg.encode('utf-8'))

if __name__ == "__main__":
    start_server()