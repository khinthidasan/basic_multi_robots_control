import json
import socket
import os
import struct
import time
import sys
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import serial
import time


class PlcMachine(object):
    def __init__(self, plc_ip='192.168.192.199', port="502"):

        
        #PLC board
        self._plcip = plc_ip
        self.plc_port = port     # Modbus TCP port (default 502)
        self.plc_unit_id = 1    # Unit ID (or Slave ID)
        self.plc_register_address = 100  # Address of the register

    def write_to_plc_register(self,value):
        try:
            client = ModbusTcpClient(self._plcip, self.plc_port)

            if client.connect():
                response = client.write_register(self.plc_register_address, value, unit=self.plc_unit_id)
                if not response.isError():
                    print(f"Successfully wrote value {value} to register {self.plc_register_address}")
                    return True
                else:
                    print("Failed to write to the register")
            else:
                print("Failed to connect to PLC")

        except ModbusException as e:
            print(f"Modbus Exception: {e}")

        finally:
            client.close()
            return False
    



