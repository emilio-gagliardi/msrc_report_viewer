import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from PIL import Image

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


def list_report_files(directory, file_extension=".json"):
    files = [f for f in os.listdir(directory) if f.endswith(file_extension)]
    return sorted(files)


def extract_date_from_filename(filename):
    # Assuming the date is always in the format YYYY_MM_DD and at the same position in the filename
    parts = filename.split('_')
    date_str = '_'.join(parts[-3:])  # Get the last three parts for the date
    date_str = date_str.replace('.json', '')  # Remove the file extension
    return datetime.strptime(date_str, "%Y_%m_%d").date()


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
    report_directory = './json'
    image_directory = './plots'
    print(f"report data is at: {report_directory}"
          f"report plots are at: {image_directory}")
    with st.container():
        st.header("Row 1: Full Width")

    # Row 2 - 1/3 + 2/3 layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Row 2: 1/3")
        # Add your widgets here for the 1/3 column
    with col2:
        st.subheader("Row 2: 2/3")
        # Add your widgets here for the 2/3 column

    # Row 3 - Full Width
    with st.container():
        st.header("Row 3: Full Width")


if __name__ == "__main__":
    main()
