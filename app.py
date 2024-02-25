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
    report_directory = './json'  # Placeholder path
    image_directory = './plots'  # Placeholder path

    # List available report files
    report_files = list_report_files(report_directory)
    if not report_files:
        st.error("No report files found.")
        return

    print("Setting up report data.")
    # Convert report filenames to dates and create a selection box
    report_dates = [extract_date_from_filename(f) for f in report_files]
    selected_date = st.selectbox("Select a report date:", report_dates)

    # Find the corresponding JSON file for the selected date
    json_filename = f"periodic_report_CVE_WEEKLY_v1_{selected_date.strftime('%Y_%m_%d')}.json"
    json_path = os.path.join(report_directory, json_filename)
    report_data = load_json_data(json_path)

    # Display report data (Placeholder for displaying actual report data)
    st.write("Report data will be displayed here.")

    # Display images associated with the report
    image_filenames = [
        f"posts_by_day_{selected_date.strftime('%Y_%m_%d')}.png",
        f"weekly_totals_{selected_date.strftime('%Y_%m_%d')}.png"
    ]

    for image_filename in image_filenames:
        image_path = os.path.join(image_directory, image_filename)
        try:
            image = Image.open(image_path)
            st.image(image, caption=image_filename)
        except FileNotFoundError:
            st.error(f"Image not found: {image_filename}")
    display_report(report_data)
    st.image(f"plots/posts_by_day_{report_date}.png", caption="Posts by Day")
    st.image(f"plots/weekly_totals_{report_date}.png", caption="Weekly Totals")

if __name__ == "__main__":
    main()
