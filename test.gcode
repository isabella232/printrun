G28 Z ; Home Z-axis until endstop is hit
G91 ; Relative Coordinates
G0 Z10 ; move up 1
G4 P2000; wait 2 sec
G90 ; Absolute Coordinates
G0 Z11 ; move up 1
G4 P2000; wait 2 sec
M114;
M105;