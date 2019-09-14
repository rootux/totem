"""
Receivs OSC and performs a simon
"""
import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def print_wek_inputs(unused_addr, *args):
  print("{}".format(args))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=12000, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/wek/outputs", print_wek_input)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
