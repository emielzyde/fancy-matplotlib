from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np

tableau20 = [
    (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
    (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
    (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
    (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
    (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)
]

for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


class InvalidInputException(Exception):
    """
    Raises when the inputs for the chart do not conform to the requirements
    """


class BasePlot:

    """
    Attributes
    ----------
    x_data
        The data for the x-axis
    converted_x_data
        The converted x data. For line charts, this is just the original data. For bar
        charts (with non-numerical x data), this is the x data converted to numerical
        values.
    y_data
        The data for the y-axis. This can be a single line/bar or multiple lines/bars
    diff_x_ticks
        The gap to leave between ticks on the x axis
    diff_y_ticks
        The gap to leave between ticks on the y axis
    x_axis_label
        The label for the x-axis
    y_axis_label
        The label for the y-axis
    y_descriptors
        The text to include in the legend, describing each individual dataset for the
        y axis
    title
        The title for the chart
    min_x, max_x
        The minimum and maximum values of the x data
    min_y, max_y
        The minimum and maximum values of the y data
    ax
        An axis object
    grid_range
        The range of x-values used for plotting the grid
    """

    def __init__(
        self,
        x_data: Union[List, np.ndarray],
        y_data: Optional[Union[List[list], List[np.ndarray], list, np.ndarray]],
        diff_x_ticks: Optional[int] = 1,
        diff_y_ticks: Optional[int] = 10,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        y_descriptors: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        """
        Initialises the chart class

        Parameters
        ----------
        x_data
            The data for the x-axis
        y_data
            The data for the y-axis. This can be a single line/bar or multiple
            lines/bars
        diff_x_ticks
            The gap to leave between ticks on the x axis
        diff_y_ticks
            The gap to leave between ticks on the y axis
        x_axis_label
            The label for the x-axis
        y_axis_label
            The label for the y-axis
        y_descriptors
            The text to include in the legend, describing each individual dataset for
            the y axis
        title
            The title for the chart
        """
        self.x_data = x_data
        self.converted_x_data = x_data
        self.y_data = y_data
        self.diff_x_ticks = diff_x_ticks
        self.diff_y_ticks = diff_y_ticks
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.y_descriptors = y_descriptors
        self.title = title

        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.ax = None
        self.grid_range = None

    def __call__(self):
        """
        Generates the chart
        """
        self.set_up_chart()
        self.plot()
        self.include_text()
        plt.show()

    def set_up_chart(self):
        """
        Sets up the chart by checking the inputs, removing the spines, getting the
        ticks and the grid
        """
        self.check_inputs()
        self.set_font()
        self.ax = plt.subplot(111)
        self.remove_spines()
        self.get_min_max()
        self.get_ticks()
        self.get_grid_range()
        self.get_grid()

    def check_inputs(self):
        """
        Checks the inputs. If the inputs do not conform to the requirements, an error
        is raised

        Raises
        ------
        InvalidInputException
            When the inputs do not conform to the requirements
        """
        pass

    def plot(self):
        """
        The function that will perform the plotting. This must be implemented in each
        subclass.
        """
        raise NotImplementedError

    @staticmethod
    def set_font():
        """
        Sets the font of the text by over-riding the default font used by Matplotlib
        """
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

    def include_text(self):
        """
        Sets the title, axis labels and the legend
        """
        plt.title(self.title) if self.title else None
        plt.xlabel(self.x_axis_label) if self.x_axis_label else None
        plt.ylabel(self.y_axis_label) if self.y_axis_label else None
        if self.y_descriptors:
            plt.legend(loc=7, frameon=False, bbox_to_anchor=(1.112, 0.5), fontsize=8)
        plt.show()

    def remove_spines(self):
        """
        Removes the spines of the chart
        """
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)

    def get_min_max(self):
        """
        Gets the minimum and maximum x and y values. These are used for generating
        the x and y axis ticks and the grid
        """
        self.min_x = min(self.converted_x_data)
        self.max_x = max(self.converted_x_data)
        if not self.y_data:
            return
        try:
            self.min_y = min(min(y_arr) for y_arr in self.y_data)
            self.max_y = max(max(y_arr) for y_arr in self.y_data)
        except TypeError:
            self.min_y = min(self.y_data)
            self.max_y = max(self.y_data)

    def get_ticks(self):
        """
        Gets the x and y axis ticks
        """
        y_tick_range = range(
            self.min_y,
            self.max_y + self.diff_y_ticks,
            self.diff_y_ticks,
        )
        x_tick_range = range(
            self.min_x,
            self.max_x + self.diff_x_ticks,
            self.diff_x_ticks
        )
        plt.yticks(y_tick_range, [str(x) for x in y_tick_range])
        if isinstance(self.x_data[0], str):
            plt.xticks(x_tick_range, self.x_data)
        else:
            plt.xticks(x_tick_range, [x for x in x_tick_range])

    def get_grid_range(self):
        """
        Gets the range of x values that is used for plotting the grid. This must be
        implemented in each subclass
        """
        raise NotImplementedError

    def get_grid(self):
        """
        Gets the grid for the chart
        """
        for y in range(self.min_y, self.max_y + self.diff_y_ticks, self.diff_y_ticks):
            plt.plot(
                self.grid_range,
                [y] * len(self.grid_range),
                "--",
                lw=0.5,
                color="black",
                alpha=0.3,
            )
