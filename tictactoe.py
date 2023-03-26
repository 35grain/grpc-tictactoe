import threading
import client
import server

if __name__ == '__main__':
    port = int(input("Enter server port to use: "))
    node_id = int(input("Enter node id to use: "))
    quit_event = threading.Event()
    
    client_thread = threading.Thread(target=client.terminal, args=(port, node_id, quit_event))
    client_thread.start()

    server_thread = threading.Thread(target=server.serve, args=(port, node_id, quit_event))
    server_thread.start()

    client_thread.join()
    server_thread.join()