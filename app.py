import base64
import time
from io import BytesIO

import pandas as pd
import streamlit as st

import autopy_view as view
import autopy_click as click


def download_link(df, filename, text):
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href


def main():
    st.title("GA4 Automation Test")

    st.header("Upload Files For Page View Parameter")
    upload = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if upload is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file:")
        df = pd.read_csv(upload) if upload.type == 'text/csv' else pd.read_excel(upload, engine='openpyxl')
        st.write(df.head())

        url_dict = view.preprocess(df)

        st.write("Progress of params comparison:")

        progress_bar = st.progress(0)

        if url_dict is not None:
            time.sleep(5)
            progress_bar.progress(10)
            time.sleep(10)
            progress_bar.progress(33)
            result_data_list = view.ga4_params_view(url_dict)

            progress_bar.progress(66)
            formatted_data = view.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = view.data_conv(formatted_data)

            st.header("Processed Data")
            st.write(result_df.head())

            download_href = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href, unsafe_allow_html=True)

    st.header("Honda KPIs")

    upload_click = st.file_uploader("Choose a file for Honda KPIs", type=["csv", "xlsx"])

    if upload_click is not None:
        st.success("File for Honda KPIs successfully uploaded!")

        st.write("Preview of the uploaded file for Honda KPIs:")
        df_honda = pd.read_csv(upload_click) if upload_click.type == 'text/csv' else pd.read_excel(upload_click, engine='openpyxl')
        st.write(df_honda.head())

        url_dict_honda, user_xpath = click.preprocess_click(df_honda)

        st.write("Progress of Honda KPIs processing:")

        progress_bar_honda = st.progress(0)

        if url_dict_honda is not None:
            time.sleep(5)
            progress_bar_honda.progress(10)
            time.sleep(10)
            progress_bar_honda.progress(33)

            result_data_list_honda = click.ga4_params_click(url_dict_honda, user_xpath)

            progress_bar_honda.progress(66)
            formatted_data_honda = click.text_conv(result_data_list_honda)

            progress_bar_honda.progress(100)
            result_df_honda = click.data_conv(formatted_data_honda)

            st.header("Processed Data (Honda KPIs)")
            st.write(result_df_honda.head())

            download_href_honda = download_link(result_df_honda, filename="Honda_KPIs_Test_results.xlsx", text="Download Honda KPIs Test Results")
            st.markdown(download_href_honda, unsafe_allow_html=True)





if __name__ == "__main__":
    main()
