# LIS3DH Accelerometer I2C Driver for Python3

LIS3DH is an accelerometer manufactured by ST Microelectronics. With this driver, you can use LIS3DH with Python3 over I2C.

## Dependencies
Only smbus2 other than Python. 

## Installation
```bash
pip3 install lis3dh
```

## Usage
From command line;
```bash
run-lis3dh
```
From Python script;
```python
from lis3dh import LIS3DH, device
from time import sleep

registers = device()
lis = LIS3DH(port=1, scale=registers.CTRL_REG4.SCALE_4G, data_rate=registers.CTRL_REG1.ODR_10Hz)

data = lis.read_dummy_register()
print("DUMMY REG CHECK ERROR: " + str(data)) # 0: No Error, -1: Error

lis.enable_axes(registers.CTRL_REG1.Xen | registers.CTRL_REG1.Yen | registers.CTRL_REG1.Zen)

while lis.read_data_ready_register() == lis.ERROR:
    sleep(0.25)

data = lis.read_all_axes()
print("x(g): {}, y(g): {}, z(g): {}".format(data[0], data[1], data[2]))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
