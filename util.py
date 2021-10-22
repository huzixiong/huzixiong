import subprocess
import time

from find_ports_at import At
from logger import logger


def get_device_connect():
    try:
        time.sleep(1)
        device_list = subprocess.check_output("adb devices").decode()

        if device_list.find('\tdevice') == -1:
            logger.info(f'can not find devices {device_list}')
            return False
        else:
            device_list = device_list.strip().replace('\r\n',' ')
            logger.info(f"find devices {device_list.strip()}")
            return True
    except Exception as e:
        logger.error(e)
        pass


def get_diag_port():
    return At().diag_port


def get_modem_port():
    return At().modem_port


# def network_ping_success():
#     while True:
#         time.sleep(1)
#         result = subprocess.getstatusoutput("adb shell ping -c 1 www.xiaomi.com")[1].find("0%")
#         logger.info(f"ping www.xiaomi.com result:{result}")
#         if result != -1:
#             logger.info("vsim network ping success!")
#             return True

def network_ping_success():
    while True:
        try:
            time.sleep(1)
            process = subprocess.Popen("adb shell ping -c 1 www.xiaomi.com", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            inf,err = process.communicate(timeout = 10)
            logger.info(inf)
            if err == b'':
                if inf.decode('utf-8').find("0%") != -1:
                    logger.info(f"vsim ping success!{inf}")
                    return True
            else:
                logger.error(err)
        except subprocess.TimeoutExpired as e:
            logger.error(e)



def get_ping_status():
    result = subprocess.getstatusoutput("adb shell ping -c 1 8.8.8.8")[1].find("0%")
    # print("ping state")
    if result != -1:
        logger.info("ping success!")
        return True
    else:
        logger.info("ping fail!")
        return False


def cloudsim_socketState():
    time.sleep(0.5)
    result = subprocess.getoutput("adb shell getprop ucloud.android.network.state")
    logger.info(f"ucloud.android.network.state {result}")
    if result == '1':
        return True
    else:
        return False

def switch_vsim_one():
    try:
        cmd_res = subprocess.check_output('adb shell am broadcast -a com.ucloudlink.switch.vsim.plmn').decode()
        if cmd_res.find('result=0') != -1:
            logger.info("Send switch vsim command succeeded！")
        else:
            logger.info("Send switch vsim command failed!")
    except Exception as e:
        logger.error(e)

def qcom_root_device():
    cmd_res = subprocess.check_output('adb shell am broadcast -n com.ukl.factory/.UklRootReceiver -a android.intent.action.OpenRoot').decode()
    if cmd_res.find('OpenRoot') != -1:
        logger.info("Send root command succeeded！")
    else:
        logger.info("Send root command failed!")

def get_strf_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))




if __name__ == "__main__":
    # get_device_connect()
    # get_diag_port()
    # get_modem_port()
    # get_ping_status()
    # cloudsim_socketState()
    # network_ping_success()
    # At().modem_of_port()
    # qcom_root_device()
    # switch_vsim_one()
    network_ping_success()
