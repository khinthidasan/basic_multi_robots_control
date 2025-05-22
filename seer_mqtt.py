import time
import paho.mqtt.client as mqtt
from cls_seer_robot import SEER

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("seer")

def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        print(f"Received message: {message}")
        
        # Try to convert message to integer
        try:
            lm_number = int(message)
            print(f"Moving to LM{lm_number}")
            robot_seer.gotargetblock(f"LM{lm_number}")
        except ValueError:
            print(f"Invalid message: {message}. Please send an integer.")
            
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    global robot_seer
    
    # Initialize SEER robot
    robot_seer = SEER("192.168.192.5")
    
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # Connect to MQTT broker (replace with your broker address)
        client.connect("localhost", 1883, 60)
        
        # Start the MQTT loop
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nStopping the system...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("System stopped")

if __name__ == "__main__":
    main() 