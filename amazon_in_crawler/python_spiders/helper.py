import re
from datetime import datetime

def string_found(_word_list, _description):
    _description = _description.lower()
    for _word in _word_list:
        if re.search(r"\b" + re.escape(_word.lower()) + r"\b", _description):
            return True
    return False

def remove_white_spaces(input_string):
    """
    Removes continuous spaces in the input string
    :param input_string:
    """
    return re.sub(r'\s+', ' ', input_string).strip()


def remove_unicode_char(input_string):
    """
    This function takes string as an input, and return strings after removing unicode character
    """
    return (''.join([i if ord(i) < 128 else ' ' for i in input_string])).strip()


def is_float(_input):
    try:
        float(_input)
        res = True
    except ValueError:
        res = False
    return res

def convert_to_numeric(_input):
    _output = _input
    if isinstance(_input, int):
        pass
    elif isinstance(_input, float):
        if _input.is_integer():
            _output = int(_input)
    elif isinstance(_input, str):
        if _input.isdigit():
            _output = int(_input)
        if is_float(_input):
            if float(_input) == int(float(_input)):
                _output = int(float(_input))
            else:
                _output = float(_input)
        else:
            _output = None
    else:
        _output = None
    return _output


def format_date(input_string, date_format="%d %B %Y"):
    """[This function convert date from String version to python date object]

    Args:
        input_string ([string]): [String representation of date]
        date_format (str, optional): [Pass date format if default is not the case]. Defaults to "%d/%m/%Y".

    Returns:
        [python date object]: [date]
    """
    try:
        return datetime.strptime(input_string, date_format).strftime("%d-%b-%Y")
    except Exception as e:
        return input_string
    
    