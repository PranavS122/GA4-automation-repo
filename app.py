import base64
import time
from io import BytesIO

import pandas as pd
import streamlit as st

import autopy_2


def preprocess(df):
    try:
        df = df.fillna("")
        url_dict = df.set_index('URL').to_dict(orient='index')
        return url_dict
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_link(df, filename, text):
    """
    Generates a download link for a DataFrame as an Excel file.
    """
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href


def main():
    st.title("GA4 Automation Test")

    st.header("Upload Files")
    upload = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if upload is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file:")
        df = pd.read_csv(upload) if upload.type == 'text/csv' else pd.read_excel(upload, engine='openpyxl')
        st.write(df.head())

        url_dict = preprocess(df)

        st.write("Progress of params comparison:")

        progress_bar = st.progress(0)

        if url_dict is not None:
            time.sleep(5)
            progress_bar.progress(10)
            time.sleep(10)
            progress_bar.progress(33)
            result_data_list = autopy_2.ga4_params_comparison(url_dict)

            progress_bar.progress(66)
            formatted_data = autopy_2.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = autopy_2.data_conv(formatted_data)

            st.header("Processed Data")
            st.write(result_df.head())

            download_href = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
