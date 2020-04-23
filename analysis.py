#!/usr/bin/env python3


# ME499-S20 Python Lab 2 Problem 1
# Programmer: Jacob Gray
# Last Edit: 4/21/2020


import csv


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