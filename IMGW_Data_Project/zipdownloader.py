def download(month: int, year: int, download_path: str, merge_path: str) -> object:

    """Basic function to download a zip file in manual mode or used in other user's functions:"""

    # import necessary utilities:
    import requests
    import zipfile
    import logging
    import datetostr as dstr
    from io import BytesIO
    from pathlib import Path

    """
    Into -> initial parameter's type conversion for function purposes: 
    zip's URL is defined as str, thus there is needed conversion of function initial parameters, 
    especially for len(month) == 1; e.g. initial func parameter -> month = 9 -> datetostr.datestr(9) 
    -> conversion to: '09" as str;
    """

    # Adjusting the initial parameter of a function to be able to use it to create the correct URL:
    month = dstr.datestr(month)
    year = str(year)

    # Defining the zip file URL:
    url = f'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/synop/' \
          f'{year}/{year}_{month}_s.zip'

    try:
        # Downloading the file by sending the request to the URL
        req = requests.get(url)

        # extracting the zip file contents
        zipfile = zipfile.ZipFile(BytesIO(req.content))
        zipfile.extractall(download_path)

    except zipfile.BadZipFile as bfile:
        print(f'Zip file {year}_{month}_s.zip probably does not exist!; error_1 --> {bfile}')

    except Exception as e:
        logging.exception(e)

    else:
        # moving file to other directory:
        Path(f'{download_path}/s_d_{month}_{year}.csv').rename(f'{merge_path}/s_d_{month}_{year}.csv')

        # if zip file was downloaded successfully print information below:
        print(f'Downloading file {year}_{month}_s.zip --> completed')
