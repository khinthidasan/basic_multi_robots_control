import time
from cls_jibot_robot import JIBOT
from cls_dobot_robot import DobotArm
from cls_seer_robot import SEER
from cls_plc_machine import PlcMachine

def main():

    # Intialize PlC machine
    plc_machine = PlcMachine("192.168.192.188")
    
    # Initialize Jibot Lift robot
    robot_lift = JIBOT("192.168.192.223")

    # Initialize Jibot Med robot
    robot_med = JIBOT("192.168.192.200")

    # Initialize SEER robot
    robot_seer = SEER("192.168.192.5")

    # Initialize dotbot MD400
    robot_md400 = DobotArm("192.168.192.66")

    # Initialize dotbot CR16A
    robot_cr16A = DobotArm("192.168.192.7")

   
    try:

        robot_lift.start()
        robot_lift.connect()
        robot_lift.get_robot_info(1000)

        robot_med.start()
        robot_med.connect()
        robot_med.get_robot_info(1000)

        robot_med.call_routes("ward_002", "a")
        while robot_med._status != "reached":
            time.sleep(1)

        robot_seer.gotargetblock("LM6")
        time.sleep(1)

        robot_md400.write_coil(0, 1)
        time.sleep(1)

        robot_seer.gotargetblock("LM10")
        time.sleep(1)

        robot_med.call_routes("ward_003", "a")
        while robot_med._status != "reached":
            time.sleep(1)

        robot_cr16A.write_coil(0, 1)
        time.sleep(1)


    except KeyboardInterrupt:
        print("\nStopping the system...")
    finally:
        # Clean up
        robot_lift.stop()
        robot_med.stop()
        print("System stopped")

if __name__ == "__main__":
    main() 