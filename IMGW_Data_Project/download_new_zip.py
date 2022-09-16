def download_new_zip(month: int, year: int, download_path: str, merge_path: str):

    """
    File detector function - function determinate all zip file that are needed
    """

    # import necessary utilities:
    import urlzip
    import datetostr as dstr
    from os import listdir
    from os.path import isfile, join

    # PREPARATION PART

    # Get file name from given directory:
    global file_name
    file_name = [file_name for file_name in listdir(merge_path)
                 if isfile(join(merge_path, file_name))
                 and '.csv' in file_name]

    # Seting variable as global and saving results for later use --> purpose: merging file:
    file_exist_set = set(i[4:11] if len(i) <= 15 else i[4:12] for i in file_name)

    # Full version of function use colection of cities + key:
    city = {155: 'GDA',
            560: 'KAT',
            566: 'KRK',
            330: 'POZ',
            375: 'WAR',
            424: 'WRO'}

    ############# Beggining part #####################

    prev_year_check = input("Would you like to check zip files for previous year? [y/n]")

    if prev_year_check == "n":

        ################ VERSION_1 only previous month within current year ##################

        if len(file_exist_set) <= 1:
            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_to_download_current = file_all_needed_set_current - file_exist_set

        else:
            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_to_download_current = file_all_needed_set_current - file_exist_set

        # Downloading of all necessery zip files:
        for file in sorted(file_to_download_current):
            urlzip.downloadzip(file[:2], file[3:], download_path, merge_path)

    else:

        ############### VERSION_2 for all previous zips before seted date ################################

        how_many_years = int(input("How many previous years would you like to analyze? [int value]?"))

        year_to_analyse = [year for year in range(year - how_many_years, year)]
        city_keys_list = [keys for keys in city.keys()]
        file_year_permutation = set([f'{y}_{x}' for x in year_to_analyse for y in city_keys_list])

        if len(file_exist_set) <= 1:

            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_all_needed_set_current = file_all_needed_set_current.union(file_year_permutation)
            file_to_download_current = file_all_needed_set_current - file_exist_set

        else:
            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_all_needed_set_current = file_all_needed_set_current.union(file_year_permutation)
            file_to_download_current = file_all_needed_set_current - file_exist_set

        # Downloading of all necessery zip files:
        for file in sorted(file_to_download_current):
            if len(file) == 7:
                urlzip.downloadzip(file[:2], file[3:], download_path, merge_path)
            else:
                urlzip.downloadzip(file[:3], file[4:], download_path, merge_path)

    global file_name_after_download
    file_name_after_download = [file_name for file_name in listdir(merge_path) if
                                isfile(join(merge_path, file_name)) and '.csv' in file_name]

    global file_downloaded_set
    file_downloaded_set = set(i[4:11] if len(i) <= 15 else i[4:12] for i in file_name_after_download)
