"""
Functions to control projector power
"""

import subprocess

def set_power(p_val):
    """
    Set the projector power to p_val clipped to the range 0-255
    """
    if p_val > 255:
        p_val = 255
    elif p_val < 0:
        p_val = 0
    
    subprocess.run('setpower ' + str(p_val), shell=True)