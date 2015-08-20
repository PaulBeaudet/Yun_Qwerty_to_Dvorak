'''
This is a module for converting evdev key codes from Qwerty to Dvorak
'''
dvorakLookup = {
    "KEY_A": "a",
    "KEY_B": "x",
    "KEY_C": "j",
    "KEY_D": "e",
    "KEY_E": ".",
    "KEY_F": "u",
    "KEY_G": "i",
    "KEY_H": "d",
    "KEY_I": "c",
    "KEY_J": "h",
    "KEY_K": "t",
    "KEY_L": "n",
    "KEY_M": "m",
    "KEY_N": "b",
    "KEY_O": "r",
    "KEY_P": "l",
    "KEY_Q": "'",
    "KEY_R": "p",
    "KEY_S": "o",
    "KEY_T": "y",
    "KEY_U": "g",
    "KEY_V": "k",
    "KEY_W": ",",
    "KEY_X": "q",
    "KEY_Y": "f",
    "KEY_Z": ";",
    "KEY_SEMICOLON": "s",
    "KEY_COMMA": "w",
    "KEY_DOT": "v",
    "KEY_SLASH": "z",
    "KEY_SPACE": " ",
    "KEY_ENTER": "\r",
    "KEY_1": "1",
    "KEY_2": "2",
    "KEY_3": "3",
    "KEY_4": "4",
    "KEY_5": "5",
    "KEY_6": "6",
    "KEY_7": "7",
    "KEY_8": "8",
    "KEY_9": "9",
    "KEY_0": "0",
    "KEY_MINUS": "[",
    "KEY_EQUAL": "]",
    "KEY_APOSTROPHE": "-",
    "KEY_BACKSLASH": "\\",
    "KEY_TAB": "\t",
    "KEY_GRAVE": "`",
    "KEY_BACKSPACE": "\b",
    "KEY_CAPSLOCK": "\b",
    "KEY_RIGHTBRACE": "=",
    "KEY_LEFTBRACE": "/"

}

def toDvorak(key):
    try:
        return dvorakLookup[key]
    except KeyError, e:
        return "error"
