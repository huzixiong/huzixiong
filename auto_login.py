import subprocess
import time

class AutoInOut:
    def __init__(self):
        pass

    def login(self):
        result = subprocess.getstatusoutput("adb shell am broadcast -a com.ucloudlink.cmd.login")[0]
        if result == 0:
            return True
        return False

    def logout(self):
        result = subprocess.getstatusoutput("adb shell am broadcast -a com.ucloudlink.cmd.logout")[0]
        if result == 0:
            return True
        return False

    def wait_some_time(self,*args):
        time.sleep(*args)

    def action(self):
        self.logout()
        self.wait_some_time(10)
        self.login()
        self.wait_some_time(80)

def main():
    a = AutoInOut()
    while True:
        a.action()

if __name__ == "__main__":
    main()




