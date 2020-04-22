#!/usr/bin/env python3


# ME499-S20 Python Lab 2 Problem 1
# Programmer: Jacob Gray
# Last Edit: 4/21/2020


def load_data_from_file():
    """
    Takes a file path as a string and returns two lists: One list contains all the time indexes and the second
    list contains all the values as python floats.
    :return:
    """


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

