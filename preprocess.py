import pandas as pd
from utils_click import doubleQuoteDict


class Preprocessor():

    @staticmethod
    def preprocess_click(df):
        df = df.fillna("")
        df.columns = df.columns.str.strip()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        url_list = [url for url in df['URL'].tolist() if isinstance(url, str) and url.strip()]

        url_idx = df.columns.get_loc('URL')
        xpath_idx = df.columns.get_loc('xpath')
        columns_between = df.columns[url_idx + 1:xpath_idx]

        nested_dicts = []

        for _, row in df.iterrows():
            inner_dict = doubleQuoteDict()

            for col in columns_between:
                value = row[col]
                if pd.notna(value):
                    inner_dict[col] = value
            if any(inner_dict.values()):
                nested_dicts.append(inner_dict)

        url_dict = []

        for url, nested_dict in zip(url_list, nested_dicts):
            url_dict.append({url: nested_dict})

        xpath_list = []
        current_list = []
        for xpath in df['xpath']:
            if xpath == "":
                if current_list:
                    xpath_list.append(current_list)
                    current_list = []
            else:
                current_list.append(xpath)

        if current_list:
            xpath_list.append(current_list)

        combined_list = []
        for url_entry, xpath_entry in zip(url_dict, xpath_list):
            for url_key, url_value in url_entry.items():
                url_value['xpath_list'] = xpath_entry
                combined_list.append({url_key: url_value})

        return combined_list
    
    def preprocess_view(df):

        try:
            df = df.fillna("")
            df.columns = df.columns.str.strip()
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            url_list = [url for url in df['URL'].tolist() if isinstance(url, str) and url.strip()]
            param_colums = df.columns[df.columns != "URL"]

            url_dict_list = []
            params_list = []

            for _, row in df.iterrows():
                inner_dict = doubleQuoteDict()

                for col in param_colums:
                    value = row[col]
                    if pd.notna(value):
                        inner_dict[col] = value
                if any(inner_dict.values()):
                    params_list.append(inner_dict)
            
            for url, param in zip(url_list, params_list):
                url_dict_list.append({url: param})
        
            return url_dict_list
        except Exception as e:
            print(f"Error: {e}")
            return None
