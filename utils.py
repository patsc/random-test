import struct
import sys

class Utils():

    @staticmethod
    def float_to_bits(num: float) -> str:
        '''Takes as input a float and return the 23 last bits
        of its representation in bits, that corresponds to the
        fraction portion of the IEEE 754 floating-point
        arithmetic standard.'''
        inp_bytes = struct.pack('!f',num)
        hex_rep = bytes.hex(inp_bytes)
        int_rep = int(hex_rep,16)
        return bin(int_rep)[-23:]

    @staticmethod
    def bytes_to_bits(byte: bytes) -> str:
        ''' Simply returns the bit representation of the byte
        input as a string of 0s and 1s.'''
        return bin(int.from_bytes(byte,sys.byteorder))[2:]

