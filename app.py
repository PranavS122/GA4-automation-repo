import base64
import time
from io import BytesIO

import pandas as pd
import streamlit as st

import autopy_view as view
import autopy_click as click

from autopy_view import GA4_params_tester_view as ga_test_view
from autopy_view import Adobe_params_teter_view as adobe_test_view
from autopy_click import GA4_params_tester_click as ga4_click
from autopy_click import Adobe_params_test_click as adobe_click
from preprocess import Preprocessor as processor


def download_link(df, filename, text):
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False,  header = False, engine='openpyxl')
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'
    return href


def main():

    st.title("GA4 Automation Test")

    st.header("Upload Files For Page View Parameter")
    upload = st.file_uploader("Choose a file", type=["csv", "xlsx"], key="upload_ga_view")

    if upload is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file:")
        df = pd.read_csv(upload) if upload.type == 'text/csv' else pd.read_excel(upload, engine='openpyxl')
        st.write(df)

        url_dict = processor.preprocess_view(df)

        st.write("Progress of params comparison:")

        progress_bar = st.progress(0)

        if url_dict is not None:
            time.sleep(2)
            progress_bar.progress(10)
            time.sleep(2)
            progress_bar.progress(33)
            result_data_list = ga_test_view.ga4_params_view(url_dict)

            progress_bar.progress(66)
            formatted_data = view.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = view.data_conv(formatted_data)

            st.header("Processed Data")
            st.write(result_df)

            download_href = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href, unsafe_allow_html=True)

    st.header("For Clicks upload files here")

    upload_click = st.file_uploader("Choose a file for Clicks", type=["csv", "xlsx"], key="upload_ga_click")

    if upload_click is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file for clicks:")
        df_click = pd.read_csv(upload_click) if upload_click.type == 'text/csv' else pd.read_excel(upload_click, engine='openpyxl')
        st.write(df_click)

        combined_list = processor.preprocess_click(df_click)

        st.write("Progress of Clicks processing:")

        progress_bar = st.progress(0)

        if combined_list is not None:
            time.sleep(5)
            progress_bar.progress(10)
            time.sleep(10)
            progress_bar.progress(33)

            result_data_list = ga4_click.ga4_params_click(combined_list)

            progress_bar.progress(66)
            formatted_data = click.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = click.data_conv(formatted_data)

            st.header("Processed Data for clicks")
            st.write(result_df)

            download_href_honda = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href_honda, unsafe_allow_html=True)

    st.title("Adobe Parameters Test")

    st.header("Upload Files For Page View")
    upload = st.file_uploader("Choose a file", type=["csv", "xlsx"], key = "adobe_upload_view")

    if upload is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file:")
        df = pd.read_csv(upload) if upload.type == 'text/csv' else pd.read_excel(upload, engine='openpyxl')
        st.write(df)

        url_dict = processor.preprocess_view(df)

        st.write("Progress of params comparison:")

        progress_bar = st.progress(0)

        if url_dict is not None:
            time.sleep(5)
            progress_bar.progress(10)
            time.sleep(10)
            progress_bar.progress(33)
            result_data_list = adobe_test_view.view_adobe(url_dict)

            progress_bar.progress(66)
            formatted_data = view.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = view.data_conv(formatted_data)

            st.header("Processed Data")
            st.write(result_df)

            download_href = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href, unsafe_allow_html=True)

    st.header("For Clicks upload files here")

    upload_click = st.file_uploader("Choose a file for Clicks", type=["csv", "xlsx"], key="upload_adobe_click")

    if upload_click is not None:
        st.success("File successfully uploaded!")

        st.write("Preview of the uploaded file for clicks:")
        df_click = pd.read_csv(upload_click) if upload_click.type == 'text/csv' else pd.read_excel(upload_click, engine='openpyxl')
        st.write(df_click)

        combined_list = processor.preprocess_click(df_click)

        st.write("Progress of Clicks processing:")

        progress_bar = st.progress(0)

        if combined_list is not None:
            time.sleep(5)
            progress_bar.progress(10)
            time.sleep(10)
            progress_bar.progress(33)

            result_data_list = adobe_click.adobe_params_click(combined_list)

            progress_bar.progress(66)
            formatted_data = click.text_conv(result_data_list)

            progress_bar.progress(100)
            result_df = click.data_conv(formatted_data)

            st.header("Processed Data for clicks")
            st.write(result_df)

            download_href_honda = download_link(result_df, filename="Test_results.xlsx", text="Download Test Results")
            st.markdown(download_href_honda, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
