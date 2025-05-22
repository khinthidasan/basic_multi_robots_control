# basic_multi_robots_control

This is just a basic to control multiple robot from their provided API.
( Dobot Arm, SEER AMR, Jibot AMR, PLC machine )

For Advanced, can be added additional functions ... AsyncTask, Thread, Process , IoT concepts, vision etc., according to the targeted tasks. 

integrated/
├── netprotocol ( seer AMR API library Ref: ( https://seer-group.feishu.cn/wiki/EvOMwPyJZiQIbmkLvCTct64Qnrb ) )
      ├── rbkNetProtoEnums.py ( Ref: ( https://github.com/seer-robotics/Robokit_TCP_API_py/tree/master ) )
└── cls_dobot_robot.py
└── cls_jibot_robot.py
└── cls_plc_machine.py
└── cls_seer_robot.py
└── main.py

- Run from main.py

Create Conda environment or just in python environment
install the following under the conda env or python env

pip install paho-mqtt==1.6.1
pip install pymodbus==3.5.4
pip install pyserial==3.5
