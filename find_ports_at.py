import serial.tools.list_ports
from serial import Serial
import time
from logger import logger


class At:
    def __init__(self):
        self.is_qcom = True
        self.diag_port = self._find_at_port()
        self.modem_port = self._modem_port()

    def _find_at_port(self):
        # 遍历串口，找到diag口
        ports = serial.tools.list_ports.comports()
        diagport = False
        for each_port in ports:
            each_port = each_port.description
            if 'Diag' in each_port:
                diagport = each_port.split(' (')[1].strip(')')
            elif 'SPRD LTE DIAG' in each_port:
                self.is_qcom = False
                diagport = each_port.split(' (')[1].strip(')')
        if diagport == False:
            logger.info("Failed to obtain the DIAG port. Ensure that the device is connected and the DIAG port is not occupied！")
        logger.info(f"diag port {diagport}")
        return diagport

    def _modem_port(self):
        # 尝试找到高通modem口
        if self.diag_port == False:
            return False

        if not self.is_qcom:
            return self._find_spreadtrum_modem_port()

        temp_port = self._find_qcom_modem_port()
        for port in temp_port:
            try:
                ser = Serial(port, 9600, timeout=0.5, writeTimeout=0.5)
                ser.write(b'ate\r\n')
                result = ser.readlines()
                ser.close()
                if result:
                    # logger.info(f"modem port {port}")
                    return port
                else:
                    logger.info("Failed to find the modem port")
            except Exception as e:
                # logger.error(e)
                pass

    def _find_spreadtrum_modem_port(self):
        #获取展讯设备modem口
        try:
            ports = serial.tools.list_ports.comports()
            for each_port in ports:
                each_port = each_port.description
                if 'SPRD LTE AT' in each_port:
                    modem_port = each_port.split(' (')[1].strip(')')
                    logger.info(f"sprd modem port {modem_port}")
                    return modem_port
        except Exception as e:
            logger.error(f"Failed to obtain the spreadtrum modem port.：{e}")
            pass

    def _find_qcom_modem_port(self):
        # 找到diag口后，列出所有可能的高通modem口
        try:
            port_num = int(self.diag_port[3:])
            return (
                "COM" + str(port_num + 1), "COM" + str(port_num - 1), "COM" + str(port_num + 2),
                "COM" + str(port_num - 2),"COM" + str(port_num - 3),"COM" + str(port_num + 3))
        except Exception as e:
            logger.error(f"Failed to obtain the Com modem port{e}")
            pass

    def diag_of_port(self):
        # 返回diag口
        return self.diag_port

    def modem_of_port(self):
        # 返回modem口
        if self.modem_port == None:
            logger.info("Failed to obtain the modem port. Ensure that the device is connected and the modem port is not occupied！")
            return False
        return self.modem_port


if __name__ == "__main__":
    start = time.time()
    test = At()
    print(test.diag_of_port())
    print(test.modem_of_port())
    end = time.time()
    total = end - start
    print(total)
