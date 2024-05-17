# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: redpepper/common/messages.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fredpepper/common/messages.proto\x12\tredpepper\"\xdc\x03\n\x07Message\x12$\n\x04type\x18\x01 \x01(\x0e\x32\x16.redpepper.MessageType\x12.\n\x0c\x63lient_hello\x18\n \x01(\x0b\x32\x16.redpepper.ClientHelloH\x00\x12.\n\x0cserver_hello\x18\x0b \x01(\x0b\x32\x16.redpepper.ServerHelloH\x00\x12\x1d\n\x03\x62ye\x18\r \x01(\x0b\x32\x0e.redpepper.ByeH\x00\x12\x1f\n\x04ping\x18\x0e \x01(\x0b\x32\x0f.redpepper.PingH\x00\x12\x1f\n\x04pong\x18\x0f \x01(\x0b\x32\x0f.redpepper.PongH\x00\x12%\n\x07\x63ommand\x18\x14 \x01(\x0b\x32\x12.redpepper.CommandH\x00\x12*\n\x06\x63\x61ncel\x18\x15 \x01(\x0b\x32\x18.redpepper.CommandCancelH\x00\x12*\n\x06status\x18\x16 \x01(\x0b\x32\x18.redpepper.CommandStatusH\x00\x12.\n\x0c\x64\x61ta_request\x18\x1e \x01(\x0b\x32\x16.redpepper.DataRequestH\x00\x12\x30\n\rdata_response\x18\x1f \x01(\x0b\x32\x17.redpepper.DataResponseH\x00\x42\t\n\x07message\"\x15\n\x03\x42ye\x12\x0e\n\x06reason\x18\x01 \x01(\t\"-\n\x0b\x43lientHello\x12\x10\n\x08\x63lientID\x18\x01 \x01(\t\x12\x0c\n\x04\x61uth\x18\x02 \x01(\t\"\x1e\n\x0bServerHello\x12\x0f\n\x07version\x18\x01 \x01(\r\"\x14\n\x04Ping\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x05\"\x14\n\x04Pong\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x05\"8\n\x07\x43ommand\x12\x11\n\tcommandID\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t\"\"\n\rCommandCancel\x12\x11\n\tcommandID\x18\x01 \x01(\x05\"\xc7\x01\n\rCommandStatus\x12\x11\n\tcommandID\x18\x01 \x01(\x05\x12/\n\x06status\x18\x02 \x01(\x0e\x32\x1f.redpepper.CommandStatus.Status\x12%\n\x08progress\x18\x03 \x01(\x0b\x32\x13.redpepper.Progress\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\t\"=\n\x06Status\x12\x0b\n\x07PENDING\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\n\n\x06\x46\x41ILED\x10\x02\x12\r\n\tCANCELLED\x10\x03\"*\n\x08Progress\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\r\x12\r\n\x05total\x18\x02 \x01(\r\"<\n\x0b\x44\x61taRequest\x12\x11\n\trequestID\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t\";\n\x0c\x44\x61taResponse\x12\x11\n\trequestID\x18\x01 \x01(\x05\x12\n\n\x02ok\x18\x02 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t*\xb3\x01\n\x0bMessageType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x0f\n\x0b\x43LIENTHELLO\x10\n\x12\x0f\n\x0bSERVERHELLO\x10\x0b\x12\x07\n\x03\x42YE\x10\x0c\x12\x08\n\x04PING\x10\r\x12\x08\n\x04PONG\x10\x0e\x12\x0b\n\x07\x43OMMAND\x10\x14\x12\x11\n\rCOMMANDCANCEL\x10\x15\x12\x11\n\rCOMMANDSTATUS\x10\x16\x12\x0f\n\x0b\x44\x41TAREQUEST\x10\x1e\x12\x10\n\x0c\x44\x41TARESPONSE\x10\x1f\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'redpepper.common.messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MESSAGETYPE']._serialized_start=1135
  _globals['_MESSAGETYPE']._serialized_end=1314
  _globals['_MESSAGE']._serialized_start=47
  _globals['_MESSAGE']._serialized_end=523
  _globals['_BYE']._serialized_start=525
  _globals['_BYE']._serialized_end=546
  _globals['_CLIENTHELLO']._serialized_start=548
  _globals['_CLIENTHELLO']._serialized_end=593
  _globals['_SERVERHELLO']._serialized_start=595
  _globals['_SERVERHELLO']._serialized_end=625
  _globals['_PING']._serialized_start=627
  _globals['_PING']._serialized_end=647
  _globals['_PONG']._serialized_start=649
  _globals['_PONG']._serialized_end=669
  _globals['_COMMAND']._serialized_start=671
  _globals['_COMMAND']._serialized_end=727
  _globals['_COMMANDCANCEL']._serialized_start=729
  _globals['_COMMANDCANCEL']._serialized_end=763
  _globals['_COMMANDSTATUS']._serialized_start=766
  _globals['_COMMANDSTATUS']._serialized_end=965
  _globals['_COMMANDSTATUS_STATUS']._serialized_start=904
  _globals['_COMMANDSTATUS_STATUS']._serialized_end=965
  _globals['_PROGRESS']._serialized_start=967
  _globals['_PROGRESS']._serialized_end=1009
  _globals['_DATAREQUEST']._serialized_start=1011
  _globals['_DATAREQUEST']._serialized_end=1071
  _globals['_DATARESPONSE']._serialized_start=1073
  _globals['_DATARESPONSE']._serialized_end=1132
# @@protoc_insertion_point(module_scope)
