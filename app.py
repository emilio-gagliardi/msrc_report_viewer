import streamlit as st
import os
import json


# Initialize the app and set the title
st.set_page_config(page_title='MSRC Report Viewer', layout='wide')


# Function to load JSON data
@st.cache
def load_json_data(report_name):
    with open(f'json/{report_name}.json') as json_file:
        return json.load(json_file)


# Function to display the report
def display_report(report_name):
    # Load the JSON data
    # data = load_json_data(report_name)
    # Display data using Streamlit components
    # TODO: Implement the display logic
    pass


# Function to list all available reports
def list_reports():
    return os.listdir('json')


# Function to style the selected report
# TODO: Implement styling with Tailwind CSS


# Sidebar for listing reports
report_list = list_reports()
report_name = st.sidebar.selectbox('Select a report:', report_list)

# Display the selected report
if report_name:
    display_report(report_name)
