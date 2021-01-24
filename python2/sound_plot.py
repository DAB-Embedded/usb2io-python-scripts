import os
import sys
import time
import select
import struct
import numpy as np
import matplotlib.pyplot as plt

fin = open("audio.txt", "rb")
d4 = np.fromfile(fin, dtype=np.int32)
fin.close()


#d4.byteswap(inplace=True)
d4a1 = np.bitwise_and(d4, 0xffffff)
d4a = np.right_shift(d4a1, 8)
print hex(d4a[2])
print hex(d4a[3])
print hex(d4a[4])

d4b = d4a[::2]
d4c = d4a[1::2] - 18900
d4d = d4c - d4b
#d4b = np.hstack((d4a[0], d4a[1]))

fig, ax = plt.subplots()
ax.plot(d4b, label="L")
ax.plot(d4c + 11000, label="R")
ax.plot(d4d, label="D")
ax.legend()
plt.show()
plt.close()