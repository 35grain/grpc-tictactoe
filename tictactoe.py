import threading
import client
import server

if __name__ == '__main__':
    print("Enter participating node addresses (in the format ip:port):")
    nodes = {}
    for i in range(1,4):
        address = input(f"Node {i} address: ")
        nodes[i] = address
    print("Which of the nodes are you (select number)?")
    for id, addr in nodes.items():
        print(f"({id}) {addr}")
    node_id = int(input("I am: "))
    
    quit_event = threading.Event()
    
    client_thread = threading.Thread(target=client.terminal, args=(nodes, node_id, quit_event))
    client_thread.start()

    server_thread = threading.Thread(target=server.serve, args=(nodes, node_id, quit_event))
    server_thread.start()

    client_thread.join()
    server_thread.join()