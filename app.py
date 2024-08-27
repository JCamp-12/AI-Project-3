import streamlit as st
import pandas as pd
from utils import query_agent

from dotenv import load_dotenv
load_dotenv()

# Set up session state to track the step
if "step" not in st.session_state:
    st.session_state.step = 1

# Step 1: Upload CSV and display the first 5 rows
if st.session_state.step == 1:
    st.title("CSV Analysis Tool")
    st.header("Upload your CSV file to start analyzing")

    data = st.file_uploader("Choose a CSV file", type="csv")
    data
    if data is not None:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(data)
            if df.empty:
                st.warning("The uploaded CSV file is empty. Please upload a valid file.")
            else:
                st.subheader("First 5 Rows of the Uploaded Data")
                st.write(df.head())

                # Save the DataFrame and data to session state
                st.session_state.data = data
                st.session_state.df = df
                if st.button("Next Step"):
                    st.session_state.step = 2
                    st.rerun()  # Rerun the app to move to the next step
        except pd.errors.EmptyDataError:
            st.error("No columns to parse from file. Please upload a valid CSV file.")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
    else:
        st.warning("Please upload a CSV file to start.")

# Step 2: Check for missing values and run the query
if st.session_state.step == 2:
    st.title("Step 2: Data Analysis")
    st.header("Are There Any Missing Values?")

    # Retrieve the DataFrame from session state
    df = st.session_state.df

    # Display missing val
    df

    data = st.session_state.data
    data
    # Text area for entering the query
    query = 'Are There Any Missing Values?'
    query
    # Button to trigger the analysis
    if st.button("Run Query"):
        if data is not None:
            try:
                # Pass the dataframe and query to the query_agent function
                answer = query_agent(data, query)
                st.write(answer)


                # # Display the result of the query
                # st.subheader("Your Query")
                # st.code(answer.get("input"), language="python")  # Displays the input query

                # st.subheader("Generated Response")
                # st.write(answer.get("output"))
            except Exception as e:
                st.error(f"An error occurred while running the query: {e}")