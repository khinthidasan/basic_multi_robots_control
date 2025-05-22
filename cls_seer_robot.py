from netprotocol.rbkNetProtoEnums import *
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


class SEER(object):
    def __init__(self, robot_ip, robot_port=19204):

        #Configuration
        #SEER board
        self._rbkip = robot_ip
        self.PACK_FMT_STR = '!BBHLH6s'
        self.port = robot_port
        self.API_number = 1013
        self.DI_id = 19
        
        #Connect to SEER Board
        self._so_DI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_DI.settimeout(3)
        self._so_DI.connect((self._rbkip, self.port))

        self._so_state = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_state.settimeout(3)
        self._so_state.connect((self._rbkip, API_PORT_STATE))

        self._so_task = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_task.settimeout(0.5)
        self._so_task.connect((self._rbkip, API_PORT_TASK))

        self._so_IO = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_IO.settimeout(0.5)
        self._so_IO.connect((self._rbkip, API_PORT_OTHER))


    def gotarget(self, landmark):
        self._so_task.send(
            packMsg(1, robot_task_gotarget_req, {"id": landmark}))

    def setDO(self, sensor, flag):
        self._so_IO.send(
            packMsg(1, robot_other_setdo_req, {"id": sensor, "status": flag}))

    def reachtarget(self):
        COMPLETED = 4
        self._so_state.send(packMsg(1, robot_status_task_req, {}))
        try:
            data = self._so_state.recv(16)
        except socket.timeout:
            return False
        jsonDataLen = 0
        if(len(data) < 16):
            print('pack head error')
            os.system('pause')
            self._so_state.close()
            quit()
        else:
            jsonDataLen = unpackHead(data)

        data = self._so_state.recv(1024)
        ret = json.loads(data)
        if(ret['task_status'] is COMPLETED):
            return True
        else:
            #print('[' + time.ctime()[11:19] + '] ' + str(ret))
            return False

    def gotargetblock(self, point):
        self.gotarget(point)
        time.sleep(0.5)
        while self.reachtarget() is not True:
            time.sleep(0.5)

    
    def packMasgLocal(self, reqId, msgType, msg={}):
        msgLen = 0
        jsonStr = json.dumps(msg)
        if (msg != {}):
            msgLen = len(jsonStr)
        rawMsg = struct.pack(self.PACK_FMT_STR, 0x5A, 0x01, reqId, msgLen,msgType, b'\x00\x00\x00\x00\x00\x00')
        print("{:02X} {:02X} {:04X} {:08X} {:04X}"
        .format(0x5A, 0x01, reqId, msgLen, msgType))

        if (msg != {}):
            rawMsg += bytearray(jsonStr,'ascii')
            #print(msg)

        return rawMsg


    def get_status_by_DI_id(self, data, target_id):
        for entry in data.get("DI", []):
            if entry.get("id") == target_id:
                return entry.get("status") 
        return None

    
    def listening_DI(self, given_flag):
        test_msg = demo.packMasgLocal(1, self.API_number,{})
        while True:
            self._so_state.send(test_msg)

            dataall = b''

            try:
                data = self._so_state.recv(16)
            except socket.timeout:
                print('timeout')
                self._so_state.close
            jsonDataLen = 0
            backReqNum = 0
            if(len(data) < 16):
                print('pack head error')
                #print(data)
                self._so_state.close()
            else:
                header = struct.unpack(self.PACK_FMT_STR, data)
                jsonDataLen = header[3]
                backReqNum = header[4]
            dataall += data
            data = b''
            readSize = 1024

            try:
                while (jsonDataLen > 0):
                    recv = self._so_state.recv(readSize)
                    data += recv
                    jsonDataLen -= len(recv)
                    if jsonDataLen < readSize:
                        readSize = jsonDataLen
                DI_status = self.get_status_by_DI_id(json.loads(data), self.DI_id)
                print( DI_status)
                if (DI_status is given_flag):
                    return "Finish"

            except socket.timeout:
                print('timeout')
           
            time.sleep(0.05)

        self._so_state.close()





