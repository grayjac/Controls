#!/usr/bin/env python3


# ME499-S20 Python Homework 1 Data Analysis
# Programmer: Jacob Gray
# Last Edit: 4/26/2020


import csv
from math import log
from math import pi
from math import e
from math import sqrt


def load_data_from_file(file_name):
    """
    Takes a file path as a string and returns two lists: One list contains all the time indexes and the second
    list contains all the values as python floats.
    :param file_name: The name of the file you want to load.
    :return: Two lists, each containing a data column.
    """

    time = []
    position = []

    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for lines in csv_reader:
            time.append(float(lines[0]))
            position.append(float(lines[1]))

    return time, position


def greater_than_index(numbers_list, comparison_number):
    """
    This function returns the position of the first element in the numbers list which is greater than or equal to the
    number input.
    :param numbers_list: List of floats or integers.
    :param comparison_number: Float or integer.
    :return: Position of first element in numbers list greater than or equal to number input.
    """

    for i in range(len(numbers_list)):
        if numbers_list[i] >= comparison_number:
            index = i
            break
        else:
            index = None

    return index


def c_initial(position_data):
    """
    Takes position data from a second order ODE and returns the initial position of the system.
    :param position_data: Position response data from second order ODE.
    :return: The initial condition.
    """
    return position_data[0]


def c_max(position_data):
    """
    Takes position data from a second order ODE and returns the maximum position value.
    :param position_data: Position response data from second order ODE.
    :return: Maximum position value.
    """
    return max(position_data)


def c_final(position_data):
    """
    Takes position data from a second order ODE and returns the steady state value.
    :param position_data: Position response data from second order ODE.
    :return: Steady state value.
    """
    return position_data[-1]


def T_r(time_data, position_data):
    """
    This function estimates the rise time for a second order ODE response.
    :param time_data: List of time data.
    :param position_data: List of position data.
    :return: Rise time.
    """

    # Returns the index of the value greater than or equal to 90% of the max position value
    upper_index = greater_than_index(position_data, 0.9 * c_max(position_data))

    # Returns the index of the value greater than or equal to 10% of the max position value
    lower_index = greater_than_index(position_data, 0.1 * c_max(position_data))

    return time_data[upper_index] - time_data[lower_index]


def T_p(time_data, position_data):
    """
    Estimates and returns the peak time of a second order ODE.
    :param time_data:  List of time data.
    :param position_data: List of position data.
    :return: Peak time.
    """

    return time_data[position_data.index(max(position_data))]


def perc_overshoot(position_data):
    """
    This estimates and returns the percent overshoot for a second order ODE response.
    :param position_data: List of position data.
    :return: Percent overshoot.
    """
    maximum = c_max(position_data) - position_data[0]
    final = c_final(position_data) - position_data[0]

    return ((maximum - final) / final) * 100


def T_s(time_data, position_data):
    """
    This estimates and returns the 2% settling time from a second order ODE response.
    :param time_data:  List of time data.
    :param position_data: List of position data.
    :return: 2% settling time in seconds.
    """
    rang = 0.02 * (c_final(position_data) - c_initial(position_data))
    lower_bound = c_final(position_data) - rang
    upper_bound = c_final(position_data) + rang

    # Looping through the list in reverse to check for the first value that passes the lower and upper bounds
    for i in range(len(position_data)):
        value = position_data[-1 - i]
        if value < lower_bound or value > upper_bound:
            break
    return time_data[-1 - i]


def get_system_params(perc_overshoot, settling_time):
    """
    Calculates and returns mass, spring, and damper constants for a second order ODE system.
    :param perc_overshoot: Percent overshoot of response.
    :param settling_time: 2% settling time of response.
    :return: Mass, spring, damper constants.
    """
    zeta = -log(perc_overshoot / 100, e) / sqrt(pi ** 2 + (log(perc_overshoot / 100, e)) ** 2)
    omega_n = 4 / (zeta * settling_time)

    return 1, omega_n ** 2, 2 * zeta * omega_n


def analyze_data(file_name, window_size=1):
    """
    This function takes a file name as a string and returns a dictionary with the following values: c_initial, c_max,
    c_final, T_r, T_p, perc_overshoot, T_s, m, k, and c.
    :param file_name: File name as a string.
    :param window_size: Size of the mean window. Positive integer.
    :return: All second order ODE system parameters.
    """

    time_data, unfiltered_position_data = load_data_from_file(file_name)
    position_data = backwards_filter(unfiltered_position_data, window_size)
    mass, spring, damper = get_system_params(perc_overshoot(position_data), T_s(time_data, position_data))

    data_dict = {'c_final': c_final(position_data),
                 'c_initial': c_initial(position_data),
                 'c_max': c_max(position_data),
                 'peak_time': T_p(time_data, position_data),
                 'perc_overshoot': perc_overshoot(position_data),
                 'rise_time': T_r(time_data, position_data),
                 'settling_time': T_s(time_data, position_data),
                 'system_damping': damper,
                 'system_mass': mass,
                 'system_spring': spring}

    return data_dict


def backwards_filter(list_data, window_size=1):
    """
    Takes a list with adjustable window size to apply a backwards mean filter.
    :param list_data: List of integers or booleans.
    :param window_size: Positive integer.
    :return: Backwards mean filtered list. Will return a ValueError if window_size is not a positive integer.
    """

    filtered_data = []

    if window_size < 0 or type(window_size) != int:
        raise ValueError

    for i in range(0, window_size):
        filtered_data.append(sum(list_data[0:i + 1]) / (i + 1))

    for i in range(0, len(list_data) - window_size):
        filtered_data.append(sum(list_data[i + 1:i + 1 + window_size]) / window_size)

    return filtered_data


if __name__ == "__main__":
    data_dict = analyze_data('data1.csv')
    alpha_list = sorted(data_dict.items(), key=lambda x: x[0])
    [print(key, ':', value) for key, value in dict(alpha_list).items()]
