def get_file_list(num_files):
    """
    formats number of files in olympus format
    :param num_files:
    :return: list of file numbers
    """
    file_list = []
    for num in range(1, num_files+1):
        num = str(num)
        to_add = 4-len(num)
        final = '0'*to_add+num
        file_list.append(final)

    return file_list


def make_macro_3_channels(data_dir, save_dir, file_name_prefix, file_nums, macro_save_dir):
    """

    :param data_dir: directory with .oir files
    :param save_dir: directory where .tif files will be saved
    :param file_name_prefix: common component of name of .oir files from experiment
           ex: "8-10-2018 exp 2 attempt 1 phase 1_A01_G001_"
    :param file_nums: output of get_file_list
    :param macro_save_dir: full path of location for macro to save
    :return: saves a macro file
    """

    file_object = open(macro_save_dir+"oir_macro.ijm", "w")

    inp = 'input="{}";'.format(data_dir)

    bio_import = 'run("Bio-Formats Importer", "open=["+ input + filename +"] view=Hyperstack split_channels stack_order=XYCZT");'
    run = 'run("Z Project...", "projection=[Max Intensity]");'
    close = 'close();'

    for file_num in file_nums:
        filename = 'filename="{}{}.oir"'.format(file_name_prefix, file_num)
        two = 'selectWindow("{}{}.oir - C=0");'.format(file_name_prefix, file_num)
        four = 'saveAs("Tiff", "{}MAX_{}{}.oir - C=0.tif");'.format(save_dir, file_name_prefix, file_num)
        two_1 = 'selectWindow("{}{}.oir - C=1");'.format(file_name_prefix, file_num)
        four_1 = 'saveAs("Tiff", "{}MAX_{}{}.oir - C=1.tif");'.format(save_dir, file_name_prefix, file_num)
        two_2 = 'selectWindow("{}{}.oir - C=2");'.format(file_name_prefix, file_num)
        four_2 = 'saveAs("Tiff", "{}MAX_{}{}.oir - C=2.tif");'.format(save_dir, file_name_prefix, file_num)

        command = inp+"\n"+filename+"\n"+bio_import+"\n"+two+"\n"+run+"\n"+four+"\n"+close+"\n"+close+"\n"+ \
                  two_1+"\n"+run+"\n"+four_1+"\n"+close+"\n"+close+"\n"+ \
                  two_2+"\n"+run+"\n"+four_2+"\n"+close+"\n"+close

        file_object.write(command+"\n")

    file_object.close()
