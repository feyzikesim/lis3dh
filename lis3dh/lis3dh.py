from smbus2 import SMBus, i2c_msg
from time import sleep

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

class device():
    LIS3DH_ADDR = 0x18

    REFERENCE = 0x26
    INT1_THS = 0x32
    INT1_DURATION = 0x33
    INT2_THS = 0x36
    INT2_DURATION = 0x37
    CLICK_THS = 0x3A
    TIME_LIMIT = 0x3B
    TIME_LATENCY = 0x3C
    TIME_WINDOW = 0x3D
    ACT_THS = 0x3E
    ACT_DUR = 0x3F

    class STATUS_REG_AUX():
        ADDR = 0x07
        OR321 = 0x80
        OR3 = 0x40
        OR2 = 0x20
        OR1 = 0x10
        DA321 = 0x08
        DA3 = 0x04
        DA2 = 0x02
        DA1 = 0x01

    class OUT_ADC():
        OUT_ADC1_L = 0x08
        OUT_ADC1_H = 0x09
        OUT_ADC2_L = 0x0A
        OUT_ADC2_H = 0x0B
        OUT_ADC3_L = 0x0C
        OUT_ADC3_H = 0x0D

    class WHO_AM_I():
        ADDR = 0x0F
        WHO_AM_I = 0x33

    class CTRL_REG0():
        ADDR = 0x1E
        SDO_PU_DISC = 0x80

    class TEMP_CFG_REG():
        ADDR = 0x1F
        ADC_EN = 0x80
        TEMP_EN = 0x40

    class CTRL_REG1():
        ADDR = 0x20
        POWER_DOWN = 0x00
        ODR_1Hz    = 0x10
        ODR_10Hz   = 0x20
        ODR_25Hz   = 0x30
        ODR_50Hz   = 0x40
        ODR_100Hz  = 0x50
        ODR_200Hz  = 0x60
        ODR_400Hz  = 0x70
        ODR_LOWPOWER_1k6Hz   = 0x80
        ODR_LOWPOWER_5k376Hz = 0x90
        LPen = 0x08
        Zen = 0x04
        Yen = 0x02
        Xen = 0x01

    class CTRL_REG2():
        ADDR = 0x21
        HPM1 = 0x80
        HPM0 = 0x40
        HPCF2 = 0x20
        HPCF1 = 0x10
        FDS = 0x08
        HPCLICK = 0x04
        HP_IA2 = 0x02
        HP_IA1 = 0x01

    class CTRL_REG3():
        ADDR = 0x22
        I1_CLICK = 0x80
        I1_IA1 = 0x40
        I1_IA2 = 0x20
        I1_ZYXDA = 0x10
        I1_321DA = 0x08
        I1_WTM = 0x04
        I1_OVERRUN = 0x02

    class CTRL_REG4():
        ADDR = 0x23
        BDU = 0x80
        BLE = 0x40
        SCALE_2G = 0x00
        SCALE_4G = 0x10
        SCALE_8G = 0x20
        SCALE_16G = 0x30
        HR = 0x08
        ST1 = 0x04
        ST0 = 0x02
        SIM = 0x01

    class CTRL_REG5():
        ADDR = 0x24
        BOOT = 0x80
        FIFO_EN = 0x40
        LIR_INT1 = 0x08
        D4D_INT1 = 0x04
        LIR_INT2 = 0x02
        D4D_INT2 = 0x01

    class CTRL_REG6():
        ADDR = 0x25
        I2_CLICK = 0x80
        I2_IA1 = 0x40
        I2_IA2 = 0x20
        I2_BOOT = 0x10
        I2_ACT = 0x08
        INT_POLARITY = 0x02

    class STATUS_REG():
        ADDR = 0x27
        ZYXOR = 0x80
        ZOR = 0x40
        YOR = 0x20
        XOR = 0x10
        ZYXDA = 0x08
        ZDA = 0x04
        YDA = 0x02
        XDA = 0x01

    class OUT_VALUE():
        OUT_X_L = 0x28
        OUT_X_H = 0x29
        OUT_Y_L = 0x2A
        OUT_Y_H = 0x2B
        OUT_Z_L = 0x2C
        OUT_Z_H = 0x2D

    class FIFO_CTRL_REG():
        ADDR = 0x2E
        BYPASS_MODE = 0x00
        FIFO_MODE = 0x40
        STREAM_MODE = 0x80
        STREAM_TO_FIFO = 0xC0
        TR = 0x20
        FTH4 = 0x10
        FTH3 = 0x08
        FTH2 = 0x04
        FTH1 = 0x02
        FTH0 = 0x01

    class FIFO_SRC_REG():
        ADDR = 0x2F
        WTM = 0x80
        OVRN_FIFO = 0x40
        EMPTY = 0x20
        FSS4 = 0x10
        FSS3 = 0x08
        FSS2 = 0x04
        FSS1 = 0x02
        FSS0 = 0x01

    class INT1_CFG():
        ADDR = 0x30
        AOI = 0x80
        D6 = 0x40
        ZHIE = 0x20
        ZLIE = 0x10
        YHIE = 0x08
        YLIE = 0x04
        XHIE = 0x02
        XLIE = 0x01

    class INT1_SRC():
        ADDR = 0x31
        IA = 0x40
        ZH = 0x20
        ZL = 0x10
        YH = 0x08
        YL = 0x04
        XH = 0x02
        XL = 0x01

    class INT2_CFG():
        ADDR = 0x34
        AOI = 0x80
        D6 = 0x40
        ZHIE = 0x20
        ZLIE = 0x10
        YHIE = 0x08
        YLIE = 0x04
        XHIE = 0x02
        XLIE = 0x01

    class INT2_SRC():
        ADDR = 0x35
        IA = 0x40
        ZH = 0x20
        ZL = 0x10
        YH = 0x08
        YL = 0x04
        XH = 0x02
        XL = 0x01

    class CLICK_CFG():
        ADDR = 0x38
        ZD = 0x20
        ZS = 0x10
        YD = 0x08
        YS = 0x04
        XD = 0x02
        XS = 0x01

    class CLICK_SRC():
        ADDR = 0x39
        IA = 0x40
        DCLICK = 0x20
        SCLICK = 0x10
        SIGN = 0x08
        Z = 0x04
        Y = 0x02
        X = 0x01

class LIS3DH():
    NO_ERROR = 0
    ERROR = -1

    def __init__(self, port, scale, data_rate):
        self.bus = SMBus(port)
        self.dev = device()
        self.set_scale(scale)
        self.set_data_rate(data_rate)

    def read_dummy_register(self):
        dummy = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.WHO_AM_I.ADDR)

        if dummy == self.dev.WHO_AM_I.WHO_AM_I:
            return self.NO_ERROR
        else:
            return self.ERROR

    def set_scale(self, scale):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG4.ADDR)

        data &= 0xCF
        data |= scale

        self.bus.write_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG4.ADDR, data)

    def get_scale(self):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG4.ADDR)

        data &= 0x30

        return data

    def set_data_rate(self, rate):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG1.ADDR)

        data &= 0x0F
        data |= rate

        self.bus.write_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG1.ADDR, data)

    def get_data_rate(self):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG1.ADDR)

        data &= 0xF0

        return data

    def enable_axes(self, axes):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG1.ADDR)

        data &= 0xF8
        data |= axes

        self.bus.write_byte_data(self.dev.LIS3DH_ADDR, self.dev.CTRL_REG1.ADDR, data)

    def read_data_ready_register(self):
        data = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.STATUS_REG.ADDR)

        control = data >> 3
        control &= 0x01

        if data & 0x01:
            return self.NO_ERROR
        else:
            return self.ERROR

    def read_all_axes(self):
        data_list = []

        scale = self.get_scale()

        if scale == self.dev.CTRL_REG4.SCALE_2G:
            factor = 0.061
        elif scale == self.dev.CTRL_REG4.SCALE_4G:
            factor = 0.122
        elif scale == self.dev.CTRL_REG4.SCALE_8G:
            factor = 0.183
        elif scale == self.dev.CTRL_REG4.SCALE_16G:
            factor = 0.732

        x_low = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_X_L)
        x_high = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_X_H)
        y_low = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_Y_L)
        y_high = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_Y_H)
        z_low = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_Z_L)
        z_high = self.bus.read_byte_data(self.dev.LIS3DH_ADDR, self.dev.OUT_VALUE.OUT_Z_H)

        x = (((x_high << 8) | x_low) - 32768.0) * factor / 1000
        y = (((y_high << 8) | y_low) - 32768.0) * factor / 1000
        z = (((z_high << 8) | z_low) - 32768.0) * factor / 1000

        data_list.append(x)
        data_list.append(y)
        data_list.append(z)

        return data_list

    def write_register(self, register_addr, value):
        self.bus.write_byte_data(self.dev.LIS3DH_ADDR, register_addr, value)

    def read_register(self, register_addr):
        return self.bus.read_byte_data(self.dev.LIS3DH_ADDR, register_addr)
