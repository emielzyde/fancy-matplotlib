from typing import List, Optional, Union

import matplotlib.pyplot as plt
import numpy as np

from .plotting_template import BasePlot, tableau20, InvalidInputException

DEFAULT_BAR_WIDTH = 0.8


class LineChart(BasePlot):

    """
    Generates a line chart with one or more individual lines
    """

    def __init__(
        self,
        x_data: Union[List, np.ndarray],
        y_data: Union[List[list], List[np.ndarray]],
        diff_x_ticks: Optional[int] = 1,
        diff_y_ticks: Optional[int] = 10,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        y_descriptors: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        super().__init__(
            x_data,
            y_data,
            diff_x_ticks,
            diff_y_ticks,
            x_axis_label,
            y_axis_label,
            y_descriptors,
            title,
        )

    def get_grid_range(self):
        self.grid_range = np.arange(self.min_x, self.max_x + self.diff_x_ticks)

    def plot(self):
        for index, y_arr in enumerate(self.y_data):
            plt.plot(
                self.x_data,
                y_arr,
                lw=1,
                color=tableau20[index],
                label=self.y_descriptors[index] if self.y_descriptors else None,
            )


class SingleBarChart(BasePlot):

    """
    Generates a bar chart with single bars
    """

    def __init__(
        self,
        x_data: Union[List, np.ndarray],
        y_data: Union[list, np.ndarray],
        diff_x_ticks: Optional[int] = 1,
        diff_y_ticks: Optional[int] = 10,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        y_descriptors: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        super().__init__(
            x_data,
            y_data,
            diff_x_ticks,
            diff_y_ticks,
            x_axis_label,
            y_axis_label,
            y_descriptors,
            title,
        )
        self.converted_x_data = np.arange(0, len(self.x_data))

    def check_inputs(self):
        is_list_of_lists = any(isinstance(sub_list, list) for sub_list in self.y_data)
        is_list_of_arrays = any(
            isinstance(sub_list, np.ndarray)
            for sub_list in self.y_data
        )
        if is_list_of_arrays or is_list_of_lists:
            raise InvalidInputException('This function plots only one bar')

    def get_grid_range(self):
        grid_range = (
            list(np.arange(self.min_x, self.max_x + 1)) +
            [self.min_x - 0.5 * DEFAULT_BAR_WIDTH] +
            [self.max_x + 0.5 * DEFAULT_BAR_WIDTH]
        )
        self.grid_range = sorted(grid_range)

    def plot(self):
        plt.bar(
            self.converted_x_data,
            self.y_data,
            lw=1,
            color=tableau20[0],
            label=self.y_descriptors[0] if self.y_descriptors else None
        )


class MultipleBarChart(BasePlot):

    """
    Generates a bar chart with multiple bars
    """

    def __init__(
        self,
        x_data: Union[List, np.ndarray],
        y_data: Union[List[list], List[np.ndarray]],
        diff_x_ticks: Optional[int] = 1,
        diff_y_ticks: Optional[int] = 10,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        y_descriptors: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        super().__init__(
            x_data,
            y_data,
            diff_x_ticks,
            diff_y_ticks,
            x_axis_label,
            y_axis_label,
            y_descriptors,
            title,
        )
        self.converted_x_data = np.arange(0, len(self.x_data))
        self.bar_width = 0.25 if len(y_data) < 5 else 0.1

    def get_grid_range(self):
        grid_range = (
            list(np.arange(self.min_x, self.max_x + 1)) +
            [self.min_x - self.bar_width * len(self.y_data) / 2] +
            [self.max_x + self.bar_width * len(self.y_data) / 2]
        )
        self.grid_range = sorted(grid_range)

    def plot(self):
        start_step = (
            np.array(self.converted_x_data) -
            self.bar_width * len(self.y_data) / 2
            + 0.5 * self.bar_width
        )
        for index, y_arr in enumerate(self.y_data):
            plt.bar(
                start_step,
                y_arr,
                lw=1,
                width=self.bar_width,
                color=tableau20[index],
                label=self.y_descriptors[index] if self.y_descriptors else None
            )
            start_step += self.bar_width


class Histogram(BasePlot):
    """
    Generates a histogram

    Attributes
    ----------
    num_bins
        The number of bins to use in the histogram
    bins
        The values of the bin edges in the histogram
    """

    def __init__(
        self,
        x_data: Union[List[list], List[np.ndarray], list, np.ndarray],
        num_bins: int,
        diff_x_ticks: Optional[int] = 1,
        diff_y_ticks: Optional[int] = 10,
        x_axis_label: Optional[str] = None,
        y_axis_label: Optional[str] = None,
        y_descriptors: Optional[List[str]] = None,
        title: Optional[str] = None,
    ):
        super().__init__(
            x_data,
            None,
            diff_x_ticks,
            diff_y_ticks,
            x_axis_label,
            y_axis_label,
            y_descriptors,
            title,
        )
        self.num_bins = num_bins
        self.bins = []
        hist_bin_values = []
        for x_array in x_data:
            current_hist_bin_values, bins = np.histogram(
                x_array,
                bins=self.num_bins,
            )
            self.bins += list(bins)
            hist_bin_values += list(current_hist_bin_values)
        self.min_y = 0
        self.max_y = max(hist_bin_values)

    def get_min_max(self):
        pass

    def get_ticks(self):
        y_tick_range = range(
            self.min_y,
            self.max_y + self.diff_y_ticks,
            self.diff_y_ticks,
        )
        x_tick_range = np.arange(
            min(self.bins),
            max(self.bins) + self.diff_x_ticks,
            self.diff_x_ticks,
        )
        plt.yticks(y_tick_range, [str(x) + "%" for x in y_tick_range])
        plt.xticks(x_tick_range, [int(x) for x in x_tick_range])

    def get_grid_range(self):
        self.grid_range = list(np.arange(
            min(self.bins),
            max(self.bins),
            (max(self.bins) - min(self.bins))/len(self.bins)
        ))
        self.grid_range.append(max(self.bins))

    def plot(self):
        plt.hist(
            self.x_data,
            bins=self.num_bins,
            color=[tableau20[i] for i in range(len(self.x_data))],
            edgecolor='black',
            lw=0.5,
        )
