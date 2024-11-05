import time
from typing import Iterable, Any

import matplotlib.pyplot as plt
import numpy as np
from _ctypes import Array
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.image import AxesImage
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.interpolate import griddata

from crazyflie_extern import CrazyflieExternController


# import matplotlib
# matplotlib.use('Agg')
# plt.savefig('graph.png')


def interpolate(data):
    # Meshgrid für die Positionen der Daten erstellen
    x = np.arange(data.shape[1])
    y = np.arange(data.shape[0])
    xx, yy = np.meshgrid(x, y)

    # Nur die Positionen und Werte der gültigen Daten extrahieren
    valid_points = ~np.isnan(data)
    points = np.column_stack((xx[valid_points], yy[valid_points]))
    values = data[valid_points]

    # Zielkoordinaten für die Interpolation
    grid_x, grid_y = np.meshgrid(x, y)

    # Interpolation durchführen
    interpolated_data = griddata(points, values, (grid_x, grid_y), method='linear')

    # NaN-Werte außerhalb des Interpolationsbereichs auf 0 oder einen anderen Wert setzen
    return np.nan_to_num(interpolated_data)


def plot_range(area_len, positions, ranges, step_count=40):
    """
    Plots a 3D surface plot of positions with heights based on ranges.

    :param area_len: Length of a side of the area.
    :param positions: List of [x, y] positions.
    :param ranges: List of range values corresponding to the positions.
    :param step_count: Number of steps in the x and y direction.
    """
    ranges_count = len(ranges)

    factor = round(step_count / np.sqrt(ranges_count)) or 1

    # Create a grid of x and y values.
    xs = np.linspace(0, area_len, round(np.sqrt(ranges_count)) * factor + 1)
    ys = np.linspace(0, area_len, round(np.sqrt(ranges_count)) * factor + 1)
    X, Y = np.meshgrid(xs, ys)

    # Initialize Z values to NaN. (NaN-values will be interpolated)
    Z = np.full(X.shape, np.nan)

    # Initialize Z count values to zero.
    z_count = np.zeros(X.shape)

    # Populate Z values based on positions and ranges.
    for i, pos in enumerate(positions):
        x_index = int(pos[1] / area_len * np.sqrt(ranges_count) * factor)
        y_index = int(pos[0] / area_len * np.sqrt(ranges_count) * factor)

        # Add the range value to the Z value or set it to the range value if it is NaN.
        Z[x_index, y_index] = (0 if np.isnan(Z[x_index, y_index]) else Z[x_index, y_index]) + ranges[i] / 1000
        z_count[x_index, y_index] += 1

    # Calculate average Z values.
    # Z = np.divide(Z, z_count, out=Z, where=z_count != 0)
    np.divide(Z, z_count, out=Z, where=z_count != 0)
    # Z = np.true_divide(Z, z_count, where=z_count != 0)

    # print which values are NaN with 🟥 and 🟩
    # for row in np.array(Z):
    #     print('\u2009'.join(np.where(np.isnan(row), "🟥", "🟩")))

    # plot_range_2d(Z)
    zz_interpolated = interpolate(Z)

    # Create a plotter object with 1 row and 2 columns.
    # plotter = Plotter(2, 2)
    plotter = Plotter(1, 2)

    # Add 2D, 2D-Scatter and 3D plots
    # plotter.add_plot_range_3d(X, Y, Z)
    plotter.add_plot_range_3d(X, Y, zz_interpolated, "Interpoliertes 3D-Höhenprofil")

    # plotter.add_plot_range_2d(X, Y, Z)
    axes_image = plotter.add_plot_range_2d(X, Y, zz_interpolated, "Interpoliertes 2D-Höhenprofil")

    # plotter.add_plot_range_scatter(positions, ranges)

    # show colorbar
    plt.colorbar(axes_image)

    # Show the figure
    plt.show()


class Crazyflie(CrazyflieExternController):
    """
    A class to control the Crazyflie drone and plot its movement data.

    Attributes:
        positions (list of list of float): List of [x, y, z] positions.
        ranges (list of float): List of range values corresponding to the positions.
    """

    last_time = None

    def __init__(self):
        """
        Initializes the Crazyflie controller and sets the run method.
        """
        super().__init__(self.run)

    positions = []
    ranges = []

    def run(self):
        """
        Main method to control the Crazyflie drone's movement and plot the data.
        """

        height = 2

        self.move_to([0, 0, height])

        # area = np.array([
        #     [0, 0, 1],
        #     [0, 1, 1],
        #     [1, 1, 1],
        #     [1, 0, 1],
        #     [0, 0, 1],
        # ])
        #
        # for pos in area:
        #     self.move_to(pos)

        step_count_x = 50
        step_count_y = 3
        area_len = 3

        # for x in range(0, step_count_x):
        #     if x % 2 == 0:
        #         self.move_to([x * area_len / step_count_x, 0, height], self.save_positions, 0)
        #         self.move_to([x * area_len / step_count_x, area_len, height], self.save_positions, 0)
        #     else:
        #         self.move_to([x * area_len / step_count_x, area_len, height], self.save_positions, 0)
        #         self.move_to([x * area_len / step_count_x, 0, height], self.save_positions, 0)

        # y_range_f = range(0, step_count_x + 1)
        y_range_f = range(0, step_count_y + 1)
        y_range_r = list(reversed(y_range_f))
        y_range_len = len(y_range_f)

        for x in range(0, step_count_x):
            if x % 2 == 0:
                y_range = y_range_f
            else:
                y_range = y_range_r

            for y in y_range:
                self.move_to([x * area_len / step_count_x, y * area_len / (y_range_len - 1), height], self.save_positions, 0)

        plot_range(area_len, self.positions, self.ranges, step_count_x)

        self.move_to([0, 0, height])
        self.move_to([0, 0, 0])
        exit()

    def save_positions(self, delta_time, current_pos):
        """
        Callback method to save the current position and range data.

        Args:
            :param delta_time: (float) The time difference since the last position was saved.
            :param current_pos: The current [x: float, y: float, z: float] position of the drone.

        Returns:
            bool: True if the position was saved, False otherwise.
        """
        # if delta_time > .01:
        # print(delta_time, list(map(lambda x: round(x, 2), current_pos)))
        self.positions.append(current_pos)
        self.ranges.append(current_pos[2] * 1000 - self.getRange())
        return True
        # return False

    def move_to(self, pos, callback=None, callback_time=None):
        """
        Moves the Crazyflie drone to the specified position.

        Args:
            :param pos: The target [x: float, y: float, z: float] position.
            :param callback: (optional) A callback function to be called during the movement.
            :param callback_time: (optional) The time interval between callback calls. (if None, callback is called when the position is reached)
        """
        self.setTarget(list(pos))
        moving = True
        self.last_time = self.last_time or self.getTime()
        while moving:
            current_pos = self.getPosition()
            current_time = self.getTime()

            delta_time = current_time - self.last_time
            if callback is not None and callback_time is not None:
                if delta_time > callback_time:
                    callback(delta_time, current_pos)
                    self.last_time = current_time

            if (abs(pos[0] - current_pos[0]) < .1) and (abs(pos[1] - current_pos[1]) < .1) and (
                    abs(pos[2] - current_pos[2]) < .1):
                moving = False
                print("arrived: ", current_pos)
                if callback is not None and callback_time is None:
                    callback(delta_time, current_pos)


class Plotter:
    def __init__(self, nrows: int, ncols: int):
        self.fig = plt.figure()
        self.nrows = nrows
        self.ncols = ncols
        self.sub_plot_index = 0

    def add_subplot(self, index: int = None, is3d: bool = False) -> Axes:
        """
        Add a subplot to the figure.

        :param index: The position of the subplot.
        :param is3d: True if the subplot should be a 3D plot, False otherwise.
        :return: The created subplot-Axes.
        """
        self.sub_plot_index += 1
        # index is sub_plot_index if index is None or < 1
        self.sub_plot_index = index if index is not None and index > 0 else self.sub_plot_index
        return self.fig.add_subplot(self.nrows, self.ncols, self.sub_plot_index, projection='3d' if is3d else None)

    def add_plot_range_3d(self, xx: np.ndarray[Any, np.dtype], yy: np.ndarray[Any, np.dtype],
                          zz: np.ndarray[Any, np.dtype], title: str = "3D-Höhenprofil") -> Poly3DCollection:
        """
        Add a 3D plot to the given axis-position.

        :param xx: The x values of the 3D data.
        :param yy: The y values of the 3D data.
        :param zz: The z values of the 3D data.
        :param title: The title of the plot.
        :return: Poly3DCollection object.
        """

        # Create a subplot.
        ax = self.add_subplot(None, is3d=True)

        # Set z-axis limits
        # ax.set_zlim(0, 1)

        # Set labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        # Create 3D plot
        return ax.plot_surface(xx, yy, zz, cmap='viridis', edgecolor='k')

    def add_plot_range_2d(self, xx: np.ndarray[Any, np.dtype], yy: np.ndarray[Any, np.dtype], zz: np.ndarray[Any, np.dtype], title: str = "2D-Höhenprofil") -> AxesImage:
        """
        Add a 2D plot to the given axis.

        :param pos: The position of the subplot. (numOfRows, numOfCols)
        :param zz: The 2D data to plot.
        :param title: The title of the plot.
        :return: AxesImage object.
        """

        # Create a subplot.
        ax = self.add_subplot()

        # Set labels and title
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(title)

        # Create 2D plot
        extent = [np.min(xx), np.max(xx), np.min(yy), np.max(yy)]
        return ax.imshow(zz, cmap='viridis', origin='lower', extent=extent)

    def add_plot_range_scatter(self, positions: Iterable, ranges: Iterable,
                               title: str = "Scatter-2D-Höhenprofil") -> PathCollection:
        """
        Plots a scatter plot of positions with varying sizes and colors based on ranges.

        Args:
            :param pos: The position of the subplot. (numOfRows, numOfCols)
            :param positions: List of [x: float, y: float] positions.
            :param ranges: List of range values (float) corresponding to the positions.
            :param title: The title of the plot.

            :return: PathCollection object.
        """

        # Create a subplot.
        ax = self.add_subplot()
        ax.set_title(title)

        # Extract x and y positions and calculate sizes and colors for the scatter plot.
        x_positions = [row[0] for row in positions]
        y_positions = [row[1] for row in positions]
        sizes = list(map(lambda range1: range1 / 10, ranges))
        colors = list(map(lambda range1: range1 * 100, ranges))

        # Plot some data on the Axes.
        return ax.scatter(x_positions, y_positions, s=sizes, c=colors, cmap='viridis')


if __name__ == "__main__":
    cf = Crazyflie()
