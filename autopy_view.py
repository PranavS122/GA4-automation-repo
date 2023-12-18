from io import StringIO

import pandas as pd

from utils_view import PageSelector
import re

def preprocess(df):
    try:
        df = df.fillna("")
        url_dict = df.set_index('URL').to_dict(orient='index')
        return url_dict
    except Exception as e:
        print(f"Error: {e}")
        return None


def ga4_params_view(url_dict, max_retries=6):
    result_data_list = []

    for url, inner_dict in url_dict.items():

        retry_count = 0
        params_dict = None

        # Determine which script to run based on the URL
        if re.search(r'formula', url, re.IGNORECASE):
            script_function = PageSelector.selenium_formula_script
        elif re.search(r'ee', url, re.IGNORECASE):
            script_function = PageSelector.selenium_ee_script
        elif re.search(r'honda', url, re.IGNORECASE):
            script_function = PageSelector.selenium_honda_script
        else:
            print(f"No specific script found for {url}. Skipping this URL.")
            continue

        while retry_count < max_retries:
            params_dict = script_function(url)

            if params_dict:
                break
            else:
                retry_count += 1
                print(f"Retrying {url} - Attempt {retry_count}")

        if not params_dict:
            print(f"Failed to obtain params_dict for {url}. Skipping this URL.")
            continue

        best_match_dict = None
        best_match_count = 0

        result_data = {'URL': '', 'Params': {}, 'Expected': {}, 'Actual': {}, 'Test Result': {}}
        result_data['URL'] = url
        result_data['Params'] = {}
        result_data['Expected'] = inner_dict
        result_data['Actual'] = {}
        result_data['Test Result'] = {}

        for idx, params_inner_dict in params_dict.items():
            match_count = sum(1 for key, expected_value in inner_dict.items() if
                              key in params_inner_dict and expected_value.lower() == params_inner_dict[key].lower())

            if match_count > best_match_count:
                best_match_dict = params_inner_dict
                best_match_count = match_count

        for key, expected_value in inner_dict.items():
            if key in best_match_dict:
                actual_value = best_match_dict[key]

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
