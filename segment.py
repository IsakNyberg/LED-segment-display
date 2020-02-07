#!/usr/bin/env python

# DP A B C D E F G
digit_register = {
    0: 0b01111110,
    1: 0b00110000,
    2: 0b01101101,
    3: 0b01111001,
    4: 0b00110011,
    5: 0b01011011,
    6: 0b01011111,
    7: 0b01110000,
    8: 0b01111111,
    9: 0b01111011,

    ' ': 0b00000000,
    '!': 0b10110000,
    '"': 0b00100010,
    '#': 0b00111111,
    '$': 0b01011011,
    '%': 0b10100101,
    '&': 0b00110001,
    "'": 0b00000010,
    '(': 0b01001010,
    ')': 0b01101000,
    '*': 0b01000010,
    '+': 0b00000111,
    "'": 0b00000100,
    '-': 0b00000001,
    '.': 0b10000000,
    '/': 0b00100101,
    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,
    ':': 0b01001000,
    ';': 0b01011000,
    '<': 0b01000011,
    '=': 0b00001001,
    '>': 0b01100001,
    '?': 0b11100101,
    '@': 0b01111101,
    'A': 0b01110111,
    'B': 0b00011111,
    'C': 0b01001110,
    'D': 0b00111101,
    'E': 0b01001111,
    'F': 0b01000111,
    'G': 0b01011110,
    'H': 0b00110111,
    'I': 0b00000110,
    'J': 0b00111100,
    'K': 0b01010111,
    'L': 0b00001110,
    'M': 0b01010100,
    'N': 0b01110110,
    'O': 0b01111110,
    'P': 0b01100111,
    'Q': 0b01101011,
    'R': 0b01100110,
    'S': 0b01011011,
    'T': 0b00001111,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b00110111,
    'Y': 0b00111011,
    'Z': 0b01101101,
    '[': 0b01001110,
    '\\': 0b00010011,
    ']': 0b01111000,
    '^': 0b01100010,
    '_': 0b00001000,
    '`': 0b00100000,
    'a': 0b01111101,
    'b': 0b00011111,
    'c': 0b00001101,
    'd': 0b00111101,
    'e': 0b01101111,
    'f': 0b01000111,
    'g': 0b01111011,
    'h': 0b00010111,
    'i': 0b00000100,
    'j': 0b00011000,
    'k': 0b01010111,
    'l': 0b00000110,
    'm': 0b00010100,
    'n': 0b00010101,
    'o': 0b00011101,
    'p': 0b01100111,
    'q': 0b01110011,
    'r': 0b00000101,
    's': 0b01011011,
    't': 0b00001111,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b00110111,
    'y': 0b00111011,
    'z': 0b01101101,
    '{': 0b00110001,
    '|': 0b00000110,
    '}': 0b00000111,
    '~': 0b01000000
}

def to_segment(n, length=4):
    if type(n) is int:
        return int_to_segment(n, length)
    if type(n) is str:
        return str_to_segment(n, length)
    if type(n) is float:
        return float_to_segment(n, length)

def int_to_segment(n, length=4):
    res = []
    for i in str(n).rjust(length, ' ')[:length]:
        res.append(digit_register[i])
    return res

def str_to_segment(n, length=4):
    res = []
    for i in n.rjust(length, ' ')[:length]:
        res.append(digit_register[i])
    return res

def float_to_segment(n, length=4):
    res = []

    if n < 10 ** (length-1):  # this means the comma needs to be accounted for
        for i in str(n).rjust(length+1, ' ')[:length+1]:
            if digit_register[i] == 0x80:  # add comma to previous digit
                res[-1] |= digit_register[i]
            else:
                res.append(digit_register[i])
    else:
        res = int_to_segment(int(n), length)
    return res
