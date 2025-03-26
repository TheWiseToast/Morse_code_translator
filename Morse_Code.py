import RPi.GPIO as GPIO,time #imports GPIO for buttons and lights, time for LED
#.... . .-.. .-.. ---/ - .... .. .../ .. .../ -./ - . ... - / --- ..-. --/ -- --- .-. ... . / -.-. --- -.. ./ .--. .-. --- --. .-. -. --
morse_dic = { #Dictionary to translate text into morse
    "a": [0,1],    #.-
    "b": [1,0,0,0],#-...
    "c": [1,0,1,0],#-.-.
    "d": [1,0,0],  #-..
    "e": [0],      #.
    "f": [0,0,1,0],#..-.
    "g": [1,1,0],  #--.
    "h": [0,0,0,0],#....
    "i": [0,0],    #..
    "j": [0,1,1,1],#.---
    "k": [1,0,1],  #-.-
    "l": [0,1,0,0],#.-..
    "m": [1,1],    #--
    "n": [1,0],    #-.
    "o": [1,1,1],  #---
    "p": [0,1,1,0],#.--.
    "q": [1,1,0,1],#--.-
    "r": [1,0,1],  #-.-
    "s": [0,0,0],  #...
    "t": [1],      #-
    "u": [0,0,1],  #..-
    "v": [0,0,0,1],#...-
    "w": [0,1,1],  #.--
    "x": [1,0,0,1],#-..-
    "y": [1,0,1,1],#-.--
    "z": [1,1,0,0],#--..
    " ": ["/"],    #/
    "1": [0,1,1,1,1],
    "2": [0,0,1,1,1],
    "3": [0,0,0,1,1],
    "4": [0,0,0,0,1],
    "5": [0,0,0,0,0],
    "6": [1,0,0,0,0],
    "7": [1,1,0,0,0],
    "8": [1,1,1,0,0],
    "9": [1,1,1,1,0],
    "0": [1,1,1,1,1],
    ".": [0,1,0,1,0,1],
    ",": [1,1,0,0,1,1],
    "?": [0,0,1,1,0,0],
    "!": [1,0,1,0,1,0],
    }
reverse_morse_dic = { #Dictionary to translate morse into text
    "01":"a",
    "1000":"b",
    "1010":"c",
    "100":"d",
    "0":"e",
    "0010":"f",
    "110":"g",
    "0000":"h",
    "00":"i",
    "0111":"j",
    "101":"k",
    "0100":"l",
    "11":"m",
    "10":"n",
    "111":"o",
    "0110":"p",
    "1101":"q",
    "010":"r",
    "000":"s",
    "1":"t",
    "001":"u",
    "0001":"v",
    "011":"w",
    "1001":"x",
    "1011":"y",
    "1100":"z",
    "":" ",
    "01111": "1",
    "00111": "2",
    "00011": "3",
    "00001": "4",
    "00000": "5",
    "10000": "6",
    "11000": "7",
    "11100": "8",
    "11110": "9",
    "11111": "0",
    "010101": ".",
    "101010": "!",
    "110011": ",",
    "001100": "?",
    }

LPin = 19 #LED light
BPin = 12 #white button
SPin = 16 #blue button
sys_mode = 0 #Variable for defining program settings

def setup():#Sets up all the devices used in the program
    global sys_mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LPin,GPIO.OUT)#Setup for LED light
    GPIO.setup(BPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)#Setup for button
    GPIO.setup(SPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)#Setup for button
    GPIO.output(LPin,GPIO.LOW)#Sets LED to be off
    sys_mode = int(input("Enter 1 for transmitting or 2 for recieving. "))

def transmitter_mode():#Function for flashing morse code using the LED
    message = input("Enter your message to be translated into Morse code: ")
    message = message.lower() #Converse all the characters to lower case
    test = list(message)#Splits all the letters in the message into an array
    for char in test:#Loops over all the characters in test
        morse = morse_dic[char]
        for num in morse:#Loops over all the numbers in morse
            if num == 0:
                short()
            elif num == 1:
                long()
            elif num == "/":
                word()
        
        letter()#Waits for 0.5 seconds to simulate the end of a letter
    
def reciever_mode():
    print("Enter 0 in morse to print out the message")
    print("Press the white button to create a character, and blue to translate it")
    text = ""
    morse = ""
    char = ""
    while True:#Runs until sentinel is achieved
        i = 0
        if GPIO.input(BPin) == 0:#If the white button is pressed
            while GPIO.input(BPin) == 0:#Used to track how long the user presses the button
                time.sleep(0.01)
                i += 1
            if i <= 20:#0.2 seconds or shorter for a 0
                morse += "0"
            elif i > 20:#0.2+ seconds for a 1
                morse += "1"

        if GPIO.input(SPin) == 0:#If the blue button is pressed
            if morse == "11111":#Sentinel
                print(text)
                break
            time.sleep(0.2)#Waits to make sure the sentinel can activate
            char = reverse_morse_dic[morse]
            text += char
            morse = ""
    
def short(): #Function for making the LED flash a 0
    GPIO.output(LPin,GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(LPin,GPIO.LOW)
    time.sleep(0.2)

def long(): #Function for making the LED flash a 1
    GPIO.output(LPin,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LPin,GPIO.LOW)
    time.sleep(0.2)
    
def letter(): #Function for making the LED wait to stimulate the end of a letter
    time.sleep(0.5)

def word(): # Function for making the LED flash a /
    time.sleep(1)
try:
    setup()
    if sys_mode == 1:
        transmitter_mode()
    elif sys_mode == 2:
        reciever_mode()
    else:#Prints a message to stop the program from crashing
        print("Void Input")
except Exception as e:#Another fail safe
    print(e)
GPIO.cleanup()#Clears all input to the hardware
















