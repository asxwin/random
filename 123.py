from scipy.io import wavfile
import numpy as np
import functools

sr, x = wavfile.read('sound.wav')  # read a mono audio file, recorded with your computer's built-in microphone

#### GET A LIST OF ALL THE BITS
L = []  # list of bits
for i in range(len(x)):
    bits = format(abs(x[i]), "b")  # get binary representation of the data
                                   # don't use "016b" format because it would create a bias: small integers (those not using
                                   # the full bit 16-bit amplitude) would have many leading 0s!
    L += map(int, bits)[1:]        # discard the first bit, which is always 1!

print L.count(1)
print L.count(0)  # check if it's equidistributed in 0s and 1s

n = 2 ** int(np.log2(len(L)))
L = L[:n]  # crop the array of bits so that the length is a power of 2; well the only requirement is that len(L) is coprime with p (see below)

### RECREATE A NEW BINARY FILE WITH ALL THESE BITS (SHUFFLED)
# The trick is: don't use **consecutive bits**, as it would recreate something close to the input audio data. 
# Let's take one bit every 96263 bits instead! Why 96263? Because it's a prime number, then we are guaranteed that
# 0 * 96263 mod n, 1 * 96263 mod n, 2 * 96263 mod n, ..., (n-1) * 96263 mod n will cover [0, 1, ..., n-1].  (**)
# This is true since 96263 is coprime with n. In math language: 96253 is a "generator" of (Z/nZ, +).

p = 96263  # The higher this prime number, the better the shuffling of the bits! 
           # If you have at least one minute of audio, you have at least 45 millions of useful bits already, 
           # so you could take p = 41716139 (just a random prime number I like around 40M)

M = set()
with open('random.raw', 'wb') as f:
    for i in range(0, n, 8):
        M.update(set([(k * p) % n for k in range(i, i+8)]))  # this is optional, here just to prove that our math claim (**) is true
        c = [L[(k * p) % n] for k in range(i, i+8)]   # take 8 bits, in shuffled order
        char = chr(functools.reduce(lambda a, b: a * 2 + b, c))  # create a char with it
        f.write(char)

print M  == set(range(n))  # True, this shows that the assertion (**) before is true. Math rulez!