# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ping_pb2 as ping__pb2


class PingCalculatorStub(object):
  """ping 服务定义
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Calc = channel.unary_unary(
        '/ping.PingCalculator/Calc',
        request_serializer=ping__pb2.PingRequest.SerializeToString,
        response_deserializer=ping__pb2.PingResponse.FromString,
        )


class PingCalculatorServicer(object):
  """ping 服务定义
  """

  def Calc(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PingCalculatorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Calc': grpc.unary_unary_rpc_method_handler(
          servicer.Calc,
          request_deserializer=ping__pb2.PingRequest.FromString,
          response_serializer=ping__pb2.PingResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ping.PingCalculator', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))