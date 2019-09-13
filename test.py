import os
import subprocess

measure_root = os.environ['MEASURE_ROOT']
cmd = ['rsync', '-av', '--chmod=F644,D755', '/dev/shm/', measure_root]
try:
    res = subprocess.check_call(cmd)
    print(res)
except:
    print("err")
