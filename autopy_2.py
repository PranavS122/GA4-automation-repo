import re
from io import StringIO
from utils import PageSelector
import pandas as pd


def ga4_params_comparison(url_dict, max_retries=6):
    result_data_list = []

    for url, inner_dict in url_dict.items():

        retry_count = 0
        params_dict = None

        while retry_count < max_retries:
            if re.search(r'.*honda.*', url, re.IGNORECASE):
                params_dict = PageSelector.selenium_honda_script(url)
            elif re.search(r'.*formula1.*', url, re.IGNORECASE):
                params_dict = PageSelector.selenium_formula_script(url)
            elif re.search(r'.*eephonesmart.*', url, re.IGNORECASE):
                params_dict = PageSelector.selenium_ee_script(url)
            else:
                return None

            if params_dict:
                break
            else:
                retry_count += 1
                print(f"Retrying {url} - Attempt {retry_count}")

        if not params_dict:
            print(f"Failed to obtain params_dict for {url}. Skipping this URL.")
            continue

        result_data = {'URL': '', 'Params': {}, 'Expected': {}, 'Actual': {}, 'Test Result': {}}
        result_data['URL'] = url
        result_data['Params'] = {}
        result_data['Expected'] = inner_dict
        result_data['Actual'] = {}
        result_data['Test Result'] = {}

        for key, expected_value in inner_dict.items():
            for params_inner_dict in params_dict.values():
                if key in params_inner_dict:
                    actual_value = params_inner_dict[key]

                    if expected_value == '' and actual_value != '':
                        result_data['Test Result'][key] = 'Fail'
                    elif expected_value == '' and actual_value == '':
                        result_data['Test Result'][key] = 'Parameter not found in input and website'
                    elif expected_value.lower() == actual_value.lower():
                        result_data['Test Result'][key] = 'Pass'
                    else:
                        result_data['Test Result'][key] = 'Fail'
                else:
                    actual_value = ''

                    if expected_value == '':
                        result_data['Test Result'][key] = "Fail"
                    else:
                        result_data['Test Result'][key] = 'Parameter not found'

                result_data['Actual'][key] = actual_value

        result_data['Params'] = {key: key for key in result_data['Expected'].keys()}
        result_data_list.append(result_data)

    return result_data_list


def text_conv(result_data_list):
    formatted_data = ""

    for entry in result_data_list:

        formatted_data += f"URL\t{entry['URL']}\n"

        for section, values in entry.items():
            if section != 'URL':
                formatted_data += f"{section}\t"

                formatted_data += "\t".join(
                    [f'"{value}"' if value == "" else str(value) for value in values.values()]) + "\n"

        formatted_data += "\n"

    print("Conversion of Test results to excel started")

    return formatted_data


def data_conv(formatted_data):
    lines = formatted_data.strip().split('\n')
    max_tabs = max(line.count('\t') for line in lines)
    formatted_lines = [line + '\t' * (max_tabs - line.count('\t')) for line in lines]
    df = pd.read_csv(StringIO('\n'.join(formatted_lines)), sep='\t', header=None)
    df = df.fillna("")
    return df
