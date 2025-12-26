import socket
import threading

# Logic based on [cite: 34, 35]
def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if msg:
                print(f"\nServer: {msg}")
        except:
            print("Connection lost.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to localhost (127.0.0.1) for testing, Port 9999 
    # When testing with Student A, change '127.0.0.1' to their IP address.
    client.connect(('127.0.0.1', 9999))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        msg = input()
        client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    start_client()