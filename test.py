import datetime
import time
import subprocess
def TimeOut(timeout = None):

    endtime = 0
    if timeout:
        endtime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    while True:
        time.sleep(0.1)
        if endtime <= datetime.datetime.now():
            raise Exception("timeout!")
def subprocess_test():
    s = subprocess.Popen("adb devices")
    t = s.communicate()
    return t

if __name__  =="__main__":
    # TimeOut(10)
    subprocess_test()
    print("test")