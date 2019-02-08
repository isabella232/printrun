#!/usr/bin/env python3

#TEST MOTOR TORQUE AS A FUNCTION OF APPLIED CURRENT
# CONNECT MOTOR TO Y-AXIS
## USE 1/16th stepping, ideally we will be at 1/16th stepping for smoothest motion


import subprocess
import os
import sys
import threading
import time

sys.path.append( '/home/lumen/Volumetric/printrun' )
from printrun.printcore import printcore
from printrun import gcoder

# https://stackoverflow.com/questions/35685403/python-run-subprocess-for-certain-time
def on_timeout(proc, status_dict):
    """Kill process on timeout and note as status_dict['timeout']=True"""
    # a container used to pass status back to calling thread
    status_dict['timeout'] = True
    print("timed out")
    proc.kill()





theCleanPortString = "/dev/lumen-arduino"
print(theCleanPortString)

p=printcore(theCleanPortString,250000) # or p.printcore('COM3',250000) on Windows
# e.g.: p=printcore("/dev/tty.usbmodem144241",250000) # or p.printcore('COM3',250000) on Windows

# Wait for the printer to connect. Check every 100 ms
while not p.online: time.sleep(0.1)
print(str(p.online) + " that the printer is online now yay!")



print("WELCOME TO VOLUMETRIC'S MOTOR TESTER!")
p.send_now("G91; relative coordinates")
stepsPerRev = 1600/200*2
degreesToMove = 180
distance = 2
pause = 2



time.sleep(pause*2)



for i in range(200,2400+200,200):
        
    
    
    print ("")
    print ("################### CURRENT SETTING IS ###################")
    print ("################### " + str(i) + " mA ###################")
    
    time.sleep(pause)

    for i in range (5):

        time.sleep(pause)
        
        p.send_now("M906 Y" + str(i))
        p.send_now("M906 Y" + str(i))
        p.send_now("M906 Y" + str(i))
        p.send_now("G0 Y" + str(distance) + " F100")
        # p.send_now("G4 P" + str(pause*1000))
        p.send_now("M400")
    
    # time.sleep(pause)
    
    
    
    # HOME THE PRINTER
    # p.send_now("G28 X")
    # print ("HOMING")
    # time.sleep(20)
    # print ("HOMING COMPLETED!!")
    #
    #
    #
    # for i in range(126):
    #
    #     if (i+1)*layerHeight >= 70:
    #         #DON'T PRINT MORE THAN 100 mm TOTAL
    #         print ("max print distance reached!")
    #         break
    #
    #     print("\n\n######## CURRENT LAYER IS #" + str(currentLayer+1))
    #
    #     # GO TO LAYER POSITION -- LIFT DISTANCE
    #     p.send_now("G91; relative positioning")
    #     p.send_now("G1 X" + str(liftDistance))
    #
    #     # GO TO LAYER POSITION -- LIFT DISTANCE
    #     p.send_now("G91; relative positioning")
    #     p.send_now("G1 X-" + str(liftDistance-layerHeight))
    #
    #
    #
    #     # PROJECT THE IMAGE
    #     # command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/makerook_imgs/" + '%03d' % (i*6) + ".png &"
    #     command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/makerook_imgs/" + '%03d' % i + ".png &"
    #     print("command #" + str(i+1) + " is '" + command + "'")
    #     return_code = subprocess.call(command, shell=True)
    #     print(return_code)
    #
    #     # PAUSE BEFORE PROJECT
    #     print ("PAUSE BEFORE PROJECTION: " + str(pauseBeforeProject) + " seconds")
    #     time.sleep(pauseBeforeProject)
    #
    #
    #     # START PROJECTION
    #     command = "setpower 126"
    #     print("command #" + str(i+1) + " is '" + command + "'")
    #     return_code = subprocess.call(command, shell=True)
    #     print(return_code)
    #
    #     print ("PROJECTION: " + str(layerTime) + " seconds")
    #     time.sleep(layerTime)
    #
    #     command = "setpower 0"
    #     print("command #" + str(i+1) + " is '" + command + "'")
    #     return_code = subprocess.call(command, shell=True)
    #     print(return_code)
    #
    #     #KILLALL FEH
    #     command = "killall feh &"
    #     print("command #" + str(i+1) + " is '" + command + "'")
    #     return_code = subprocess.call(command, shell=True)
    #     print(return_code)
    #
    #
    #     # PAUSE BEFORE LIFT
    #     print ("PAUSE BEFORE LIFT: " + str(pauseBeforeLift) + " seconds")
    #     time.sleep(pauseBeforeLift)
    #
    #
    #
    #
    #     print ("MOVE TO NEXT LAYER")
    #
    #
    #
    #     # command = "killall feh"
    #     # print("command #" + str(i+1) + " is " + command)
    #     # return_code = subprocess.call(command, shell=True)
    #     # print(return_code)
    #
    #
    #
    #
    #     currentLayer += 1
    #
    #
    #
    #




# # If you need to interact with the printer:
# # p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
# # p.pause() # use these to pause/resume the current print
# # p.resume()
# p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.


p.send_now("M18; Motors off")

p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
