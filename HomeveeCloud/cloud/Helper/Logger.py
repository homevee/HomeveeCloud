IS_DEBUG = True

def log(string: str):
    """
    Log the given string to the command line if IS_DEBUG == true
    :param string: the string to log
    :return:
    """
    if IS_DEBUG:
        print(str(string))