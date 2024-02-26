import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image
from bs4 import BeautifulSoup

# Initialize the app and set the title
st.set_page_config(page_title='MSRC Report Viewer', layout='wide')


# Function to load JSON data
@st.cache
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


def load_html_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


def list_data_files(directory, file_extension=".json"):
    files = [f for f in os.listdir(directory) if f.endswith(file_extension)]
    return sorted(files, reverse=True)


def list_html_files(directory, file_extension=".html"):
    files = [f for f in os.listdir(directory) if f.endswith(file_extension)]
    return sorted(files, reverse=True)


def extract_date_from_filename(filename):
    # Assuming the date is always in the format YYYY_MM_DD
    # and at the same position in the filename
    parts = filename.split('_')
    date_str = '_'.join(parts[-3:])  # Get the last three parts for the date
    date_str = date_str.replace('.json', '').replace('.html',
                                                     '').replace('.png', '')
    return datetime.strptime(date_str, "%Y_%m_%d")


def generate_date_range_from_end(end_date, num_days):
    start_date = end_date - timedelta(days=num_days)
    return (start_date, end_date)


def format_filename_to_date(file_name, prefix=None, suffix=None):
    # Assuming the date is always in the format
    # '_YYYY_MM_DD.html' at the end of the file name
    try:
        date_str = file_name.split('_')[-3:]
        # Removes '.html' from 'DD.html'
        date_str[-1] = date_str[-1].split('.')[0]
        date_obj = datetime.strptime('-'.join(date_str), '%Y-%m-%d')
        # Format the date as 'Report Feb 02, 2024'
        label = f"{prefix if prefix else ''}{date_obj.strftime('%B %d, %Y')}{suffix if suffix else ''}"
        return label, date_obj
    except ValueError:
        # Returns None if the filename does not match the expected format
        return file_name


def display_report(report_data):
    st.header(report_data['report_title'])
    st.subheader(report_data['report_subtitle'])
    st.write(report_data['report_description'])

    # Dynamically generate sections based on table of contents
    for section_key, section_title in report_data['toc'].items():
        st.write(f"## {section_title}")
        section_data = report_data.get(f"{section_key}_data", [])
        for item in section_data:
            st.write(f"### {item['title']}")
            st.write(f"Published: {item['published']}")
            st.write(f"Source: {item['source']}")
            st.write(f"Summary: {item['summary']}")
            # Display more properties as needed


def main():
    st.title("Weekly Report Viewer")

    # Directory where reports and images are stored
    data_directory = './json'
    image_directory = './plots'
    html_directory = './html'

    # with st.container():
    #     st.header("Row 1: Full Width")

    html_files = list_html_files(html_directory)
    formatted_names_to_files = {}

    for file in html_files:
        formatted_name, date_obj = format_filename_to_date(file, "Report ")
        if formatted_name:
            formatted_names_to_files[formatted_name] = file

    # Row 2 - 1/3 + 2/3 layout
    col1, col2 = st.columns([1, 2])

    with col1:
        selected_report = st.selectbox("Select a report",
                                       options=list(
                                           formatted_names_to_files.keys()))
        selected_file = formatted_names_to_files[selected_report]
        st.session_state.selected_file = selected_file

    with col2:

        if 'selected_file' in st.session_state and st.session_state.selected_file:
            # Construct the full path by concatenating the directory and the file name
            file_path = os.path.join(html_directory,
                                     st.session_state.selected_file)
            with open(file_path, 'r', encoding='utf-8',
                      errors='replace') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'html.parser')
            h1_to_remove = soup.find("h1", class_="text-4xl")
            h1_to_remove.decompose()
            h4_to_remove = soup.find("h4", class_="text-2xl text-center")
            h4_to_remove.decompose()
            description_remove = soup.find(
                "div",
                class_="flex-1 bg-white p-2 flex flex-col justify-center")
            description_remove.decompose()
            for show_more_remove in soup.find_all("a", class_="button"):
                show_more_remove.decompose()

            body_content = soup.body
            st.markdown(str(body_content), unsafe_allow_html=True)

        else:
            st.write("Please select a report from the dropdown.")

    # Row 3 - Full Width
    with st.container():
        st.header("Row 3: Full Width")


if __name__ == "__main__":
    main()
