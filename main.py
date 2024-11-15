import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Title and description
st.title('AI Web Scraper')
st.write('This is a simple web scraper that uses AI to scrape and extract specific data from websites.')

# Input for the URL
url = st.text_input('Enter the URL to scrape:', '')

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

# Optional: Provide option to download the parsed result as a file
if "dom_content" in st.session_state and st.button('Download Parsed Result'):
    result = parse_with_ollama(split_dom_content(st.session_state.dom_content), parse_description)
    st.download_button(label="Download Parsed Content", data=result, file_name="parsed_result.txt", mime="text/plain")
