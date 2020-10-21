import struct
import math
import sys
from abc import ABC, abstractmethod

class BaseTest(ABC):

    @staticmethod
    @abstractmethod
    def test_bits(bits: str) -> bool:
        pass


class UniversalTest(BaseTest):
    # expected and variance denote the expected value
    # and variance for block lengths between 8 and 16
    # bits
    expected = {
            8: 7.1836656,
            9: 8.1764258,
            10: 9.1723243,
            11: 10.170032,
            12: 11.168765,
            13: 12.168070,
            14: 13.167693,
            15: 14.167488,
            16: 15.167379
            }

    variance = {
            8: 3.238,
            9: 3.311,
            10: 3.356,
            11: 3.384,
            12: 3.401,
            13: 3.410,
            14: 3.416,
            15: 3.419,
            16: 3.421,
            }

    @staticmethod
    def approx_variance_correction(l: int, k: int) -> float:
        return 0.7 - 0.8 / l + (4 + 32 / l) * pow(k,-3 / l) / 15

    @staticmethod
    def universal_test(bits: str, l: int, q: int, k: int) -> float:
        latest_block_map = {}
        latest = 0
        ftu = 0.0
        if ((q + k) * l > len(bits)):
            raise ValueError('Bitstring length and paramters inconsistent!')

        bitstring = bits[:(q+k)*l]

        for i in range(q):
            latest_block_map.update({int(bitstring[i*l:(i+1)*l],2):i})

        for j in range(k):
            current_bitstring = bitstring[(q+j)*l:(q+j+1)*l]
            current_number = int(current_bitstring,2)
            try:
                latest = latest_block_map[current_number]
                latest_block_map.update({current_number:q+j})
            except KeyError:
                latest_block_map.update({current_number:q+j})
                latest = 0
            ftu += math.log2(q + j - latest)

        return ftu / k

    @staticmethod
    def test_bits(bits: str) -> bool:
        '''
        This is a sample implementation of Maurer's universal statistical
        test. The block length l has been set to 10, the rejection rate
        to 0.001. using the method universal_test() the test-parameters
        can be choosen according to the needs.
        '''
        l = 10
        if (len(bits) < (pow(2,l)*100)):
                raise ValueError('Input too small for a significant test.')

        q = pow(2,l) * pow(2,l // 2) // l
        k = (len(bits) - q * l) // l
        clk = UniversalTest.approx_variance_correction(l,k)
        sigma = clk*math.sqrt(UniversalTest.variance[l] / k)
        # choice of 2.58 results in a rejection of 0.001
        # could be set to 3.30 for a rejection rate of 0.01
        t1 = UniversalTest.expected[l] - 2.58 * sigma
        t2 = UniversalTest.expected[l] + 2.58 * sigma
        unitest = UniversalTest.universal_test(bits,l,q,k)
        return (t1 < unitest) & (t2 > unitest)

