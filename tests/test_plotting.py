import numpy as np
import pytest

from fancy_matplotlib.chart_templates import (
    LineChart,
    Histogram,
    SingleBarChart,
    MultipleBarChart,
    InvalidInputException,
)


def test_generating_line_chart():
    x_values = [0, 1, 2, 3, 4]
    y_values = [[10, 30, 70, 100, 150], [20, 40, 80, 120, 30]]
    line_chart = LineChart(
        x_values,
        y_values,
        title='Sample plot',
        x_axis_label='Sample x-axis',
        y_descriptors=['Line 1', 'Line 2'],
    )
    line_chart()


def test_generating_bar_chart():
    x_values = ['A', 'B', 'C', 'D', 'E']
    y_values = [[10, 30, 70, 100, 150], [20, 40, 80, 120, 30]]
    bar_chart = SingleBarChart(
        x_values,
        y_values[0],
        title='Sample plot',
        y_axis_label='Sample y-axis',
        x_axis_label='Sample x-axis',
    )
    bar_chart()


def test_generating_multiple_bar_chart():
    x_values = ['A', 'B', 'C', 'D', 'E']
    y_values = [[10, 30, 70, 100, 150], [20, 40, 80, 120, 30], [10, 30, 70, 100, 150]]
    multiple_bar_chart = MultipleBarChart(
        x_values,
        y_values,
        title='Sample plot',
        x_axis_label='Sample x-axis',
        y_descriptors=['Line 1', 'Line 2', 'Line 3'],
    )
    multiple_bar_chart()


def test_generating_histogram():
    x_values = [np.random.random(1000) * 1000]
    histogram = Histogram(
        x_values,
        diff_x_ticks=100,
        diff_y_ticks=3,
        num_bins=30,
        title='Sample plot',
        x_axis_label='Sample x-axis',
    )
    histogram()


def test_generating_histogram_with_multiple_bars():
    x_values = [np.random.random(1000) * 1000, np.random.random(1000) * 1000]
    histogram = Histogram(
        x_values,
        diff_x_ticks=100,
        diff_y_ticks=5,
        num_bins=30,
        title='Sample plot',
        x_axis_label='Sample x-axis',
    )
    histogram()


def test_generating_single_bar_chart_with_wrong_input():
    with pytest.raises(InvalidInputException):
        x_values = ['A', 'B', 'C', 'D', 'E']
        y_values = [[10, 30, 70, 100, 150], [20, 40, 80, 120, 30]]
        bar_chart = SingleBarChart(
            x_values,
            y_values,
            title='Sample plot',
            y_axis_label='Sample y-axis',
            x_axis_label='Sample x-axis',
        )
        bar_chart()
