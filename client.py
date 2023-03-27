import grpc
from datetime import datetime
import pytz
import time
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
    try:
        position = int(input(f"Node {node_id}> Enter position on board (1-9): "))
        symbol = input(f"Node {node_id}> Enter your symbol: ")
    except:
        sOut("Invalid input format. Please try again!")
        return
    response = stub.SetSymbol(game_pb2.SetSymbolRequest(node_id=node_id, position=position, symbol=symbol, timestamp=time.time()))
    if not response.success:
        sOut(node_id, response.message)
        if response.message != "Game has not started!" and response.message != "Illegal turn!":
            setSymbol(stub, node_id)

def timeStringToTimestamp(time):
    today = datetime.today()
    utc_tz = pytz.timezone('UTC')
    dt = datetime.combine(today, datetime.strptime(time, '%H:%M:%S').time()).astimezone(utc_tz)
    return dt.timestamp()

def setNodeTime(stub, node_id):
    try:
        target_node = int(input(f"Node {node_id}> Target node ID: "))
        set_time = input(f"Node {node_id}> Set time to <hh:mm:ss>: ")
        timestamp = timeStringToTimestamp(set_time)
    except:
        sOut("Invalid input format. Please try again!")
        return
    response = stub.SetTime(game_pb2.SetTimeRequest(node_id=node_id, target_node_id=target_node, time=timestamp))
    if response.success:
        sOut(node_id, f"Node {target_node} time set to {set_time}")
    else:
        sOut(node_id, response.message)

def terminal(nodes, node_id, quit_event):
    address = nodes[node_id]
    with grpc.insecure_channel(address) as channel:
        stub = game_pb2_grpc.GameStub(channel)
        print(f"Node {node_id}> Enter 'Start-game' to get started or 'Quit' to abort.")
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
            elif command == 'Quit':
                quit_event.set()
            elif len(command):
                print(f"Node {node_id}> Unknown command. Please try again!")
            else:
                continue