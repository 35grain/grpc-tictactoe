# To start playing
Make sure to generate the required client and server classes from the .proto file:

`python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. game.proto`

Then simply run `python3 tictactoe.py`