# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ngame.proto\"#\n\x10StartGameRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\"5\n\x11StartGameResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x12\n\x10ListBoardRequest\"D\n\x11ListBoardResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\r\n\x05\x62oard\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"\xe3\x01\n\x12UpdateBoardRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\r\n\x05\x62oard\x18\x02 \x03(\t\x12\x18\n\x10\x62oard_timestamps\x18\x03 \x03(\x01\x12\x31\n\x07players\x18\x04 \x03(\x0b\x32 .UpdateBoardRequest.PlayersEntry\x12\x0c\n\x04turn\x18\x05 \x01(\t\x12\x11\n\tgame_over\x18\x06 \x01(\x08\x12\x0f\n\x07message\x18\x07 \x01(\t\x1a.\n\x0cPlayersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"7\n\x13UpdateBoardResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"X\n\x10SetSymbolRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x10\n\x08position\x18\x02 \x01(\x05\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\x01\"5\n\x11SetSymbolResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x03 \x01(\t\"\r\n\x0bTimeRequest\"!\n\x0cTimeResponse\x12\x11\n\tnode_time\x18\x01 \x01(\x01\"1\n\x0bSyncRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x11\n\tsync_time\x18\x02 \x01(\x01\"0\n\x0cSyncResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"G\n\x0eSetTimeRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x16\n\x0etarget_node_id\x18\x02 \x01(\x05\x12\x0c\n\x04time\x18\x03 \x01(\x01\"3\n\x0fSetTimeResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"N\n\x0f\x45lectionRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x13\n\x0b\x65lection_id\x18\x02 \x01(\x05\x12\x15\n\rvisited_nodes\x18\x03 \x03(\x05\"4\n\x10\x45lectionResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\">\n\x15\x45lectionResultRequest\x12\x0e\n\x06leader\x18\x01 \x01(\x05\x12\x15\n\rvisited_nodes\x18\x02 \x03(\x05\"J\n\x16\x45lectionResultResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0e\n\x06leader\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t2\xe4\x03\n\x04Game\x12\x34\n\tStartGame\x12\x11.StartGameRequest\x1a\x12.StartGameResponse\"\x00\x12\x34\n\tListBoard\x12\x11.ListBoardRequest\x1a\x12.ListBoardResponse\"\x00\x12:\n\x0bUpdateBoard\x12\x13.UpdateBoardRequest\x1a\x14.UpdateBoardResponse\"\x00\x12\x34\n\tSetSymbol\x12\x11.SetSymbolRequest\x1a\x12.SetSymbolResponse\"\x00\x12(\n\x07GetTime\x12\x0c.TimeRequest\x1a\r.TimeResponse\"\x00\x12,\n\x0bSynchronize\x12\x0c.SyncRequest\x1a\r.SyncResponse\"\x00\x12.\n\x07SetTime\x12\x0f.SetTimeRequest\x1a\x10.SetTimeResponse\"\x00\x12\x31\n\x08\x45lection\x12\x10.ElectionRequest\x1a\x11.ElectionResponse\"\x00\x12\x43\n\x0e\x45lectionResult\x12\x16.ElectionResultRequest\x1a\x17.ElectionResultResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _UPDATEBOARDREQUEST_PLAYERSENTRY._options = None
  _UPDATEBOARDREQUEST_PLAYERSENTRY._serialized_options = b'8\001'
  _STARTGAMEREQUEST._serialized_start=14
  _STARTGAMEREQUEST._serialized_end=49
  _STARTGAMERESPONSE._serialized_start=51
  _STARTGAMERESPONSE._serialized_end=104
  _LISTBOARDREQUEST._serialized_start=106
  _LISTBOARDREQUEST._serialized_end=124
  _LISTBOARDRESPONSE._serialized_start=126
  _LISTBOARDRESPONSE._serialized_end=194
  _UPDATEBOARDREQUEST._serialized_start=197
  _UPDATEBOARDREQUEST._serialized_end=424
  _UPDATEBOARDREQUEST_PLAYERSENTRY._serialized_start=378
  _UPDATEBOARDREQUEST_PLAYERSENTRY._serialized_end=424
  _UPDATEBOARDRESPONSE._serialized_start=426
  _UPDATEBOARDRESPONSE._serialized_end=481
  _SETSYMBOLREQUEST._serialized_start=483
  _SETSYMBOLREQUEST._serialized_end=571
  _SETSYMBOLRESPONSE._serialized_start=573
  _SETSYMBOLRESPONSE._serialized_end=626
  _TIMEREQUEST._serialized_start=628
  _TIMEREQUEST._serialized_end=641
  _TIMERESPONSE._serialized_start=643
  _TIMERESPONSE._serialized_end=676
  _SYNCREQUEST._serialized_start=678
  _SYNCREQUEST._serialized_end=727
  _SYNCRESPONSE._serialized_start=729
  _SYNCRESPONSE._serialized_end=777
  _SETTIMEREQUEST._serialized_start=779
  _SETTIMEREQUEST._serialized_end=850
  _SETTIMERESPONSE._serialized_start=852
  _SETTIMERESPONSE._serialized_end=903
  _ELECTIONREQUEST._serialized_start=905
  _ELECTIONREQUEST._serialized_end=983
  _ELECTIONRESPONSE._serialized_start=985
  _ELECTIONRESPONSE._serialized_end=1037
  _ELECTIONRESULTREQUEST._serialized_start=1039
  _ELECTIONRESULTREQUEST._serialized_end=1101
  _ELECTIONRESULTRESPONSE._serialized_start=1103
  _ELECTIONRESULTRESPONSE._serialized_end=1177
  _GAME._serialized_start=1180
  _GAME._serialized_end=1664
# @@protoc_insertion_point(module_scope)
