import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime, timedelta
# from PIL import Image
from bs4 import BeautifulSoup

# Initialize the app and set the title
st.set_page_config(page_title='MSRC Report Viewer', layout='wide')

# flex_container_start = """
# <div style="display: flex; flex-wrap: wrap; gap: 10px;">
# """

# flex_container_end = """
# </div>
# """

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

        return file_name


def display_section_1(report_data):
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

    # Directory where reports and images are stored
    data_directory = './json'
    image_directory = './plots'
    html_directory = './html'

    # with st.container():
    #     st.header("Row 1: Full Width")

    json_files = list_data_files(data_directory)
    formatted_names_to_files = {}
    dates_to_files = {}

    for file in json_files:
        formatted_name, date_obj = format_filename_to_date(file, "Report ")
        if formatted_name and date_obj:
            formatted_names_to_files[formatted_name] = file
            dates_to_files[file] = date_obj

    # Sort the files by their associated date object
    # sorted_files = sorted(dates_to_files, key=dates_to_files.get, reverse=True)

    # If you need to get the sorted formatted names instead of filenames
    sorted_formatted_names = [
        key for key, value in sorted(formatted_names_to_files.items(),
                                     key=lambda item: dates_to_files[item[1]],
                                     reverse=True)
    ]
    style = """
<style>
#root div.withScreencast div div div > section > div {
    padding: 10px; 
}

h1#big-hat-group-weekly-security-update-report {
    font-family: Roboto, sans-serif;
    width: 100%;
    font-weight: 600;
    text-align: center;
}
h4#windows-and-edge-edition {
    font-family: Roboto, sans-serif;
    width: 100%;
    text-align: center;
}
</style>
"""
    st.markdown(style, unsafe_allow_html=True)
    st.title("Big Hat Group Weekly Security Update Report")
    st.markdown("#### (Windows and Edge Edition)")
    col1, col2 = st.columns([1, 2])

    with col1:
        # Initialize selected_report with a placeholder for no selection
        report_options = ["Please select a report"] + sorted_formatted_names
        selected_report = st.selectbox("Select a report",
                                       options=report_options,
                                       index=0)

        if selected_report != "Please select a report":
            selected_file = formatted_names_to_files[selected_report]
            st.session_state.selected_file = selected_file
        else:
            # Handle the case where no report is selected
            st.session_state.selected_file = None

    with col2:
        if 'selected_file' in st.session_state and st.session_state.selected_file:
            file_path = os.path.join(data_directory,
                                     st.session_state.selected_file)
            with open(file_path, 'r', encoding='utf-8',
                      errors='replace') as file:
                report_data = json.load(file)
            section_1_metadata = report_data['section_1_metadata']
            section_1_data = report_data['section_1_data']

            with st.container():
                st.write("## MSRC Posts")
                # Now, iterate through the metadata dictionary
                metadata_string = ""
                for key, value in section_1_metadata.items():

                    metadata_string += f"**{key.replace('_',' ').capitalize()}:** {value},   "
                metadata_string = metadata_string[:-4]
                st.markdown(metadata_string, unsafe_allow_html=True)

            for item in section_1_data:
                post_title = {'title': item['title'], 'source': item['source']}
                st.markdown(
                    f"<a href='{item['source']}'><h3>{item['title']}</h3></a>",
                    unsafe_allow_html=True)
                post_metadata = f"**Revision:** {item['revision']} - **Published:** {item['published']} - **Official Fix:** {'Yes' if item['post_type'] in ['Solution provided', 'Information only'] else 'No'}"
                st.markdown(post_metadata, unsafe_allow_html=True)

                st.markdown(
                    f"**Product Family:** {', '.join(item['core_products'])}")
                
                st.markdown(
                    f"**Build Numbers:** {', '.join(item['build_number_str'])}"
                )

                # KB Articles
                kb_articles_md = ", ".join([
                    f"[{kb['kb_id']}]({kb['kb_link']})"
                    for kb in item['kb_article_pairs']
                ])
                st.markdown(f"**KB Articles:** {kb_articles_md}")

                # Update Packages
                update_packages_md = ", ".join([
                    f"[{package['package_type']}]({package['package_url']})"
                    for package in item['package_pairs']
                ])
                st.markdown(f"**Update Packages:** {update_packages_md}")

                st.markdown(f"**Summary:** {item['summary']}")

                st.markdown("---")
                
            section_4_data = report_data['section_4_data']
            section_4_metadata = report_data['section_4_metadata']
            collection_label = ""
            for doc in section_4_data:
                if collection_label == "":
                    collection_label = doc['collection'].replace("_", " ").capitalize()
                    st.markdown(f"### {collection_label}")
                elif doc['collection'].replace("_", " ").capitalize() != collection_label:
                    collection_label = doc['collection'].replace("_", " ").capitalize()
                    st.markdown(f"### {collection_label}")
                    
                st.markdown(f"[{doc['title']}]({doc['source']})")
                    

        else:
            # Display a friendly message
            st.text("Select a report to view its details.")


if __name__ == "__main__":
    main()
