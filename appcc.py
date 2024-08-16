import streamlit as st
import pandas as pd
import os

# Path to the folder where CSV files are stored
csv_folder = "./data/"

# List of CSV filenames
csv_files = [
    'eg-and-csv.csv',
    'eg-ios-csv.csv',
    'iq-and-csv.csv',
    'ir-ios-csv.csv',
    'mo-and-csv.csv',
    'mo-ios-csv.csv',
    'sa-and-csv.csv',
    'sa-ios-csv.csv',
    'uae-and-csv.csv',
    'uae-ios-csv.csv'
]

# Streamlit app title
st.title("CSV Data Viewer")

# Display header image
header_image_path = os.path.join(csv_folder, "image.png")
if os.path.exists(header_image_path):
    st.image(header_image_path)
else:
    st.warning("Header image not found.")

# Display the build signature
st.markdown("<div style='text-align: center; background-color: #1f3b4d; padding: 10px; border-radius: 10px;'><span style='color: white;'>Build by DW 8-14-23</span></div>", unsafe_allow_html=True)

# Display each CSV file's data
for csv_file in csv_files:
    # Construct full CSV path
    csv_path = os.path.join(csv_folder, csv_file)
    
    # Load the CSV file with a different encoding
    try:
        df = pd.read_csv(csv_path, encoding='ISO-8859-1')
        st.write(f"### {csv_file}")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to load {csv_file}: {e}")
