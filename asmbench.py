# File (bench.S) should be in the current directory
from projectrv64 import rv64
import time
import os
icount = 500000
t = 0.0
path = f'{os.path.dirname(__file__)}/bench.S'
while t < 9.9 or t > 10.1:
    tstart = time.perf_counter()
    rv64.execute(path, imax = icount)
    tend = time.perf_counter()
    t = tend - tstart
    icount = int(round(icount * 10 / t))
print(round(icount / t))