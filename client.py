import grpc
import game_pb2
import game_pb2_grpc

def sOut(node_id, message):
    print(f"Node {node_id}> {message}")

def startGame(stub, node_id):
    response = stub.StartGame(game_pb2.StartGameRequest(node_id=node_id))
    if not response.success:
        sOut(node_id, response.message)

def listBoard(stub, node_id):
    response = stub.ListBoard(game_pb2.ListBoardRequest())
    if response.success:
        sOut(node_id, response.board)
    else:
        sOut(node_id, response.message)

def setSymbol(stub, node_id):
    position = int(input(f"Node {node_id}> Enter position on board (1-9): "))
    symbol = input(f"Node {node_id}> Enter your symbol: ")
    response = stub.SetSymbol(game_pb2.SetSymbolRequest(node_id=node_id, position=position, symbol=symbol))
    if not response.success:
        sOut(node_id, response.message)
        if response.message != "Game has not started!":
            setSymbol(stub, node_id)

def setNodeTime(stub, node_id):
    return

def setTimeOut(stub, node_id):
    return

def terminal(port, node_id, quit_event):
    with grpc.insecure_channel('localhost:' + str(port)) as channel:
        stub = game_pb2_grpc.GameStub(channel)
        print("Enter 'Start-game' to get started or 'Quit' to abort.")
        while not quit_event.is_set():
            command = input(f"Node {node_id}> ")
            if command == 'Start-game':
                startGame(stub, node_id)
            elif command == 'List-board':
                listBoard(stub, node_id)
            elif command == 'Set-symbol':
                setSymbol(stub, node_id)
            elif command == 'Set-node-time':
                setNodeTime(stub, node_id)
            elif command == 'Set-time-out':
                setTimeOut(stub, node_id)
            elif command == 'Quit':
                quit_event.set()
            elif len(command):
                print("Unknown command. Please try again!")
            else:
                continue