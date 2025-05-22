import re
import time
import json
import socket
import threading
import serial

class JIBOT:
    def __init__(self, robot_ip, robot_port=7273):
        # Robot IP and port
        self.robot_ip = robot_ip
        self.robot_port = robot_port

        # Connection to Jibot
        self._so_task = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_task.settimeout(3)
        self._so_task.connect((self.robot_ip, self.robot_port))
        
        self._running = True
        self._mode = ""
        self._status = ""
        
        self._receiver_thread = threading.Thread(target=self.receive_data_from_server)

    def start(self):
        self._receiver_thread.start()

    def stop(self):
        self._running = False
        self._receiver_thread.join()
        self._so_task.close()

    def json_cmd_to_jibot(self, json_cmd):
        try:
            json_data = json.dumps(json_cmd, separators=(',', ':'))
            total_length = len(json_data)
            formatted_message = f"$#{total_length}##{json_data}$~"
            self._so_task.sendall(formatted_message.encode('utf-8'))
        except Exception as e:
            print("Error:", e)
            
    def connect(self):
        json_cmd_connect = {
            "#CMD#": "UmConnect",
            "#GAP#": -1,
            "user": "test",
            "password": "test",
            "device_type": "pc"
        }
        self.json_cmd_to_jibot(json_cmd_connect)
        
    def call_routes(self, name, key):
        json_cmd_routes = {
            "#CMD#": "UmRoutes",
            "#GAP#": -1,
            "key": key,
            "routes": name
        }
        self.json_cmd_to_jibot(json_cmd_routes)
        
    def get_robot_info(self, interval_ms):
        json_cmd_get_robot_info = {
            "#CMD#": "UmGetRobotInfo",
            "#GAP#": interval_ms
        }
        self.json_cmd_to_jibot(json_cmd_get_robot_info)

    def receive_data_from_server(self):
        try:
            while self._running:
                data = self._so_task.recv(32768)
                print("Data:", data.decode('utf-8'))
                self.process_data(data.decode('utf-8'))
        except Exception as e:
            print("Error:", e)

    def process_data(self, data):
        response = self.parse_string(data)
        if response is None:
            print("response is None")
        else:
            if response.get('#CMD#') == "UmGetRobotInfo":
                self._mode = response.get('mode')
                self._status = response.get('status')
                if self._mode == "Set":
                    self._status = self._status[:-1]
                print(f'info {self._mode} {self._status}')
            
    def parse_string(self, s):
        pattern = r'\$#(\d+)##(.+?)\$~'
        match = re.match(pattern, s)

        if match:
            json_length = int(match.group(1))
            json_data = match.group(2)

            if len(json_data) == json_length:
                try:
                    parsed_json = json.loads(json_data)
                    return parsed_json
                except json.JSONDecodeError:
                    print("error：cannot parse data")
                    return None
            else:
                print(f"error：length not match： {json_length}, {len(json_data)}")
                return None
        else:
            print("error：pattern not match")
            return None

