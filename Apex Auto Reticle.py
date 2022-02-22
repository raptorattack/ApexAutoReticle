# Sources:
# https://www.reddit.com/r/learnpython/comments/22tke1/use_python_to_send_keystrokes_to_games_in_windows/
# https://stackoverflow.com/questions/3800458/quickly-getting-the-color-of-some-pixels-on-the-screen-in-python-on-windows-7

#old reticle colors in cfg file:
#bind "F1" "exec reticles"
#bind "i" "reticle_color 60 220 850"
#bind "o" "reticle_color 800 60 600"
#bind "p" "reticle_color 400 350 0"

#new reticle colors in cfg file:
#bind "F1" "exec reticles"
#bind "i" "reticle_color 0 255 233"
#bind "o" "reticle_color 255 60 204"
#bind "p" "reticle_color 255 220 0"

from PIL import Image, ImageGrab
from time import sleep
import ctypes, time

reticle = "magenta"


# Bunch of stuff so that the script can send keystrokes to game

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Send Keystroke Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def KeyPressCyan():
    #time.sleep(3)
    PressKey(0x17) # press I
    time.sleep(.05)
    ReleaseKey(0x17) #release I

def KeyPressMagenta():
    #time.sleep(3)
    PressKey(0x18) # press O
    time.sleep(.05)
    ReleaseKey(0x18) #release O

def KeyPressYellow():
    #time.sleep(3)
    PressKey(0x19) # press P
    time.sleep(.05)
    ReleaseKey(0x19) #release P


sleep(2)


while True: # run this code constantly
    image = ImageGrab.grab() # get an image of the space just above the reticle
    for y in range(685, 686, 10): # tiny patch of the screen
        for x in range(1280, 1281, 10):
            color = image.getpixel((x, y))
    if (color[0] > color[1] + 10 and color[0] > color[2] + 10 and reticle != "cyan"): # if it's a more red scene
        reticle = "cyan"
        KeyPressCyan()
    if (color[1] > color[0] + 10 and color[1] > color[2] + 10 and reticle != "magenta"): # if it's a more green scene
        reticle = "magenta"
        KeyPressMagenta()
    if (color[2] > color[0] + 10 and color[2] > color[1] + 10 and reticle != "yellow"): # if it's a more blue scene
        reticle = "yellow"
        KeyPressYellow()
    sleep(0.5) # wait a bit so it's not running constantly
