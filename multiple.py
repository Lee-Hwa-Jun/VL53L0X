import time
import board
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X
import matplotlib.pyplot as plt
import numpy as np

i2c = board.I2C()

xshut = [DigitalInOut(board.D7),
DigitalInOut(board.D9),
DigitalInOut(board.D18),
DigitalInOut(board.D17),
DigitalInOut(board.D27)]

vl53 = []
for power_pin in xshut:
    power_pin.switch_to_output(value=False)
for i,power_pin in enumerate(xshut):
    print(i,power_pin)
    power_pin.value = True
    time.sleep(0.5)
    vl53.insert(i,VL53L0X(i2c))

    if i < len(xshut) -1:
        vl53[i].set_address(i+0x30)

subli = [231,232,233,234,235]
pltli = []
for x in vl53:
    pltli.append([])
def detect_range(count=5):
    k=100
    while k:
        for index,sensor in enumerate(vl53):
            print(index+1,sensor.range,end=" ")
            pltli[index].append(sensor.range)
        print("")
        k-=1
    for index,result in enumerate(subli):
        plt.subplot(result)
        pltli[index] = np.array(pltli[index])
        pltli[index][pltli[index]>8000]=0
        plt.plot(np.arange(0.0,100.0,1.0),pltli[index])
    plt.show()

while 1:
    if(input("y/n")=="y"):
        detect_range()
    else:
        break
