"""
Receivs OSC and performs a simon
"""
import argparse
import math
import time

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio

import numpy as np
from playsound import playsound

current_stage = []
sum_of_values = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}

dispatcher = Dispatcher()

def store_highest_value(*args):
  # TODO - if user doesn't make sounds then don't sum it
  values = np.array(args)
  print("{}".format(args))
  # The strongest produced value
  # TODO - perhaps I should also count the 2nd best value
  strongest_value = values.argmax()
  sum_of_values[str(strongest_value)] += 1

def check_wek_inputs(unused_addr, *args):
  store_highest_value(args)  
  print(sum_of_values)

async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    while True:
      dispatcher.map("/wek/outputs", check_wek_inputs)
      print("Listening..")
      await asyncio.sleep(5)
      dispatcher.unmap("/wek/outputs", check_wek_inputs)
      print("Sleeping...")
      await asyncio.sleep(2)


async def init_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
      type=int, default=12000, help="The port to listen on")
    args = parser.parse_args()
    
    server = AsyncIOOSCUDPServer((args.ip, args.port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    print('Server started')
    playsound('./sounds/welcome.wav')

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint

if __name__ == "__main__":
  asyncio.run(init_main())
