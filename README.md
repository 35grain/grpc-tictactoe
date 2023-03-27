# To start playing
Make sure to generate the required client and server classes from the .proto file:

`python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. game.proto`

The `win32api` Python package is required for setting system time on Windows based machines.

Then simply run `python3 tictactoe.py`.

**NB! All nodes must start the game with administrator/sudo privileges to be able to modify system time!**
