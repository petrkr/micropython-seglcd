"""
Character to Segment Mapping
Converts ASCII characters to 7-segment and 16-segment display patterns
"""


def get_char_value(ch):
    """
    Convert character to 7-segment display pattern.

    Segment mapping (ABCDEFGH):
        AAA
       F   B
       F   B
        GGG
       E   C
       E   C
        DDD   H(DP)

    Args:
        ch: Character (str or int/byte)

    Returns:
        8-bit segment pattern (int) where bits represent: ABCDEFGH
    """
    if isinstance(ch, str):
        ch = ord(ch) if len(ch) == 1 else 0

    # Digit mapping
    _SEGMENTS = {
        ord(' '): 0x00,
        ord('0'): 0b11111100,
        ord('1'): 0b01100000,
        ord('2'): 0b11011010,
        ord('3'): 0b11110010,
        ord('4'): 0b01100110,
        ord('5'): 0b10110110,
        ord('6'): 0b10111110,
        ord('7'): 0b11100000,
        ord('8'): 0b11111110,
        ord('9'): 0b11110110,

        # Letters (uppercase)
        ord('A'): 0b11101110,
        ord('B'): 0b00111110,
        ord('C'): 0b10011100,
        ord('D'): 0b01111010,
        ord('E'): 0b10011110,
        ord('F'): 0b10001110,
        ord('G'): 0b11110110,
        ord('H'): 0b01101110,
        ord('I'): 0b01100000,
        ord('J'): 0b01111000,
        ord('K'): 0b10101110,
        ord('L'): 0b00011100,
        ord('M'): 0b10101010,
        ord('N'): 0b11101100,
        ord('O'): 0b11111100,
        ord('P'): 0b11001110,
        ord('Q'): 0b11100110,
        ord('R'): 0b00001010,
        ord('S'): 0b10110110,
        ord('T'): 0b00011110,
        ord('U'): 0b01111100,
        ord('V'): 0b01010100,
        ord('W'): 0b01010110,
        ord('X'): 0b01101110,
        ord('Y'): 0b01110110,
        ord('Z'): 0b11011010,

        # Letters (lowercase)
        ord('a'): 0b11101110,
        ord('b'): 0b00111110,
        ord('c'): 0b00011010,
        ord('d'): 0b01111010,
        ord('e'): 0b10011110,
        ord('f'): 0b10001110,
        ord('g'): 0b11110110,
        ord('h'): 0b00101110,
        ord('i'): 0b00100000,
        ord('j'): 0b01111000,
        ord('k'): 0b10101110,
        ord('l'): 0b00011000,
        ord('m'): 0b10101010,
        ord('n'): 0b00101010,
        ord('o'): 0b00111010,
        ord('p'): 0b11001110,
        ord('q'): 0b11100110,
        ord('r'): 0b00001010,
        ord('s'): 0b10110110,
        ord('t'): 0b00011110,
        ord('u'): 0b00111000,
        ord('v'): 0b01010100,
        ord('w'): 0b01010110,
        ord('x'): 0b00101000,
        ord('y'): 0b01110110,
        ord('z'): 0b11011000,

        # Special characters
        ord('*'): 0b11000110,
        ord(','): 0b00001000,
        ord('.'): 0b00010000,
        ord('/'): 0b01001010,
        ord('~'): 0b10000000,
        ord('-'): 0b00000010,
        ord('_'): 0b00010000,
        ord(':'): 0b00010010,
        ord('|'): 0b00001100,
        ord('"'): 0b01000100,
        ord('('): 0b10011100,
        ord('['): 0b10011100,
        ord(')'): 0b11110000,
        ord(']'): 0b11110000,
    }

    return _SEGMENTS.get(ch, 0x00)


def get_16char_value(ch):
    """
    Convert character to 16-segment display pattern.

    Segment mapping (A1A2BCD2D1EFG1G2HIJKLM):
         A1  A2
        F  J K  B
        F  J K  B
         G1  G2
        E  M L  C
        E  M L  C
         D1  D2   I(DP)

    Args:
        ch: Character (str or int/byte)

    Returns:
        16-bit segment pattern (int)
    """
    if isinstance(ch, str):
        ch = ord(ch) if len(ch) == 1 else 0

    # 16-segment mapping
    _SEGMENTS_16 = {
        ord(' '): 0b0000000000000000,
        ord('0'): 0b1111111100001100,
        ord('1'): 0b0011000000000000,
        ord('2'): 0b1110111011000000,
        ord('3'): 0b1111110011000000,
        ord('4'): 0b0011000111000000,
        ord('5'): 0b1101110111000000,
        ord('6'): 0b1101111111000000,
        ord('7'): 0b1111000000000000,
        ord('8'): 0b1111111111000000,
        ord('9'): 0b1111110111000000,

        # Uppercase letters
        ord('A'): 0b1111001111000000,
        ord('B'): 0b1111110001010010,
        ord('C'): 0b1100111100000000,
        ord('D'): 0b1111110000010010,
        ord('E'): 0b1100111110000000,
        ord('F'): 0b1100001110000000,
        ord('G'): 0b1101111101000000,
        ord('H'): 0b0011001111000000,
        ord('I'): 0b1100110000010010,
        ord('J'): 0b0011111000000000,
        ord('K'): 0b0000001110001001,
        ord('L'): 0b0000111100000000,
        ord('M'): 0b0011001100101000,
        ord('N'): 0b0011001100100001,
        ord('O'): 0b1111111100000000,
        ord('P'): 0b1110001111000000,
        ord('Q'): 0b1111111100000001,
        ord('R'): 0b1110001111000001,
        ord('S'): 0b1101110111000000,
        ord('T'): 0b1100000000010010,
        ord('U'): 0b0011111100000000,
        ord('V'): 0b0000001100001100,
        ord('W'): 0b0011001100000101,
        ord('X'): 0b0000000000101101,
        ord('Y'): 0b0000000000101010,
        ord('Z'): 0b1100110000001100,

        # Lowercase letters
        ord('a'): 0b0000111010000010,
        ord('b'): 0b0001111111000000,
        ord('c'): 0b0000111011000000,
        ord('d'): 0b0011111011000000,
        ord('e'): 0b0000111010000100,
        ord('f'): 0b0100000011010010,
        ord('g'): 0b0000101010000101,
        ord('h'): 0b0001001111000000,
        ord('i'): 0b1000110010000010,
        ord('j'): 0b0101110001000000,
        ord('k'): 0b0000001111000001,
        ord('l'): 0b1000100000010010,
        ord('m'): 0b0001001011000010,
        ord('n'): 0b0001001011000000,
        ord('o'): 0b0001111011000000,
        ord('p'): 0b0001010001000011,
        ord('q'): 0b0001111011000001,
        ord('r'): 0b0000001011000000,
        ord('s'): 0b0000110001000001,
        ord('t'): 0b0000100011010010,
        ord('u'): 0b0001111000000000,
        ord('v'): 0b0000001000000100,
        ord('w'): 0b0001001000000101,
        ord('x'): 0b0000000011000101,
        ord('y'): 0b0001110000000001,
        ord('z'): 0b0000010010000100,

        # Special characters
        ord('*'): 0b0000000011111111,
        ord(','): 0b0000000000000100,
        ord('.'): 0b0000010000000000,
        ord('/'): 0b0000000000001100,
        ord('\\'): 0b0000000000100001,
        ord('~'): 0b1100000000000000,
        ord('+'): 0b0000000011010010,
        ord('-'): 0b0000000011000000,
        ord('_'): 0b0000110000000000,
        ord(':'): 0b0000010010000000,
        ord('='): 0b0000110011000000,
        ord('|'): 0b0000000000010010,
        ord('"'): 0b0000000000101000,
        ord('('): 0b0000000000001001,
        ord(')'): 0b0000000000100100,
        ord('['): 0b0100100000010010,
        ord(']'): 0b1000010000010010,
        ord('{'): 0b0100100010010010,
        ord('}'): 0b1000010001010010,
    }

    return _SEGMENTS_16.get(ch, 0b0000000000000000)
