G28 X ; Home X-axis until endstop is hit
G91 ; Relative Coordinates
G1 X10 ; move up 1
G4 P2000; wait 2 sec
G90 ; Absolute Coordinates
G1 X11 ; move up 1
G4 P2000; wait 2 sec
M114;
M105;