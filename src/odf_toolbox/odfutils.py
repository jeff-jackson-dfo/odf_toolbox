# -*- coding: utf-8 -*-
import datetime
import pandas
import shlex
import re
from icecream import ic

def read_file_lines(file_with_path: str):
    assert isinstance(file_with_path, str), \
        f"Input value is not of type str: {file_with_path}"
    try:
        with open(file_with_path, 'r') as file:
            lines = list(file_line.strip() for file_line in file.readlines())
        return lines
    except FileNotFoundError:
        return f"File not found: {file_with_path}"
    except Exception as e:
        return f"An error occurred while reading the file: {e}"

def find_lines_with_text(odf_file_lines: list, separator: str) -> list:
    assert isinstance(odf_file_lines, list), \
        f"Input value is not of type list: {odf_file_lines}"
    assert isinstance(separator, str), \
        f"Input value is not of type str: {separator}"
    matching_lines = [(text_index, text_line) for text_index, text_line in enumerate(odf_file_lines)
                      if separator in text_line]
    return matching_lines

def split_lines_into_dict(lines: list) -> dict:
    assert isinstance(lines, list), \
        f"Input value is not of type list: {lines}"
    return list_to_dict(lines)

def search_dictionaries(search_text: str, dictionaries: list):
    assert isinstance(search_text, str), \
        f"Input value is not of type str: {search_text}"
    assert isinstance(dictionaries, list), \
        f"Input value is not of type list: {dictionaries}"
    matching_results = []
    for string_index, dictionary in enumerate(dictionaries):
        for key, value in dictionary.items():
            if search_text.lower() in key.lower() or search_text.lower() in value.lower():
                matching_results.append((string_index + 1, dictionary))
    return matching_results

def split_lines_after_data(all_data_lines: list) -> pandas.DataFrame:
    assert isinstance(all_data_lines, list), \
        f"Input value is not of type list: {all_data_lines}"
    result_lines = []
    for data_line in all_data_lines:
        # Split each line by all whitespace characters
        parts = data_line.split()
        result_lines.append(parts)

    # Convert the list of lists to a Pandas DataFrame
    df = pandas.DataFrame(result_lines)

    return df

def get_current_date_time() -> str:
    dt = datetime.datetime.now()
    dts = dt.strftime("%d-%b-%Y %H:%M:%S.%f").upper()
    return f"'{dts[:-4]}'"

def check_value(value):
    value_type = type(value)
    if value_type == str:  
        check_string(value)
    elif value_type == int:
        check_int(value)
    elif value_type == float:
        check_float(value)

def check_float(value: float) -> float:
    if value is None:
        value = -99.0
    assert isinstance(value, float), \
        f"Input value is not of type float: {value}"
    return value

def check_int(value: int) -> int:
    if value is None:
        value = -99
    assert isinstance(value, int), \
        f"Input value is not of type int: {value}"
    return value

def check_long(value: float) -> float:
    if value is None:
        value = -999.0
    return value

def check_datetime(value: str) -> str:
    assert isinstance(value, str), \
        f"Input value is not of type str: {value}"
    if value is None:
        value = "'17-NOV-1858 00:00:00.00'"
    else:
        sytm_format = "%d-%b-%Y %H:%M:%S.%f"

        # checking if format matches the date
        res = True

        # using try-except to check for truth value
        try:
            res = bool(datetime.datetime.strptime(value, sytm_format))
        except ValueError:
            res = False

    return value

def check_string(value: str) -> str:
    assert isinstance(value, str), \
        f"Input value is not of type str: {value}"
    value = check_datetime(value)
    # Check if this string value is actually an exponential number that uses the old unsupported exponent "D".
    # If it does then replace it with an "E".
    if re.search(r'[0-9]*.[0-9]*D[+-][0-9]*', value):
        value = re.sub('D', 'E', value)
    if value is None:
        value = ''
    if not value:
        value = ''
    return value

def list_to_dict(lst: list) -> dict:
    assert isinstance(lst, list), \
        f"Input value is not of type list: {lst}"
    # Using a dictionary comprehension to create key-value pairs from alternating elements in the list
    result_dict = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return result_dict

def remove_leading_whitespace(lst: list):
    assert isinstance(lst, list), \
        f"Input value is not of type list: {lst}"
    # Using list comprehension to remove trailing commas and whitespace from each item
    cleaned_list = [item.rstrip(', ').strip() for item in lst]
    return cleaned_list

def remove_trailing_commas_and_whitespace(lst: list):
    assert isinstance(lst, list), \
        f"Input value is not of type list: {lst}"
    # Using list comprehension to remove trailing commas and whitespace from each item
    cleaned_list = [item.rstrip(', ').strip() for item in lst]
    return cleaned_list

def split_string_with_quotes(input_string: str):
    assert isinstance(input_string, str), \
        f"Input value is not of type str: {input_string}"
    # Using shlex.split to split the string by whitespace except when between double quotes
    result_list = shlex.split(input_string)
    return result_list

def convert_to_float(item):
    try:
        # Attempt to convert the item to float
        return float(item)
    except (ValueError, TypeError):
        # Return the original item if conversion is not possible
        return item

def convert_dataframe(df: pandas.DataFrame) -> pandas.DataFrame:
    assert isinstance(df, pandas.DataFrame), f"Input value is not of type pandas.DataFrame: {df}"
    # Apply the conversion function to each element in the DataFrame
    df = df.map(convert_to_float)
    return df

def add_commas_except_last(lines: str) -> str:
    assert isinstance(lines, str), f"Input value is not of type str: {lines}"
    lines_with_commas = lines.replace("\n", ",\n")
    lines_with_commas = lines_with_commas.rstrip(",\n")
    lines_with_commas = lines_with_commas + "\n"
    return lines_with_commas

def add_commas(lines: str) -> str:
    assert isinstance(lines, str), f"Input value is not of type str: {lines}"
    lines_with_commas = lines.replace("\n", ",\n")
    lines_with_commas = lines_with_commas.replace("' ,", "',")
    return lines_with_commas


if __name__ == "__main__":

    # ret = check_datetime('23-MAY-2010 16:00:02.88')
    # print(ret)

    # check_value(None)
    # check_value(57.5)
    # check_value(100)
    # check_value('Nice melons!')

    coef = '0.60000000D+01'
    coef = check_string(coef)
    new_coef = check_float(float(coef))
    ic(new_coef)
    
    # text_lines = "This is line 1\nThis is line\nThis is the last line\n"
    # print(text_lines)
    # print(type(text_lines))
    # formatted_text = add_commas_except_last(text_lines)
    # print(formatted_text)
    # print(type(formatted_text))

    # file_path = input("Enter the file path: ")
    # file_path = 'C:/DEV/pythonProjects/odfClass/test-files/XBT_HUD2005016_58_1_016.ODF'
    # file_path = '../../test-files/MADCP_HUD2016027_1999_3469-31_3600.ODF'
    # file_lines = read_file_lines(file_path)

    # text_to_find = "_HEADER"
    # text_to_find = "-- DATA --"
    # header_lines_with_indices = find_lines_with_text(file_lines, text_to_find)
    # data_line_start = None
    # for index, line in header_lines_with_indices:
    #     data_line_start = index + 1

    # Separate the header and data lines
    # header_lines = file_lines[:data_line_start - 1]
    # data_lines = file_lines[data_line_start:]

    # lines_after_data_df = split_lines_after_data(data_lines)

    # print("\nDataFrame with lines after '--DATA--' split by whitespace:")
    # print(lines_after_data_df)
