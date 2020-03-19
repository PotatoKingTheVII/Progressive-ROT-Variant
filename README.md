## Cipher and file breakdown
I came across this cipher in a puzzle and decided to create a slightly more complicated version. I've looked around and still aren't 100% sure on it's name but it can be thought of as a progressive ROT variant or even a vigenere variant. The basic premise is similar to affine in that the shift of the current letter is the a0z25 value of the previous letter multiplied by a mlt factor and with a shift added (all mod 26) (The first letter has a shift of 0).

The Bruteforce is done by ordering all combinations with a chi-squared statistic of their letter frequencies compared to the expected English results. This is a basic approach and works best with a decently sized cipher-text.

I'd be very interested if anyone knows the proper name or term for this cipher.
## File usage
The CipherGUI file allows encoding and decoding with specific multiplication and shift values from 0-26 with a tkinter interface. The Bruteforce file attempts every combination of shift and multiplication values from 1-26 and both prints and writes them to a file in the order of most likely to least.

## Dependancies
 - numpy
