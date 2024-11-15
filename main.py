import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama
import json
import pandas as pd

# Title and description
st.title('AI Web Scraper')
st.write('This is a simple web scraper that uses AI to scrape and extract specific data from websites.')

# Input for the URL
url = st.text_input('Enter the URL to scrape:', '')

# Initialize result as None
result = None

# Button to start scraping
if st.button('Scrape Site'):
    if url:  # Check if URL is entered
        st.write("Scraping the site... Please wait.")

        # Scrape the website
        try:
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content

            with st.expander('View DOM content'):
                st.text_area('DOM content:', cleaned_content, height=300)
        except Exception as e:
            st.error(f"Error scraping the site: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")

# Only show parsing options if content is available
if "dom_content" in st.session_state:
    parse_description = st.text_area('What would you like to parse?', 'Enter a description or query')

    if st.button('Parse'):
        if parse_description:
            st.write('Parsing the content...')
            dom_chunks = split_dom_content(st.session_state.dom_content)

            try:
                result = parse_with_ollama(dom_chunks, parse_description)
                if result.strip():  # Check if parsed result is not empty
                    st.write(result)
                else:
                    st.warning("No matching content found.")
            except Exception as e:
                st.error(f"Error parsing the content: {str(e)}")
        else:
            st.warning("Please provide a description of what you want to parse.")

    # Provide an option to select the download format
    if result:
        download_format = st.selectbox(
            "Select file format for download:",
            [".txt", ".csv", ".json"]
        )

        # Provide the download button only if the content is parsed
        if st.button('Download Parsed Result'):
            if result.strip():
                # Prepare the data to be downloaded
                if download_format == ".txt":
                    # Download as a .txt file
                    st.download_button(
                        label="Download as .txt",
                        data=result,
                        file_name="parsed_result.txt",
                        mime="text/plain"
                    )
                elif download_format == ".csv":
                    # Convert the result into CSV format
                    result_list = result.splitlines()  # Split into lines (or further process as required)
                    df = pd.DataFrame(result_list, columns=["Parsed Content"])
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="Download as .csv",
                        data=csv_data,
                        file_name="parsed_result.csv",
                        mime="text/csv"
                    )
                elif download_format == ".json":
                    # Convert the result into JSON format
                    result_json = json.dumps({"parsed_content": result})
                    st.download_button(
                        label="Download as .json",
                        data=result_json,
                        file_name="parsed_result.json",
                        mime="application/json"
                    )
            else:
                st.warning("No parsed content to download.")
