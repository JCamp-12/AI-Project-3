import streamlit as st
from dotenv import load_dotenv
from utils import query_agent


# Load environment variables from a .env file
load_dotenv()

# Set up the main title and header for the app
st.title("CSV Analysis Tool")
st.header("Upload your CSV file to start analyzing")

# File uploader widget for CSV files
data = st.file_uploader("Choose a CSV file", type="csv")

# Text area for entering the query
query = st.text_area("Enter your query here")

# Button to trigger the analysis
if st.button("Generate Response"):
    # Ensure a file is uploaded before processing
    if data is not None:
        # Process the uploaded file and the query using the query_agent function
        answer = query_agent(data, query)
        
        # Display the result of the query
        st.subheader("Your Query")
        st.code(answer.get("input"), language="python")  # Displays the input query
        
        st.subheader("Generated Response")
        st.write(answer.get("output"))
    else:
        # Display a message if no file was uploaded
        st.warning("Please upload a CSV file before submitting a query.")



# st.write(df.head())