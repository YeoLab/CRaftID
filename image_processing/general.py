import numpy as np


def get_x_and_y_coords(array):
    """
    Import a value from an array and transform into a list of x and y coords
    :param array: 2D array of square coordinates
    :return: list of x and y coordinates to be used for plotting
    """
    x_vals = [array[0][0], array[1][0], array[2][0], array[3][0]]
    y_vals = [array[0][1], array[1][1], array[2][1], array[3][1]]
    coords = [x_vals, y_vals]
    return coords


def make_new_dict_of_squares(squares, keys_to_keep):
    """
    subsets a dictionary with a list of keys to keep
    :param squares: dictionary of squares
    :param keys_to_keep: keys of interest to keep
    :return: new dictionary only containing key:value pairs from keys_to_keep
    """
    clean_squares_dict = dict()

    for index in keys_to_keep:
        keep = squares[index]
        clean_squares_dict[index] = keep

    return clean_squares_dict


def get_x_and_y_coords_for_a_square(square_array):
    """
    For a given array, return x and y coordinates
    :param square_array: array with coordinates of one square (from find_squares)
    :return: x1,y1,x2,y2,x3,y3,x4,y4
    """
    x1 = square_array[0][0]
    y1 = square_array[0][1]
    x2 = square_array[1][0]
    y2 = square_array[1][1]
    x3 = square_array[2][0]
    y3 = square_array[2][1]
    x4 = square_array[3][0]
    y4 = square_array[3][1]

    return x1, y1, x2, y2, x3, y3, x4, y4


def get_min_x_and_y_coordinate_from_all_squares(squares_dict):
    """
    Use this to find overlapping squares
    :param squares_dict:
    :return:
    """
    x_y_dict = dict()

    for item in squares_dict.keys():
        x1, y1, x2, y2, x3, y3, x4, y4 = get_x_and_y_coords_for_a_square(squares_dict[item])
        min_x = min(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)

        x_y_dict[item] = [min_x, min_y]

    return x_y_dict


def make_df_with_square_coords(squares_dict):
    """

    :param squares_dict:dictionary of squares
    :return:dataframe with min_x and min_y information
    """
    test_df = pd.DataFrame(index=squares_dict.keys())
    for square in test_df.index:
        to_plot = gen.get_x_and_y_coords(squares_dict[square])
        test_df.ix[square, 'min_x'] = min(to_plot[0])
        test_df.ix[square, 'min_y'] = min(to_plot[1])
    sorted_df = test_df.sort_values(by=['min_x', 'min_y'])
    return sorted_df


def make_square(min_x, min_y, x_length, y_length):
    """
    format a square properly
    :param min_x: min_x coord
    :param min_y: min_y coord
    :param x_length: x_length of square
    :param y_length: y_length of square
    :return: numpy array of the square
    """
    square = np.array([[min_x, min_y],
             [min_x, min_y + y_length],
             [min_x + x_length, min_y + y_length],
             [min_x + x_length, min_y]])
    return square


def expand_square(square, expansion_distance):
    """
    Expand a square to make sure we don't miss any edges
    :param square: array with square coordinates (from find_squares)
    :param expansion_distance: number of pixels to expand the square in all directions
    :return: numpy array of new square with coordinates
    """
    x1, y1, x2, y2, x3, y3, x4, y4 = get_x_and_y_coords_for_a_square(square)

    min_x = min(x1, x2, x3, x4)
    max_x = max(x1, x2, x3, x4)
    min_y = min(y1, y2, y3, y4)
    max_y = max(y1, y2, y3, y4)

    min_x_new = min_x-expansion_distance
    max_x_new = max_x+expansion_distance

    min_y_new = min_y-expansion_distance
    max_y_new = max_y+expansion_distance

    new_square = np.array([[min_x_new, min_y_new],
                           [min_x_new, max_y_new],
                           [max_x_new, max_y_new],
                           [max_x_new, min_y_new]])
    return new_square

