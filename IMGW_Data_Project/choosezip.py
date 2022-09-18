def file_to_download(month: int, year: int, merge_path: str):
    """
    File detector function - these function determinate all zip file that are needed
    """

    # import necessary utilities:
    import datetostr as dstr
    from os import listdir
    from os.path import isfile, join

    # PREPARATION PART

    # Get file name from given directory to determine which files are existed (what do we have right now):

    file_name = [file_name for file_name in listdir(merge_path)
                 if isfile(join(merge_path, file_name))
                 and '.csv' in file_name]

    # Get file name {month/package}{year} and convert into set for later use:
    file_exist_set = set(i[4:11] if len(i) <= 15 else i[4:12] for i in file_name)

    # Full version of function use collection of cities + key:
    city = {155: 'GDA',
            560: 'KAT',
            566: 'KRK',
            330: 'POZ',
            375: 'WAR',
            424: 'WRO'}

    # FUNCTION INTRO - USER INPUT

    prev_year_check = input("Would you like to check zip files for previous year? [y/n]")

    if prev_year_check == "n":

        # VERSION_1  ->> to determine files from previous months of the current year that should be downloaded;

        if len(file_exist_set) <= 1:
            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_to_download_current = file_all_needed_set_current - file_exist_set

        else:
            file_all_needed_set_current = set(f'{dstr.datestr(x)}_{year}' for x in range(1, month + 1))
            file_to_download_current = file_all_needed_set_current - file_exist_set

    else:

        # VERSION_2 ->> to determine the files that must be downloaded before a given date;

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

    return file_to_download_current
