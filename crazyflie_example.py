from crazyflie_extern import CrazyflieExternController

import time

class Crazyflie(CrazyflieExternController):
    def __init__(self):
        super().__init__(self.run)

    def run(self):
        self.setTarget([1.0,1.0, 1.0])
        for i in range(3):
            print(self.getRange(), self.getPosition())
            time.sleep(1)
        time.sleep(3)
        self.setTarget([0,0,0])


if __name__ == "__main__":
    cf = Crazyflie()