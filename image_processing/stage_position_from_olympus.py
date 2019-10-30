import re
import pandas as pd


def get_setup_parameters(matl_file):
    """

    :param matl_file: full path to output from olympus run (matl.omp2info)
    :return: dictionary with parameters from run
    """

    results = dict()

    file = open(matl_file, "r")

    for line in file.readlines():

        if 'matl:overlap' in line:
            results['overlap'] = int(re.search('<matl:overlap>(.*)</matl:overlap>', line).group(1))

        if 'marker:coordinates' in line:
            results['x_origin'] = int(line.split('"')[5])
            results['y_origin'] = int(line.split('"')[7])

        if '<matl:areaWidth>' in line:
            results['x_step'] = int(re.search('<matl:areaWidth>(.*)</matl:areaWidth>', line).group(1))

        if '<matl:areaHeight>' in line:
            results['y_step'] = int(re.search('<matl:areaHeight>(.*)</matl:areaHeight>', line).group(1))

    return results


def get_image_name_and_steps(matl_file):
    """

    :param matl_file: full path to output from olympus run (matl.omp2info)
    :return: dataframe with x and y step listed for each file (+1 to remove 0-based indexing)
    """

    rows = []

    with open(matl_file) as file:
        for line in file:
            if 'matl:image' in line:
                filename = re.search('<matl:image>(.*)</matl:image>', line).group(1)
                nextline = next(file)
                x_step = int(re.search('<matl:xIndex>(.*)</matl:xIndex>', nextline).group(1))+1
                nextline = next(file)
                y_step = int(re.search('<matl:yIndex>(.*)</matl:yIndex>', nextline).group(1))+1

                row = [filename, str(x_step), str(y_step)]

                rows.append(row)

    all_steps = pd.DataFrame(rows)
    all_steps.columns = ['filename', 'x_step', 'y_step']
    all_steps.set_index('filename', inplace=True)

    return all_steps


def calculate_position(step_number, overlap, image_size=2048, resolution_factor=0.6215):
    """

    :param step_number: 1-based step (x or y)
    :param resolution_factor: of images (default is 0.6125)
    :param overlap: percent overlap (whole number)
    :param image_size: resolution of image
    :return: absolute position given a step
    """

    offset_fraction = (100 - overlap/2)/100

    micron_step = image_size*offset_fraction*resolution_factor

    absolute_pos = float(step_number)*float(micron_step)

    return absolute_pos


def master(matl_file, filename_to_save=None, image_size=2048, resolution_factor=0.6215):
    """

    :param matl_file: full path to output from olympus run (matl.omp2info)
    :param filename_to_save: location to save resulting dataframe as csv
    :param image_size: default is 2048
    :param resolution_factor: default is 0.6125
    :return:
    """
    params_dict = get_setup_parameters(matl_file)
    all_steps = get_image_name_and_steps(matl_file)
    all_steps['x_absolute'] = all_steps['x_step'].apply(lambda x: calculate_position(x, params_dict['overlap'], image_size=image_size, resolution_factor=resolution_factor))
    all_steps['y_absolute'] = all_steps['y_step'].apply(lambda x: calculate_position(x, params_dict['overlap'], image_size=image_size, resolution_factor=resolution_factor))

    if filename_to_save is not None:
        all_steps.to_csv(filename_to_save)

    return all_steps
