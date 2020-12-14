import serial
import time
import json
import random
import arena
from threading import Thread
from utils import send_alert2

# Global for keeping track of which sensor to display data from

test_email = True




email_status= False

if test_email and email_status==False:
    send_alert2()
    email_status=True

def start_serial():
    global sensor_to_read
    global reading_text



    global email_status 
#    global test_email
    global door_status

    # set up the serial line
    ser = serial.Serial('COM4', 9600)
    time.sleep(2)
   
   
    while True:
        if email_status and door_status == True:
            ser.write("blink\n".encode())
            
        elif email_status and door_status == False:
            ser.write("dont blink\n".encode())
        time.sleep(1)

    ser.close()


def scene_callback(msg):
    print("scene_callback: ", msg)

arena.init("arena.andrew.cmu.edu", "realm", "patrick_scene")#, scene_callback)




door_status = False
def door_button_callback(event):
    global door_obj
    global door_status
    if event.event_type == arena.EventType.mousedown:
        if door_status:
            door_status = False
            door_obj.update(data='{"animation": { "property": "rotation", "from": "0 90 0", "to": "0 0 0", "loop": false, "dur": 1000}}')
        else:
            door_status = True
            door_obj.update(data='{"animation": { "property": "rotation","from": "0 0 0", "to": "0 90 0 ", "loop": false, "dur": 1000}}')
door_obj = arena.Object(
        objName = "door",
        objType=arena.Shape.cube,
        scale=(0.1,2,1.2),
        location=(-9,1.6,-2),
        clickable=False,
        data='{"animation": { "property": "rotation", "to": "0 0 0", "loop": false, "dur": 0}}',
)
button_door = arena.Object(
        objName = "button_dor",
        objType=arena.Shape.cube,
        scale=(1,1,1),
        location=(-11,1.6,-3),
        clickable=True,
        callback=door_button_callback,
        color = (255,0, 255)
)
        

thread = Thread(target = start_serial)
thread.start()
arena.handle_events()

thread.join()