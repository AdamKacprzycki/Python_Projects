def datestr(month: int) -> str:

    """
    These function converts initial parameter from int to str with max len == 2 .
    It is needed for defining proper URL (str) to download zip.
    URL contain month expressed as len == 2 str, e.g. month: January is expressed as '01'.

    https://danepubliczne.imgw.pl/.../{year}/{year}_{month}_s.zip.
    """

    if len(str(month)) <= 1:
        return str(f'0{month}')
    else:
        return str(month)
