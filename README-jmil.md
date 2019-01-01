installation instructions:

follow 

Install:
Cython-based G-Code parser

Printrun default G-Code parser is quite memory hungry, but we also provide a much lighter one which just needs an extra build-time dependency (Cython), plus compiling the extension with:

$ python -m pip install Cython
$ python setup.py build_ext --inplace

The warning message:

WARNING:root:Memory-efficient GCoder implementation unavailable: No module named gcoder_line
means that this optimized G-Code parser hasn't been compiled. To get rid of it and benefit from the better implementation, please install Cython and run the command above.



Dependencies

To use pronterface, you need:

Python 3 (ideally 3.6),
pyserial (or python3-serial on ubuntu/debian)
pyreadline (not needed on Linux)
wxPython 4
pyglet
numpy (for 3D view)
pycairo (to use Projector feature)
cairosvg (to use Projector feature)
dbus (to inhibit sleep on some Linux systems)

