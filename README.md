# Statistical Tests for Sources of Radomness

The main goal of this repository is to provide a set of statistical tests, that to test the quality of sources of randomness.

To test the stistical quality of `os.urandom`, onw could for example use the tools as follows:

```
import os
import sys
import statistic_tests

test_randomness = ''
for i in range(700):
    test_randomness += bin(int.from_bytes(os.urandom(200),sys.byteorder))[2:]
statistic_tests.UniversalTest.test.bits(test_randomness)
```

If the previous code outputs `True` the bit-string `test_randomness` passes Maurer's universal statistical test (with a rejection rate of 0.01).
