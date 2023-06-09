import grpc
import time
import random
import sys
from datetime import datetime
import game_pb2
import game_pb2_grpc
from concurrent import futures

class GameServicer(game_pb2_grpc.GameServicer):
    def __init__(self, node_addresses, node_id):
        self.node_addresses = node_addresses
        self.node_ids = list(self.node_addresses.keys())
        self.node_id = node_id

        self.board = None
        self.board_timestamps = None
        self.game_active = False
        self.game_master = None
        self.players = {'X': None, 'O': None}
        self.turn = None
        self.election = {'id': 0, 'leader': None, 'announced': False}

    def StartGame(self, request, context):
        if not self.game_active:
            if self.game_master == self.node_id:
                players = self.node_ids.copy()
                players.remove(self.node_id)
                random.shuffle(players)

                self.players['X'], self.players['O'] = players[0], players[1]
                self.board = [""] * 9
                self.board_timestamps = [0.0] * 9
                self.turn = 'X'
                for node in self.node_ids:
                    try:
                        channel = grpc.insecure_channel(self.node_addresses[node])
                        stub = game_pb2_grpc.GameStub(channel)
                        response = stub.UpdateBoard(game_pb2.UpdateBoardRequest(node_id=self.node_id, board=self.board, board_timestamps=self.board_timestamps, players=self.players, turn=self.turn))
                        if not response.success:
                            return game_pb2.StartGameResponse(success=False, message=response.message)
                    except:
                        return game_pb2.StartGameResponse(success=False, message=f"Failed to reset game board for node {node}")
                self.game_active = True
                self.sOut(f"Game started by node {request.node_id}")
            elif self.node_id == request.node_id:
                synchronization = self.initSynchronization()
                if synchronization.success:
                    self.sOut(f"Node times synchronized.")
                else:
                    self.sOut(synchronization.message)
                    return game_pb2.StartGameResponse(success=False, message="Starting conditions unmet!")
                election = self.initElection()
                if election.success:
                    self.sOut(f"Election complete. New game-master is node {election.leader}.")
                else:
                    self.sOut(election.message)
                    return game_pb2.StartGameResponse(success=False, message="Starting conditions unmet!")
                
                self.sOut("Starting game!")
                for node in self.node_ids:
                    if self.node_id != node or node == election.leader:
                        try:
                            channel = grpc.insecure_channel(self.node_addresses[node])
                            stub = game_pb2_grpc.GameStub(channel)
                            response = stub.StartGame(game_pb2.StartGameRequest(node_id=self.node_id))
                            if not response.success:
                                return game_pb2.StartGameResponse(success=False, message=response.message)
                        except:
                            return game_pb2.StartGameResponse(success=False, message=f"Failed to initiate game for node {node}")
                if self.node_id != election.leader:
                    self.game_active = True
                    self.sOut(f"Game started by node {request.node_id}")
            else:
                self.game_active = True
                self.sOut(f"Game started by node {request.node_id}")
            return game_pb2.StartGameResponse(success=True)
        return game_pb2.StartGameResponse(success=False, message=f"Game already started on node {self.node_id}!")
    
    def getBoardState(self):
        positions = []
        for position, timestamp in zip(self.board, self.board_timestamps):
            symbol = position if len(position) else "empty"
            if timestamp != 0:
                time = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
                positions.append(f"{symbol}:{time}")
            else:
                positions.append(symbol)

        return ", ".join(positions)
    
    def UpdateBoard(self, request, context):
        if self.game_master == request.node_id:
            new_board = self.board == None or request.board == [""] * 9
            self.board = request.board
            self.board_timestamps = request.board_timestamps
            self.players = request.players
            self.turn = request.turn

            if request.message:
                self.sOut(request.message)

            if request.game_over:
                self.board = None
                self.board_timestamps = None
                self.game_active = False
                self.game_master = None
                self.players = {'X': None, 'O': None}
                self.turn = None
            else:
                if not new_board:
                    self.sOut("New board state:")
                    self.sOut(self.getBoardState())
                for player, node in self.players.items():
                    if node == self.node_id:
                        if new_board:
                            self.sOut(f"You are player {player}")
                        if self.turn == player:
                            self.sOut("It's your turn!")
                        else:
                            self.sOut("It's the other player's turn!")
                        break

            return game_pb2.UpdateBoardResponse(success=True)
        return game_pb2.UpdateBoardResponse(success=False, message="Illegal game board update request from non game-master node!")
    
    def ListBoard(self, request, context):
        if self.game_active:
            return game_pb2.ListBoardResponse(success=True, board=self.getBoardState())
        return game_pb2.ListBoardResponse(success=False, message="Game has not started!")
    
    def validMove(self, position, symbol):
        if self.board[position] == "" and symbol in ['X', 'O']:
            return True
        return False
    
    def checkCombination(self):
        # Check horizontal combinations
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2]:
                return self.board[i]

        # Check vertical combinations
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6]:
                return self.board[i]

        # Check diagonal combinations
        if self.board[0] == self.board[4] == self.board[8]:
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6]:
            return self.board[2]
        
        # Return "tie" if board is full without any winning combinations
        if "" not in self.board:
            return "tie"

        # Return None if no player has won yet
        return None
    
    def SetSymbol(self, request, context):
        if self.game_active:
            if self.game_master == self.node_id:
                position = request.position - 1
                symbol = request.symbol
                node = request.node_id
                timestamp = request.timestamp
                if self.turn == symbol and node == self.players[symbol]:
                    if self.validMove(position, symbol):
                        self.board[position] = symbol
                        self.board_timestamps[position] = timestamp
                        winner = self.checkCombination()
                        game_over = True if winner else False
                        if winner:
                            self.game_active = False
                            if winner == "tie":
                                message = "Game over! It's a tie!"
                            else:
                                message = f"Game over! Player {winner} wins!"
                        else:
                            message = f"Player {self.turn} sets symbol {symbol} at position {request.position}."
                        self.turn = 'O' if symbol == 'X' else 'X'
                        for node in self.node_ids:
                            try:
                                channel = grpc.insecure_channel(self.node_addresses[node])
                                stub = game_pb2_grpc.GameStub(channel)
                                response = stub.UpdateBoard(game_pb2.UpdateBoardRequest(node_id=self.node_id, board=self.board, board_timestamps=self.board_timestamps, players=self.players, turn=self.turn, game_over=game_over, message=message))
                                if not response.success:
                                    return game_pb2.SetSymbolResponse(success=False, message=response.message)
                            except:
                                return game_pb2.SetSymbolResponse(success=False, message=f"Unable to notify node {node} about move!")
                        return game_pb2.SetSymbolResponse(success=True)
                    else:
                        return game_pb2.SetSymbolResponse(success=False, message="Invalid position or symbol!")
                else:
                    return game_pb2.SetSymbolResponse(success=False, message="Illegal turn!")
            elif self.node_id == request.node_id:
                try:
                    channel = grpc.insecure_channel(self.node_addresses[self.game_master])
                    stub = game_pb2_grpc.GameStub(channel)
                    response = stub.SetSymbol(game_pb2.SetSymbolRequest(node_id=self.node_id, position=request.position, symbol=request.symbol, timestamp=request.timestamp))
                    if response.success:
                        return game_pb2.SetSymbolResponse(success=True)
                    else:
                        return game_pb2.SetSymbolResponse(success=False, message=response.message)
                except:
                    return game_pb2.SetSymbolResponse(success=False, message=f"Unable to request setting symbol from game-master!")
            return game_pb2.SetSymbolResponse(success=False, message="Illegal set symbol request from another node!")
        return game_pb2.SetSymbolResponse(success=False, message="Game has not started!")
        
    def GetTime(self, request, context):
        return game_pb2.TimeResponse(node_time=time.time())
    
    def initSynchronization(self):
        self.sOut("Initiating clock synchronization")

        difference_sum = 0
        for node in self.node_ids:
            try:
                channel = grpc.insecure_channel(self.node_addresses[node])
                stub = game_pb2_grpc.GameStub(channel)
                self_time = time.time()
                response = stub.GetTime(game_pb2.TimeRequest())
                node_time = response.node_time
                difference_sum += node_time - self_time
            except:
                return game_pb2.SyncResponse(success=False, message=f"Unable to get time from node {node}")
        difference_avg = difference_sum / len(self.node_ids)
        synchronized_time = time.time() + difference_avg
        for node in self.node_ids:
            try:
                channel = grpc.insecure_channel(self.node_addresses[node])
                stub = game_pb2_grpc.GameStub(channel)
                response = stub.Synchronize(game_pb2.SyncRequest(node_id=self.node_id, sync_time=synchronized_time))
            except:
                return game_pb2.SyncResponse(success=False, message=f"Unable to synchronize time with node {node}")
            
        self.sOut(f"Synchronized time: {datetime.fromtimestamp(synchronized_time)}")
        return game_pb2.SyncResponse(success=True)

    def Synchronize(self, request, context):
        synchronized_time = request.sync_time
        synchronized, message = self.setSystemTime(synchronized_time)
        return game_pb2.SyncResponse(success=synchronized, message=message)
    
    def _winSetTime(self, timestamp):
        try:
            import win32api
            
            dt = datetime.utcfromtimestamp(timestamp)
            win32api.SetSystemTime(dt.year, dt.month, dt.weekday(), dt.day, dt.hour, dt.minute, dt.second, 0)
            return True, ""
        except:
            return False, f"Unable to set system time for node {self.node_id}. Perhaps player has unsufficient privileges?"

    def _linuxSetTime(self, timestamp):
        try:
            import subprocess
            import shlex
            
            dt = datetime.fromtimestamp(timestamp)
            time_string = dt.isoformat()
            subprocess.call(shlex.split("sudo timedatectl set-ntp false"))
            subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
            return True, ""
        except:
            return False, f"Unable to set system time for node {self.node_id}"

    def _macSetTime(self, timestamp):
        try:
            import subprocess
            import shlex
            
            dt = datetime.fromtimestamp(timestamp)
            time_string = dt.strftime("%m%d%H%M%y.%S")
            subprocess.call(shlex.split("sudo date '%s'" % time_string))
            return True, ""
        except:
            return False, f"Unable to set system time for node {self.node_id}"
    
    def setSystemTime(self, timestamp):
        if sys.platform == 'linux2' or sys.platform == 'linux':
            return self._linuxSetTime(timestamp)
        elif sys.platform == 'darwin':
            return self._macSetTime(timestamp)
        elif sys.platform == 'win32':
            return self._winSetTime(timestamp)
    
    def SetTime(self, request, context):
        if self.game_active:
            if self.node_id == request.node_id == request.target_node_id or (self.game_master == request.node_id and request.target_node_id == self.node_id):
                success, message = self.setSystemTime(request.time)
                return game_pb2.SetTimeResponse(success=success, message=message)
            elif self.game_master == self.node_id:
                try:
                    channel = grpc.insecure_channel(self.node_addresses[request.target_node_id])
                    stub = game_pb2_grpc.GameStub(channel)
                    response = stub.SetTime(game_pb2.SetTimeRequest(node_id=self.node_id, target_node_id=request.target_node_id, time=request.time))
                    if response.success:
                        return game_pb2.SetTimeResponse(success=True)
                    return game_pb2.SetTimeResponse(success=False, message=response.message)
                except:
                    return game_pb2.SetTimeResponse(success=False, message=f"Unable to set time of node {request.target_node_id}")
            return game_pb2.SetTimeResponse(success=False, message=f"Only the game-master (node {self.game_master}) may change the internal clock of node {request.target_node_id}!")
        return game_pb2.SetTimeResponse(success=False, message="Game has not started!")

    def getNextNodeId(self):
        self_index = self.node_ids.index(self.node_id)
        if self_index + 1 >= len(self.node_ids):
            return self.node_ids[self_index + 1 - len(self.node_ids)]
        return self.node_ids[self_index + 1]
    
    def initElection(self):
        self.sOut("Initiating game-master election")
        next_node_id = self.getNextNodeId()
        election_id = self.election['id'] + 1
        try:
            channel = grpc.insecure_channel(self.node_addresses[next_node_id])
            stub = game_pb2_grpc.GameStub(channel)
            response = stub.Election(game_pb2.ElectionRequest(node_id=self.node_id, election_id=election_id, visited_nodes=[self.node_id]))
            if not response.success:
                return game_pb2.ElectionResponse(success=False, message=response.message)
        except:
            return game_pb2.ElectionResponse(success=False, message=f"Unable to pass election message to node {next_node_id}")
        
        while not self.election['leader']:
            time.sleep(1)

        self.sOut(f"End of election. New game-master is node {self.election['leader']}. Announcing result.")
        try:
            channel = grpc.insecure_channel(self.node_addresses[next_node_id])
            stub = game_pb2_grpc.GameStub(channel)
            response = stub.ElectionResult(game_pb2.ElectionResultRequest(leader=self.election['leader'], visited_nodes=[self.node_id]))
            if not response.success:
                return game_pb2.ElectionResultResponse(success=False, message=response.message)
        except:
            return game_pb2.ElectionResultResponse(success=False, message=f"Unable to announce game-master to node {next_node_id}")
        
        while not self.election['announced']:
            time.sleep(1)

        return game_pb2.ElectionResultResponse(success=True, leader=self.election['leader'])

    def Election(self, request, context):
        visited_nodes = request.visited_nodes
        if self.node_id not in visited_nodes:
            self.election['id'] = request.election_id
            visited_nodes.append(self.node_id)
            next_node_id = self.getNextNodeId()
            try:
                channel = grpc.insecure_channel(self.node_addresses[next_node_id])
                stub = game_pb2_grpc.GameStub(channel)
                response = stub.Election(game_pb2.ElectionRequest(node_id=self.node_id, election_id=request.election_id, visited_nodes=visited_nodes))
                if response.success:
                    return game_pb2.ElectionResponse(success=True)
                return game_pb2.ElectionResponse(success=False, message=response.message)
            except:
                return game_pb2.ElectionResponse(success=False, message=f"Unable to pass election message to node {next_node_id}")
        else:
            game_master = max(request.visited_nodes)
            self.election['leader'] = game_master
            return game_pb2.ElectionResponse(success=True, message="End of election.")
    
    def ElectionResult(self, request, context):
        visited_nodes = request.visited_nodes
        if self.node_id not in visited_nodes:
            self.game_master = request.leader
            self.sOut(f"New game-master is node {request.leader}")
            visited_nodes.append(self.node_id)
            next_node_id = self.getNextNodeId()
            try:
                channel = grpc.insecure_channel(self.node_addresses[next_node_id])
                stub = game_pb2_grpc.GameStub(channel)
                response = stub.ElectionResult(game_pb2.ElectionResultRequest(leader=request.leader, visited_nodes=visited_nodes))
                if response.success:
                    return game_pb2.ElectionResultResponse(success=True)
                return game_pb2.ElectionResultResponse(success=False, message=response.message)
            except:
                return game_pb2.ElectionResultResponse(success=False, message=f"Unable to announce game-master to node {next_node_id}")
        else:
            if self.election['leader'] in request.visited_nodes:
                self.sOut("Game-master announced to all nodes.")
                self.election['announced'] = True
                self.game_master = self.election['leader']
                return game_pb2.ElectionResultResponse(success=True, message="End of game-master announcment.")
            self.election['leader'] = None
            self.game_master = None
            return game_pb2.ElectionResultResponse(success=False, message="Selected game-master not in visited nodes list!")

    def sOut(self, message):
        print(f"Node {self.node_id}> {message}")

def serve(nodes, node_id, quit_event):
    node_addresses = nodes
    port = nodes[node_id].split(':')[-1]
    print(f"Node {node_id}> Starting server on port {port}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(node_addresses, node_id), server)

    server.add_insecure_port('[::]:' + str(port))
    server.start()

    while not quit_event.is_set():
        time.sleep(1)

    server.stop(0)
    print(f"Node {node_id}> Server stopped")