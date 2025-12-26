import socket
import time
import sys
# This imports the logic Student A wrote
import otp_generator 

# Configuration
SECRET_KEY = "project_phantom_key" # Must match the server's key exactly
SERVER_IP = "127.0.0.1"            # Use localhost for testing, change to Student A's IP later

def start_dynamic_client():
    print(f"[-] Client starting. Hunting for server on {SERVER_IP}...")

    while True:
        # 1. Ask the 'Brain' which port is currently open [cite: 57]
        # We use the same key so we get the same number as the server
        target_port = otp_generator.generate_token(SECRET_KEY)
        
        try:
            # 2. Create a fresh socket for every attempt
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2.0) # Set a short timeout so we don't freeze if it fails
            
            # 3. Try to connect to the calculated port [cite: 58]
            # print(f"[*] Trying Port {target_port}...") 
            client.connect((SERVER_IP, target_port))
            
            print(f"\n[+] SUCCESS! Connected to Port {target_port}")
            print("[+] Type a message to send (or 'exit' to quit):")

            # --- Chat Loop (Keep connection alive until server hops) ---
            while True:
                msg = input("You: ")
                if msg.lower() == 'exit':
                    client.close()
                    sys.exit()
                
                client.send(msg.encode('utf-8'))
                
                # Wait for reply
                try:
                    data = client.recv(1024)
                    if not data:
                        # If data is empty, server likely closed the connection (Hopped)
                        print("[-] Server disconnected (Port closed).")
                        break 
                    print(f"Server: {data.decode('utf-8')}")
                except socket.timeout:
                    # Just in case read times out
                    continue
                except OSError:
                    break

        except ConnectionRefusedError:
            # 4. Error Handling: The server isn't on this port yet, or just moved 
            # We catch the error and the loop restarts, calculating the port again.
            print(f"[-] Port {target_port} refused. Retrying...", end='\r')
            time.sleep(1) # Wait a bit before retrying to avoid spamming CPU
            
        except socket.timeout:
            print(f"[-] Connection timed out on {target_port}. Retrying...", end='\r')
            
        except Exception as e:
            print(f"[!] Unexpected Error: {e}")
            time.sleep(1)
        
        finally:
            # Always clean up the old socket before making a new one
            client.close()

if __name__ == "__main__":
    start_dynamic_client()