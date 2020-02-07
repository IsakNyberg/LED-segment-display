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

    'A': 0b01110111,
    'E': 0b01001111,
    'F': 0b01000111,
    'H': 0b00110111,
    'I': 0b00110000,
    'L': 0b00001110,
    'N': 0b01110110,
    'O': 0b01111110,
    'P': 0b01100111,
    'S': 0b01011011,
    'Y': 0b00111011,
    'V': 0b00111110,
    
    'a': 0b
    'b': 0b00011111,
    'C': 0b01001110,
    'd': 0b00111101,
    'e': 0b01101111,
    'i': 0b00110000,
    'n': 0b00010101,
    'o': 0b00011101,
    's': 0b01011011,
    't': 0b00001111,
    
    "'": 0b01100011,
    ' ': 0b00000000,
    '.': 0b10000000,
    ':': 0b10000000,
    '=': 0b00001001,
    '-': 0b00000001,
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
