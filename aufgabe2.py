from crazyflie_extern import CrazyflieExternController

# import matplotlib
# matplotlib.use('Agg')
# plt.savefig('graph.png')

import matplotlib.pyplot as plt
import numpy as np

import time


class Crazyflie(CrazyflieExternController):
    def __init__(self):
        super().__init__(self.run)

    def run(self):
        self.setTarget([0, 0, 1])
        time.sleep(5)

        positions = []
        ranges = []

        self.move_to([0.0, 1.0, 1.0], positions, ranges)
        self.move_to([1.0, 1.0, 1.0], positions, ranges)
        self.move_to([0.0, 0.0, 1.0], positions, ranges)

        # time.sleep(3)
        self.setTarget([0, 0, 0])
        self.plot_range(positions, ranges)

    def move_to(self, pos, positions, ranges):
        self.setTarget(pos)
        moving = True
        last_time = time.time()
        while moving:
            current_pos = self.getPosition()
            current_time = time.time()
            if (current_time - last_time) > .1:
                print(current_time)
                last_time = current_time
                positions.append(current_pos)
                ranges.append(self.getRange())
            if (abs(pos[0] - current_pos[0]) < .1) and (abs(pos[1] - current_pos[1]) < .1) and (
                    abs(pos[2] - current_pos[2]) < .1):
                moving = False
                print("arrived: ", current_pos)

    def plot_range(self, positions, ranges):
        print(len(positions))

        # Create a figure containing a single Axes.
        fig, ax = plt.subplots()

        #
        x_positions = [row[0] for row in positions]
        y_positions = [row[1] for row in positions]
        sizes = list(map(lambda range1: range1 / 10, ranges))
        colors = list(map(lambda range1: range1 * 100, ranges))

        # Plot some data on the Axes.
        ax.scatter(x_positions, y_positions, s=sizes, c=colors, cmap='viridis')
        plt.show()  # Show the figure.


if __name__ == "__main__":
    cf = Crazyflie()
