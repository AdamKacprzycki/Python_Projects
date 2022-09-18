def download_get_diff(month: int, year: int, download_path: str, merge_path: str):
    """ Function download missing zip files and determinate files that should be concat together """

    import zipdownloader as zipdl
    import choosezip as czip
    from os import listdir
    from os.path import isfile, join

    # Get file name from given directory (Which files do we have before download:

    file_name = [file_name for file_name in listdir(merge_path)
                 if isfile(join(merge_path, file_name))
                 and '.csv' in file_name]

    file_to_download_current = czip.file_to_download(month, year, merge_path)

    # Downloading of all necessary zip files:
    for file in sorted(file_to_download_current):
        if len(file) == 7:
            zipdl.download(file[:2], file[3:], download_path, merge_path)
        else:
            zipdl.download(file[:3], file[4:], download_path, merge_path)

    # Determinate all file names after download:
    file_name_after_download = [file_name for file_name in listdir(merge_path)
                                if isfile(join(merge_path, file_name))
                                and '.csv' in file_name]

    # Difference between previous files names and dowloaded files:
    file_diff = set(file_name_after_download) - set(file_name)

    #TODO: In general it would be better if file_diff will be determinated on os.path.getime or similar [manual_mode];

    return file_diff
