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



# runs = 1000 # Default run is 1000
# if len(sys.argv)>1: # If I want to change the num of runs
#     runs = int(sys.argv[1])
# FNULL = open(os.devnull, 'w')
# logfile = open('logfile', 'w')


# replacing example with a running program. This is a simple python
# we can call from the command line.
# args = "exe" # Exe to test
# test_script = "import time;import sys;time.sleep(%d);sys.exit(100)"

test_script = "killall feh; feh -x --geometry 1280x800 /home/lumen/Volumetric/LightField/model-library/LUMEN-logo_imgs/01.png"






# REPRAP GCODES:
# https://reprap.org/wiki/G-code



# jmil says FIND THE CORRECT PORT FIRST WITH "ls /dev/ | grep ttyACM*"
# import subprocess
# batcmd="ls /dev/|grep ttyACM*"
# allPorts = subprocess.check_output(batcmd, shell=True)
# # this could contain multiple lines. Get only the first line
# thePortsArray = allPorts.splitlines()
# print(thePortsArray)
# theFirstPort = thePortsArray[0]
# theCleanPortString = "/dev/" + theFirstPort.decode("utf-8").strip()

theCleanPortString = "/dev/lumen-arduino"
print(theCleanPortString)

p=printcore(theCleanPortString,250000) # or p.printcore('COM3',250000) on Windows
# e.g.: p=printcore("/dev/tty.usbmodem144241",250000) # or p.printcore('COM3',250000) on Windows

# Wait for the printer to connect. Check every 100 ms
while not p.online: time.sleep(0.1)
print(str(p.online) + " that the printer is online now yay!")

# gcode=[i.strip() for i in open('test.gcode')] # or pass in your own array of gcode lines instead of reading from a file
# print(gcode)

# gcode = gcoder.LightGCode(gcode)

# print(gcode)

# p.startprint(gcode) # this will start a print



# def projectLayer():
#     test_script = "killall feh; setpower 255; feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/LUMEN-logo_imgs/01.png"
#     succ = 0
#     fail = 0
#     # set by timer
#     status_dict = {'timeout':False}
#     # test prog sleeps i seconds
#     args = ["bash", "-c", test_script]
#     proc = subprocess.Popen(args,
#         stdout = logfile, stderr = FNULL)
#     # trigger timout and kill process in 5 seconds
#     timer = threading.Timer(5, on_timeout, (proc, status_dict))
#     timer.start()
#     proc.wait()
#     # in case we didn't hit timeout
#     timer.cancel()
#     print (status_dict)
#     if not status_dict['timeout'] and proc.returncode == 100:
#         succ += 1 # If returned 100 then success
#     else:
#         fail += 1 # Else Failed
#     open('logfile', 'w').close() # Empties the file
#     print ("Succ: %d , Fail: %d" % (succ, fail))
#
#
# def powerOff():
#     test_script = "setpower 0"
#     succ = 0
#     fail = 0
#     # set by timer
#     status_dict = {'timeout':False}
#     # test prog sleeps i seconds
#     args = ["bash", "-c", test_script]
#     proc = subprocess.Popen(args,
#         stdout = logfile, stderr = FNULL)
#     # trigger timout and kill process in 5 seconds
#     timer = threading.Timer(5, on_timeout, (proc, status_dict))
#     timer.start()
#     proc.wait()
#     # in case we didn't hit timeout
#     timer.cancel()
#     print (status_dict)
#     if not status_dict['timeout'] and proc.returncode == 100:
#         succ += 1 # If returned 100 then success
#     else:
#         fail += 1 # Else Failed
#     open('logfile', 'w').close() # Empties the file
#     print ("Succ: %d , Fail: %d" % (succ, fail))




# NEVER STOP
currentLayer = 0
# while True:
    

# layerHeight = 0.1
layerHeight = 0.5
layerTime = 0.5
pauseBeforeLift = 0.5
pauseForSetpower = 0.5
pauseBeforeProject = 2
liftDistance = 2



# TURN OFF PROJECTOR
command = "setpower 0"
print("command is '" + command + "'")
return_code = subprocess.call(command, shell=True)
print(return_code)

command = "killall feh"
print("command is '" + command + "'")
return_code = subprocess.call(command, shell=True)
print(return_code)

# SET FAN AT FULL SPEED
print("Set Fan at FULLSPEED with M106")
p.send_now("M106; set fan at full speed")

# SET BED TEMP TO 60 C
print("Set BED TEMP TO 60 C with M140 S60")
p.send_now("M140 S60; set bed temp to 60 C")


while True:
    # HOME THE PRINTER
    p.send_now("G28 X")
    print ("HOMING")
    time.sleep(20)
    print ("HOMING COMPLETED!!")



    for i in range(100):
    
        #DON'T PRINT MORE THAN THIS HEIGHT, TOTAL
        if (i+1)*layerHeight >= 39:
            print ("max print distance reached!")
            break
    
        print("\n\n######## CURRENT LAYER IS #" + str(currentLayer+1))
    
        # GO TO LAYER POSITION -- LIFT DISTANCE
        p.send_now("G91; relative positioning")
        p.send_now("G1 X" + str(liftDistance))
        
        # GO TO LAYER POSITION -- LIFT DISTANCE
        p.send_now("G91; relative positioning")
        p.send_now("G1 X-" + str(liftDistance-layerHeight))
        
        
        
        # PROJECT THE IMAGE
        # command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/model-library/makerook_imgs/" + '%03d' % (i*6) + ".png &"
        command = "feh -x --geometry 1280x800 /home/lumen/Volumetric/LightField/model-library/makerook_imgs/" + '%03d' % i + ".png &"
        print("command #" + str(i+1) + " is '" + command + "'")
        return_code = subprocess.call(command, shell=True)
        print(return_code)
        
        # PAUSE BEFORE PROJECT
        print ("PAUSE BEFORE PROJECTION: " + str(pauseBeforeProject) + " seconds")
        time.sleep(pauseBeforeProject)


        # START PROJECTION
        command = "setpower 126"
        print("command #" + str(i+1) + " is '" + command + "'")
        return_code = subprocess.call(command, shell=True)
        print(return_code)
    
        print ("PROJECTION: " + str(layerTime) + " seconds")
        time.sleep(layerTime)

        command = "setpower 0"
        print("command #" + str(i+1) + " is '" + command + "'")
        return_code = subprocess.call(command, shell=True)
        print(return_code)
    
        #KILLALL FEH
        command = "killall feh &"
        print("command #" + str(i+1) + " is '" + command + "'")
        return_code = subprocess.call(command, shell=True)
        print(return_code)


        # PAUSE BEFORE LIFT
        print ("PAUSE BEFORE LIFT: " + str(pauseBeforeLift) + " seconds")
        time.sleep(pauseBeforeLift)
    
    
    

        print ("MOVE TO NEXT LAYER")



        # command = "killall feh"
        # print("command #" + str(i+1) + " is " + command)
        # return_code = subprocess.call(command, shell=True)
        # print(return_code)
    
    


        currentLayer += 1
    







# # If you need to interact with the printer:
# # p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
# # p.pause() # use these to pause/resume the current print
# # p.resume()
# p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.



p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
