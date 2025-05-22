from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time

class DobotArm:
    def __init__(self, ip='192.168.192.6', port=502, unit_id=0):
        self.ip = ip
        self.port = port
        self.unit_id = unit_id
        self.client = ModbusTcpClient(self.ip, self.port)

    def write_coil(self, address, value):
        if self.client.connect():
            response = self.client.write_coil(address, value, unit=self.unit_id)
            if not response.isError():
                print(f"Successfully wrote value {value} to coil {address}")
                return True
            else:
                print("Failed to write to the coil")
        else:
            print("Failed to connect to Dobot")
        return False

    def read_coil(self, address):
        if self.client.connect():
            response = self.client.read_coils(address, unit=self.unit_id)   
            if not response.isError():
                coil_value = response.bits[0]
                return coil_value
            else:
                print("Failed to read from the coil")
        else:
            print("Failed to connect to Dobot")
        return None

    def close(self):
        self.client.close() 