# basic_multi_robots_control

This is just a basic to control multiple robot from their provided API.
( Dobot Arm, SEER AMR, Jibot AMR, PLC machine ).

For Advanced, can be added additional functions ... AsyncTask, Thread, Process , IoT concepts, vision etc., according to the targeted tasks. 

integrated/

├── netprotocol ( SEER AMR API library )
      ├── rbkNetProtoEnums.py ( SEER AMR API library )
└── cls_dobot_robot.py
└── cls_jibot_robot.py
└── cls_plc_machine.py
└── cls_seer_robot.py
└── main.py


integratedRobotCtrl/
├── netprotocol
      ├── rbkNetProtoEnums.py ( SEER AMR API library )
├── cls_dobot_robot.py
├── cls_jibot_robot.py
├── cls_plc_machine.py
└── cls_seer_robot.py
└── main.py

- Run from main.py

Create Conda environment or just in python environment
install the following under the conda env or python env

pip install pymodbus==3.5.4
pip install pyserial==3.5

SEER AMR API library Ref: ( https://seer-group.feishu.cn/wiki/EvOMwPyJZiQIbmkLvCTct64Qnrb ) 
SEER AMR API library Ref: ( https://github.com/seer-robotics/Robokit_TCP_API_py/tree/master ) 
