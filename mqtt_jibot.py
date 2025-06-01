import time
import paho.mqtt.client as mqtt
from cls_jibot_robot import JIBOT

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("jibot")

def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        print(f"Received message: {message}")
        
        # Try to convert message to integer
        try:
            ward_number = int(message)
            print(f"Moving to ward_{ward_number:03d}")
            robot_jibot.call_routes(f"ward_{ward_number:03d}", "a")
            while robot_jibot._status != "reached":
                time.sleep(1)
        except ValueError:
            print(f"Invalid message: {message}. Please send an integer.")
            
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    global robot_jibot
    
    # Initialize JIBOT robot
    robot_jibot = JIBOT("192.168.192.200")
    
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Start and connect the robot
        robot_jibot.start()
        robot_jibot.connect()
        robot_jibot.get_robot_info(1000)
        
        # Connect to MQTT broker (replace with your broker address)
        client.connect("localhost", 1883, 60)
        
        # Start the MQTT loop
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nStopping the system...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        robot_jibot.stop()
        client.disconnect()
        print("System stopped")

if __name__ == "__main__":
    main() 
