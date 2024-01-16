import re
import pandas as pd
from io import StringIO
from utils_click import PageClick_GA as ga_click
from utils_click import PageClick_Adobe as adobe_click

def clean_key(key):
    return ''.join(c for c in key if c.isalnum())

class GA4_params_tester_click():

    @staticmethod
    def ga4_params_click(combined_list):
        result_data_list = []

        for entry in combined_list:
            url_dict = {}
            
            for url_key, url_value in entry.items():
                url_dict[url_key] = {k: v for k, v in url_value.items() if k != 'xpath_list'}
                xpath_list = url_value.get('xpath_list')

                if re.search(r'formula', url_key, re.IGNORECASE):
                    script_function = ga_click.selenium_formula_script
                elif re.search(r'eephone', url_key, re.IGNORECASE):
                    script_function = ga_click.selenium_ee_script
                elif re.search(r'honda', url_key, re.IGNORECASE):
                    script_function = ga_click.selenium_honda_script
                else:
                    print(f"No specific script found for {url_key}. Skipping this URL.")
                    continue

                params_list = script_function(url_key, xpath_list)

                for url_key, inner_dict in url_dict.items():
                    inner_dict_values_lower = {k: v.lower() for k, v in inner_dict.items()}

                    best_match_dict = None
                    best_match_count = 0

                    for params_dict in params_list:
                        params_dict_values_lower = {k: v.lower() for k, v in params_dict.items()}

                        match_count = sum(value == params_dict_values_lower.get(key) for key, value in inner_dict_values_lower.items())
                        
                        if match_count > best_match_count:
                            best_match_dict = params_dict.copy() 
                            best_match_count = match_count

                    print(f"For URL: {url_key}")
                    print("Best Match:")
                    print(best_match_dict)

                    result_data = {
                        'URL': url_key,
                        'Params': {key: key for key in inner_dict_values_lower.keys()},
                        'Expected': inner_dict,
                        'Actual': {},
                        'Test Result': {}
                    }

                    for key, expected_value in inner_dict_values_lower.items():
                        key_lower = clean_key(key.lower())

                        if any(clean_key(k.lower()) == key_lower for k in best_match_dict):

                            actual_value = next((v for k, v in best_match_dict.items() if clean_key(k.lower()) == key_lower), None)

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
                                result_data['Test Result'][key] = 'Fail'
                            else:
                                result_data['Test Result'][key] = 'Parameter not found'

                        result_data['Actual'][key] = actual_value

                    result_data_list.append(result_data)

        return result_data_list
    
class Adobe_params_test_click():

    def adobe_params_click(combined_list):
        result_data_list = []

        for entry in combined_list:
            url_dict = {}
            
            for url_key, url_value in entry.items():
                url_dict[url_key] = {k: v for k, v in url_value.items() if k != 'xpath_list'}
                xpath_list = url_value.get('xpath_list')

                params_list = adobe_click.selenium_goodyear_script(url_key, xpath_list)

                for url_key, inner_dict in url_dict.items():
                    inner_dict_values_lower = {k: v.lower() for k, v in inner_dict.items()}

                    best_match_dict = None
                    best_match_count = 0

                    for params_dict in params_list:
                        params_dict_values_lower = {k: v.lower() if isinstance(v, str) else v for k, v in params_dict.items()}

                        match_count = sum(value == params_dict_values_lower.get(key) for key, value in inner_dict_values_lower.items())
                        
                        if match_count > best_match_count:
                            best_match_dict = params_dict.copy() 
                            best_match_count = match_count

                    print(f"For URL: {url_key}")
                    print("Best Match:")
                    print(best_match_dict)

                    result_data = {
                        'URL': url_key,
                        'Params': {key: key for key in inner_dict_values_lower.keys()},
                        'Expected': inner_dict,
                        'Actual': {},
                        'Test Result': {}
                    }

                    for key, expected_value in inner_dict_values_lower.items():
                        key_lower = clean_key(key.lower())

                        if any(clean_key(k.lower()) == key_lower for k in best_match_dict):

                            actual_value = next((v for k, v in best_match_dict.items() if clean_key(k.lower()) == key_lower), None)

                            expected_value = str(expected_value)
                            actual_value = str(actual_value)

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
                                result_data['Test Result'][key] = 'Fail'
                            else:
                                result_data['Test Result'][key] = 'Parameter not found'

                        result_data['Actual'][key] = actual_value

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
