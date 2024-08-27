import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from utils import query_agent

# Load environment variables from a .env file
load_dotenv()

# Initialize session state to keep track of the current step
if 'step' not in st.session_state:
    st.session_state.step = 1

# Define functions to move to the next or previous steps
def next_step():
    st.session_state.step += 1

def previous_step():
    st.session_state.step -= 1

# Step 1: Upload CSV File
if st.session_state.step == 1:
    st.title("Step 1: Upload your CSV file")
    data = st.file_uploader("Choose a CSV file", type="csv")

    if data is not None:
        st.session_state.data = pd.read_csv(data)
        st.button("Next", on_click=next_step)
    else:
        st.warning("Please upload a CSV file to proceed.")

# Step 2: Are There any Missing values?
elif st.session_state.step == 2:
    st.title("Step 2: Missing Values Check")
    st.write("Checking for missing values in the dataset...")
    
    missing_values = st.session_state.data.isnull().sum()
    st.write(missing_values[missing_values > 0])
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 3: Are there Duplicate Rows?
elif st.session_state.step == 3:
    st.title("Step 3: Duplicate Rows Check")
    st.write("Checking for duplicate rows in the dataset...")
    
    duplicates = st.session_state.data.duplicated().sum()
    st.write(f"There are {duplicates} duplicate rows.")
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 4: Are there any Outliers?
elif st.session_state.step == 4:
    st.title("Step 4: Outliers Detection")
    st.write("Checking for outliers in numerical columns...")
    
    outliers = st.session_state.data.describe().T[['mean', 'std']].copy()
    outliers['Outliers'] = ((st.session_state.data - outliers['mean']).abs() > 3 * outliers['std']).sum()
    st.write(outliers[['Outliers']])
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 5: Are there any Extreme Values?
elif st.session_state.step == 5:
    st.title("Step 5: Extreme Values Check")
    st.write("Checking for extreme values in numerical columns...")
    
    extreme_values = st.session_state.data.describe(percentiles=[.01, .99]).T[['min', '1%', '99%', 'max']]
    st.write(extreme_values)
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 6: Are all columns the correct Data Type?
elif st.session_state.step == 6:
    st.title("Step 6: Data Types Check")
    st.write("Checking if all columns have the correct data types...")
    
    data_types = st.session_state.data.dtypes
    st.write(data_types)
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 7: Are any Date Columns not in date time format?
elif st.session_state.step == 7:
    st.title("Step 7: Date Columns Format Check")
    st.write("Checking if any date columns are not in datetime format...")
    
    date_columns = st.session_state.data.select_dtypes(include=['object']).columns
    not_datetime = [col for col in date_columns if not pd.to_datetime(st.session_state.data[col], errors='coerce').notna().all()]
    st.write(not_datetime if not_datetime else "All date columns are correctly formatted.")
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 8: Should any columns be renamed?
elif st.session_state.step == 8:
    st.title("Step 8: Column Renaming Suggestions")
    st.write("Checking if any columns should be renamed...")
    
    st.write("Current column names:")
    st.write(st.session_state.data.columns)
    
    st.text_input("Enter new column names as a comma-separated list:", key="new_columns")
    
    if st.session_state.new_columns:
        new_names = st.session_state.new_columns.split(',')
        st.session_state.data.columns = new_names
        st.write("Columns have been renamed.")
    
    st.button("Previous", on_click=previous_step)
    st.button("Next", on_click=next_step)

# Step 9: Are there are some large differences between the mean and max values in some columns?
elif st.session_state.step == 9:
    st.title("Step 9: Mean vs Max Values Check")
    st.write("Checking for large differences between the mean and max values in some columns...")
    
    mean_max_diff = (st.session_state.data.max() - st.session_state.data.mean()).sort_values(ascending=False)
    st.write(mean_max_diff)
    
    st.button("Previous", on_click=previous_step)
    st.success("All steps completed!")
