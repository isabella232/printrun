#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder
import time

# REPRAP GCODES:
# https://reprap.org/wiki/G-code

# jmil says FIND THE CORRECT PORT FIRST WITH "ls /dev/tty.usb*"
import subprocess
batcmd="ls /dev/tty.usb*"
allPorts = subprocess.check_output(batcmd, shell=True)
# this could contain multiple lines. Get only the first line
thePortsArray = allPorts.splitlines()
print(thePortsArray)
theFirstPort = thePortsArray[0]
theCleanPortString = theFirstPort.decode("utf-8").strip()
print(theCleanPortString)

p=printcore(theCleanPortString,115200) # or p.printcore('COM3',115200) on Windows
# e.g.: p=printcore("/dev/tty.usbmodem144241",115200) # or p.printcore('COM3',115200) on Windows

# Wait for the printer to connect. Check every 100 ms
while not p.online: time.sleep(0.1)

gcode=[i.strip() for i in open('test.gcode')] # or pass in your own array of gcode lines instead of reading from a file
gcode = gcoder.LightGCode(gcode)
p.startprint(gcode) # this will start a print


#p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.






# Kliment default file with printcore, from: https://github.com/kliment/Printrun#cython-based-g-code-parser
# #to send a file of gcode to the printer
# from printrun.printcore import printcore
# from printrun import gcoder
# p=printcore('/dev/ttyUSB0',115200) # or p.printcore('COM3',115200) on Windows
# gcode=[i.strip() for i in open('filename.gcode')] # or pass in your own array of gcode lines instead of reading from a file
# gcode = gcoder.LightGCode(gcode)
# p.startprint(gcode) # this will start a print
#
# #If you need to interact with the printer:
# p.send_now("M105") # this will send M105 immediately, ahead of the rest of the print
# p.pause() # use these to pause/resume the current print
# p.resume()
# p.disconnect() # this is how you disconnect from the printer once you are done. This will also stop running prints.
