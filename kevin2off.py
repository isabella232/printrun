#!/usr/bin/env python3

#to send a file of gcode to the printer

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


# test_script = "killall feh; feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/LUMEN-logo_imgs/01.png"




theCleanPortString = "/dev/lumen-arduino"
print(theCleanPortString)

p=printcore(theCleanPortString,250000) # or p.printcore('COM3',250000) on Windows

# Wait for the printer to connect. Check every 100 ms
while not p.online: time.sleep(0.1)
print(str(p.online) + " that the printer is online now yay!")



# NEVER STOP
currentLayer = 0

# TURN OFF PROJECTOR
command = "setpower 0"
print("command is '" + command + "'")
return_code = subprocess.call(command, shell=True)
print(return_code)

command = "killall feh"
print("command is '" + command + "'")
return_code = subprocess.call(command, shell=True)
print(return_code)



BEDTEMP = 37
p.send_now("M140 S" + str(BEDTEMP))


# HOME THE PRINTER
p.send_now("G28 X")
print ("HOMING")
# print ("pausing 60 sec to allow you to adjust z0")
# time.sleep(60)

z0 = 0

# mm/min
PRINTSPEED = 200


for i in range(80):
    
    if i == 0:
        # 50 µm printing FTW
        layerHeight = 0.05
        exposureTime = 13
        pauseBeforeLift = 10
        pauseToFindZero = 60
        pauseBeforeExpose = 4
        pauseToLoadResin = 15
        liftDistance = 2

        # PAUSE BEFORE PROJECT
        print ("SET Z0 NOW, MANUALLY, you have " + str(pauseToFindZero) + " seconds. Be precise here!!")
        # print ("PAUSE TO SET Z0: " + str(pauseToFindZero) + " seconds")
        time.sleep(pauseToFindZero)

        # GO TO LAYER POSITION -- LIFT DISTANCE
        p.send_now("G91") # RELATIVE POSITIONING
        # p.send_now("G92 X0; you are now at z0")
        
        print("YOU ARE NOW AT Z0, ALMOST READY TO BEGIN PRINTING")
    

        p.send_now("G90") # ABSOLUTE POSITIONING
        p.send_now("G1 X30 F" + str(PRINTSPEED))
        
        # PAUSE BEFORE PROJECT
        print ("PAUSE TO LOAD RESIN: " + str(pauseToLoadResin) + " seconds")
        time.sleep(pauseToLoadResin)
        

        p.send_now("G1 X" + str(layerHeight) + " F" + str(PRINTSPEED))
        p.send_now("G91") # RELATIVE POSITIONING
        print ("PAUSE TO RETURN TO FIRST LAYER POSITION: " + str(pauseToLoadResin) + " seconds")
        time.sleep(pauseToLoadResin)
        

    if i == 1:
        pauseBeforeLift = 4

    if i > 1:
        exposureTime = 2
        # pauseBeforeLift = 1
        # pauseBeforeExpose = 2
        # liftDistance = 2
        


    if (i+1)*layerHeight >= 80:
        #DON'T PRINT MORE THAN 80 mm TOTAL
        print ("max print distance reached!")
        break

    print("\n\n######## CURRENT LAYER IS #" + str(currentLayer+1))



    if i > 0:
        # PAUSE BEFORE LIFT
        print ("PAUSE BEFORE LIFT: " + str(pauseBeforeLift) + " seconds")
        time.sleep(pauseBeforeLift)

        # GO TO LAYER POSITION -- LIFT DISTANCE
        p.send_now("G91; relative positioning")
        p.send_now("G1 X" + str(liftDistance) + " F" + str(PRINTSPEED))
    
        # GO TO LAYER POSITION -- LIFT DISTANCE
        p.send_now("G91; relative positioning")
        p.send_now("G1 X-" + str(liftDistance-layerHeight) + " F" + str(PRINTSPEED))
    
    
    
    # PROJECT THE IMAGE
    # command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/makerook_imgs/" + '%03d' % (i*6) + ".png &"
    command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/working/kevin-50-2off/" + '%06d' % i + ".png &"
    print("command #" + str(i+1) + " is '" + command + "'")
    return_code = subprocess.call(command, shell=True)
    print(return_code)
    
    # PAUSE BEFORE PROJECT
    print ("PAUSE BEFORE PROJECTION: " + str(pauseBeforeExpose) + " seconds")
    time.sleep(pauseBeforeExpose)


    # START PROJECTION
    command = "setpower 126"
    print("command #" + str(i+1) + " is '" + command + "'")
    return_code = subprocess.call(command, shell=True)
    print(return_code)

    print ("PROJECTION: " + str(exposureTime) + " seconds")
    time.sleep(exposureTime)

    command = "setpower 0"
    print("command #" + str(i+1) + " is '" + command + "'")
    return_code = subprocess.call(command, shell=True)
    print(return_code)

    #KILLALL FEH
    command = "killall feh &"
    print("command #" + str(i+1) + " is '" + command + "'")
    return_code = subprocess.call(command, shell=True)
    print(return_code)




    print ("MOVE TO NEXT LAYER")



    # command = "killall feh"
    # print("command #" + str(i+1) + " is " + command)
    # return_code = subprocess.call(command, shell=True)
    # print(return_code)




    currentLayer += 1
    



p.send_now("G90")
p.send_now("G0 X100 F300")

print ("PRINT HAS COMPLETED YAY!")


# # If you need to interact with the printer:
# # p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
# # p.pause() # use these to pause/resume the current print
# # p.resume()
# p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.



p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
