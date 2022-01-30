import threading
import socket


def connect_method():
    host = 'localhost'
    port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    return server


# dictionary containing key-value pairs (username,(ip,addr)) of peers
# ip_list = {"Devansh": ("192.168.1.8", 12020),
#            "Prashant": ("192.168.1.3", 12020)}
# client_conn = []
# users = []
users = []
ip_list=[]
client_conn = []


def broadcast(message, name):
    
    for client in client_conn:
        index = client_conn.index(client)
        msg = message.split('#')
        if msg[0] == "USERNAME" or msg[0]=="IP_LIST":
            client.send(message.encode('utf-8'))
        else:
            if users[index] == name:
                client.send(f"You: {message}".encode('utf-8'))
            else:
                client.send(f"{name}: {message}".encode('utf-8'))


def handle_client(client, name):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            msg=message.split("#")
            if msg[0] == "FILE_LIST":
                # Get files of client_name (msg[1]) from database
                print(f"Getting files of {msg[1]}")
                tag = "FILE_LIST#"
                file_list=tag+"Hello World"
                client.send(file_list.encode('utf-8'))
                # pass
            else:
                broadcast(message, name)
        except Exception as e:
            print("Error: ",e)
            index = client_conn.index(client)
            client_conn.remove(client)
            ip_list.pop(index)
            
            # client.send(f"USERNAME#{users}".encode('utf-8'))
            # client.send(f"IP_LIST#{ip_list}".encode('utf-8'))
            name = users[index]
            broadcast(f"USERNAME#{users}",name)
            broadcast(f"IP_LIST#{ip_list}",name)

            client.close()
            print(f'{name} has left the chat room!')
            users.remove(name)
            break


def Main():
    server = connect_method()
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('username?'.encode('utf-8'))
        name = client.recv(1024).decode("utf-8")
        ip_list.append(address)
        # Sending ip_list to client
        users.append(name)
        client_conn.append(client)
        print(f'{name} is connected now!')
        
        broadcast(f"USERNAME#{users}",name)
        broadcast(f"IP_LIST#{ip_list}",name)
        # broadcast(f'has connected to the chat room',name)
        # client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client, name,))
        thread.start()


if __name__ == "__main__":
    Main()
